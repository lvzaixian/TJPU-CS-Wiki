# 内容六：Web 服务与维护权限

## 一、Nginx Web 服务配置 (Server2)

### 1. 安装 Nginx

```bash
sudo apt update
sudo apt install nginx -y
```

![安装 Nginx](assets/image-20260109193706-5hwfqlw.png)

---

### 2. 准备网页内容

在 `/var/www/html` 下准备 `index.html`：

![网页内容](assets/image-20260109193257-x0n8as3.png)

> **说明**：由于已经挂载了 NFS，此处的文件实际存储在 Server1 上。

---

### 3. Nginx 配置

Nginx 默认站点配置就是 serve `/var/www/html` 下的所有文件，无需额外配置：

![Nginx 配置](assets/image-20260109193633-1iirdg9.png)

---

### 4. 配置文件权限

确保 `www-data` 组用户能够读取 `index.html`：

```bash
sudo chown www-data:www-data /var/www/html/index.html
```

![文件权限](assets/image-20260109194039-7ujedal.png)

---

### 5. 内网访问验证

现在可以在内网机器通过域名或 IP 访问：

**通过 IP 访问**：

![IP 访问](assets/image-20260109184711-at3gh3r.png)

**通过域名访问**：

![域名访问](assets/image-20260109184637-fa3m3gj.png)

---

## 二、外网访问配置 (端口转发)

### 1. 配置端口映射

在主路由 R1 (OpenWRT) 创建端口转发规则：

![端口转发配置](assets/image-20260109173057-c2ty2m9.png)

---

### 2. 解决 Server2 双网卡路由问题

为了解决 Server2 上双网卡的非对称路由问题，需要在 `netplan` 中配置路由策略：

指示所有来自 `192.168.1.101` 的包都去查路由表 100，再于路由表 100 中配置让包前往 Server2 的网关（防火墙）：

```yaml
# /etc/netplan/00-installer-config.yaml
network:
  version: 2
  ethernets:
    enp1s0:
      dhcp4: true
      dhcp4-overrides:
        route-metric: 200
    enp2s0:
      dhcp4: true
      dhcp4-overrides:
        route-metric: 100
      routing-policy:
        - from: 192.168.1.101
          table: 100
      routes:
        - to: default
          via: 192.168.1.1
          table: 100
```

![路由策略配置](assets/image-20260109192040-hk5gxmm.png)

应用配置：

```bash
sudo netplan apply
```

---

### 3. 外网访问验证

现在可以在外网通过 `192.168.122.100:8080` 访问：

![外网访问](assets/image-20260109190839-7852w8p.png)

---

## 三、DNS 域名解析配置

### 1. 添加 A 记录

利用 Server3 自带的 DNS 服务为 192.168.122.100 添加一条 A 记录：

```powershell
Add-DnsServerResourceRecordA -Name "www" -ZoneName "home.lab" -IPv4Address "192.168.122.100"
```

![添加 DNS 记录](assets/image-20260109214838-w9ikx98.png)

---

### 2. 域名访问验证

现在可以通过域名访问网页：

![域名访问网页](assets/image-20260109215025-tij89bx.png)

也可以连接到 R1 的 Web 界面：

![R1 管理界面](assets/image-20260109215112-3jma8p6.png)

---

### 3. 端口优化

为了确保美观（通过 80 端口访问到的是 Web 界面，而不是 R1 的管理界面），调整端口配置：
- Web 服务端口映射监听 80 端口
- 管理界面改为 8080 端口

**R1 管理界面端口修改**：

![R1 端口修改](assets/image-20260109220400-a9wak3h.png)

**Web 端口映射修改**：

![Web 端口映射](assets/image-20260109215439-iapg3yb.png)

现在可以直接访问 Web 主页面：

![直接访问 Web](assets/image-20260109215817-wiedvhs.png)

并通过 8080 端口访问 R1 管理界面：

