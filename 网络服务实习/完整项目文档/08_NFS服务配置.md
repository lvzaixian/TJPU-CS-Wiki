# 内容五：NFS 服务配置

## 一、典型应用场景

本项目采用 **"存储与计算分离"** 的企业级架构：
- **Server1**：作为存储后端，提供 NFS 共享
- **Server2**：作为 Web 前端，挂载 NFS 读取网页文件

这样实现了：
1. Web 服务器无需本地存储网页文件
2. 管理员可以通过 SMB/FTP 远程维护网页
3. 数据集中存储，便于备份和管理

---

## 二、NFS 服务端配置 (Server1)

### 1. 创建 Web 存储目录

**操作目的/推理**：创建一个专门存放网站文件的仓库。在配置初期，为了排除权限干扰，确保 Server2 挂载后能读写，暂时赋予最高权限。

```bash
sudo mkdir -p /srv/share/www_root
sudo chmod -R 777 /srv/share/www_root
echo "<h1>This is hosted on Server1 (NFS)</h1>" | sudo tee /srv/share/www_root/index.html
```

---

### 2. 安装 NFS 服务

```bash
sudo apt update
sudo apt install nfs-kernel-server -y
sudo systemctl enable nfs-kernel-server
```

---

### 3. 配置 NFS 导出策略

**操作目的/推理**：配置 `/etc/exports` 允许 Web 服务器 (192.168.1.101) 访问。

参数说明：
- `sync`：确保数据实时写入磁盘，防止断电丢数据
- `no_root_squash`：**关键配置**，允许 Server2 的 root 用户在挂载点保留 root 权限，对后续数据迁移至关重要

```bash
sudo nano /etc/exports
```

**写入配置内容**：

```
/srv/share/www_root 192.168.1.101(rw,sync,no_root_squash,no_subtree_check)
```

**应用配置**：

```bash
sudo exportfs -arv
sudo systemctl restart nfs-kernel-server
```

![NFS 导出](assets/image-20260110114538743.png)

> 执行后确认 `/srv/share/www_root` 已共享。

---

## 三、NFS 客户端配置 (Server2)

### 1. 安装 NFS 客户端

```bash
sudo apt update
sudo apt install nfs-common -y
```

---

### 2. 备份原有网页目录

**操作目的/推理**：Server2 原有的默认网页文件需要保留，防止挂载覆盖后丢失。

```bash
sudo mv /var/www/html /var/www/html_bak
sudo mkdir -p /var/www/html
```

---

### 3. 挂载 NFS 共享

```bash
sudo mount -t nfs 192.168.1.100:/srv/share/www_root /var/www/html
```

**验证连通性**：

```bash
curl localhost
```

![NFS 挂载验证](assets/image-20260110115311168.png)

> 返回 `<h1>This is hosted on Server1 (NFS)</h1>`，证明挂载成功。

---

### 4. 数据回迁与恢复

**操作目的/推理**：将备份的网页数据"倒"回新的挂载点（实际写入 Server1），恢复业务显示。

```bash
# 清理测试文件
sudo rm -rf /var/www/html/*

# 把备份目录里的所有东西"倒"进挂载点
sudo cp -r /var/www/html_bak/* /var/www/html/

# 验证
ls /var/www/html/
```

**最终内容检查**：

```bash
cat /var/www/html/index.html
```

![内容验证](assets/image-20260110123428414.png)

> 此时应看到原有的默认主页代码，说明业务已恢复。

---

### 5. 配置开机自动挂载

编辑 `/etc/fstab`：

```bash
sudo nano /etc/fstab
```

添加以下行：

```
192.168.1.100:/srv/share/www_root /var/www/html nfs defaults,_netdev 0 0
```

> `_netdev` 参数确保在网络可用后再尝试挂载。

---

## 四、权限控制强化 (Server1)

### 1. 收回 777 权限

**操作目的/推理**：挂载验证通过后，必须收回之前的 777 权限，实施严格的安全控制。

**归属调整**：将目录所有权交给 `admins` 域组，确保只有管理员能管理网页。

```bash
sudo chown -R root:"admins@home.lab" /srv/share/www_root
```

**设置 SGID 权限**：

```bash
# 设置权限为 2775
# 2 (SetGID): 以后在这个目录下新建的文件，自动属于 admins 组
# 7 (Owner-Root): rwx
# 7 (Group-Admins): rwx (管理员可读写)
# 5 (Others-Web): r-x (Web服务器只读，关键！)
sudo chmod -R 2775 /srv/share/www_root
```

**验证最终权限**：

```bash
ls -ld /srv/share/www_root
```

![权限验证](assets/image-20260110123801156.png)

> 输出显示 `drwxrwsr-x`，其中 `s` 代表 SGID 位已生效。

---

## 五、NFS 架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                           管理员 (Client3)                           │
│                    通过 SMB/FTP 上传网页文件                          │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Server1 (文件服务器)                            │
│                  /srv/share/www_root                                │
│                     • 存储网页文件                                   │
│                     • 提供 NFS 导出                                  │
│                     • 提供 SMB 共享                                  │
└─────────────────────────────┬───────────────────────────────────────┘
                              │ NFS (192.168.1.100:/srv/share/www_root)
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Server2 (Web 服务器)                            │
│                  /var/www/html (NFS 挂载点)                         │
│                     • Nginx 读取网页文件                             │
│                     • 对外提供 HTTP 服务                             │
└─────────────────────────────┬───────────────────────────────────────┘
                              │ HTTP (Port 80)
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         外部用户访问                                 │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 六、验证 NFS 服务状态

在 Server1 上检查 NFS 服务状态：

```bash
systemctl is-active nfs-kernel-server
```

在 Server2 上检查挂载状态：

```bash
df -h | grep 192.168.1.100
```

预期输出显示 `192.168.1.100:/srv/share/www_root` 挂载在 `/var/www/html`。