![8080 访问管理](assets/image-20260109220327-alfrbi4.png)

---

## 四、Web 维护权限配置 (Server1)

### 1. 配置 SMB 共享段

**操作目的/推理**：管理员在 Windows 客户机上开发网页时，使用 SMB（网上邻居/映射驱动器）直接编辑代码效率最高。需要将 `/srv/share/www_root` 暴露给 SMB 服务，并配置强制权限掩码。

**编辑配置文件**：

```bash
sudo nano /etc/samba/smb.conf
```

**添加配置内容**（在文件末尾添加）：

```ini
[web_root]
   comment = Web Server Root (Admins Only)
   path = /srv/share/www_root
   read only = no
   browsable = yes
   # 核心限制：只允许 admins 组
   valid users = @"admins@home.lab"
   # 权限修正：保证上传的文件 Web 服务器也能读
   force create mode = 0664
   force directory mode = 2775
```

**参数说明**：
- `valid users`：严格限制只有域管理员组能访问，防止学生或教师误改网页
- `force create mode = 0664`：强制新文件权限为 `rw-rw-r--`（Owner/Group可写，Others可读）
- `force directory mode = 2775`：强制新目录权限为 `rwxrwxr-x`，并保留 SGID 位

**重启服务**：

```bash
sudo systemctl restart smbd
```

---

### 2. 底层权限标准化 (ACL配置)

**操作目的/推理**：实验环境中存在多种写入途径（SMB、FTP、本地 CLI）。为了实现"统一标准"，需要在文件系统底层使用 ACL 来兜底。

**权限目标**：
1. **文件**：`rw-rw-r-- (664)` -> 管理员读写，Web 服务器只读
2. **目录**：`rwxrwxr-x (775)` -> 管理员能进能改，Web 服务器能进能读

**清洗旧权限**：

```bash
setfacl -R -b /srv/share/www_root
```

**设定现有文件的绝对控制权**：

```bash
setfacl -R -m g:"admins@home.lab":rwx /srv/share/www_root
```

**设定默认 ACL (继承规则)**：

```bash
# 这行命令保证了：以后不管谁上传文件，Admins组永远有 rwx，其他人永远有 r-x
setfacl -R -d -m g:"admins@home.lab":rwx /srv/share/www_root
setfacl -R -d -m o::rx /srv/share/www_root
```

**参数说明**：
- `-d` (Default)：仅对**未来新建**的文件/目录生效
- `g:"admins@home.lab":rwx`：新文件自动给管理员组读写执行权限
- `o::rx`：新文件自动给 Others（包括 Web 服务器进程）读和执行权限

---

## 五、维护权限验证矩阵

| 操作 | 管理员 (admin01) | 教师 (teacher01) | 学生 (stu01) | 外部用户 |
|------|------------------|------------------|--------------|----------|
| 访问网页 (HTTP) | ✅ | ✅ | ✅ | ✅ |
| SMB 访问 web_root | ✅ 读写 | ❌ 拒绝 | ❌ 拒绝 | ❌ |
| FTP 上传到 www_root | ✅ | ❌ | ❌ | ❌ |
| 修改网页代码 | ✅ | ❌ | ❌ | ❌ |

---

## 六、工作流程图

```
┌──────────────────────────────────────────────────────────────────────┐
│                        Web 维护工作流程                               │
└──────────────────────────────────────────────────────────────────────┘

1. 管理员登录 Windows 客户端 (admin01@home.lab)
                              │
                              ▼
2. 打开资源管理器，访问 \\server1.home.lab\web_root
                              │
                              ▼
3. 编辑/上传网页文件 (index.html, style.css, etc.)
                              │
                              ▼
4. 文件保存到 Server1 的 /srv/share/www_root
                              │
                              ▼
5. Server2 通过 NFS 挂载自动读取到更新后的文件
                              │
                              ▼
6. 用户通过浏览器访问 http://www.home.lab 看到更新后的网页
```
