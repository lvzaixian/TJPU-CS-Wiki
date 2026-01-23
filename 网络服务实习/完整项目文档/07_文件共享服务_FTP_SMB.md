# 内容四：文件共享服务 (FTP/SMB)

## 一、Server1 域环境配置与加入

### 1. 验证 DNS 解析状态

**操作目的/推理**：在加入域（AD）之前，首要任务是确保 Server1 能够正确解析域控制器的域名。域环境强依赖 DNS 服务，若无法通过域名找到域控（192.168.1.102），后续的加入操作将无法进行。

**操作命令**：

```bash
resolvectl status
```

![DNS 状态](assets/image-20260108215105864.png)

Server1 解析域相关记录都会去问 Server3。

```bash
nslookup home.lab 192.168.1.102
```

![DNS 解析验证](assets/image-20260108215218315.png)

说明可以解析我们的域名。

---

### 2. 安装必要的系统工具与依赖

**操作目的/推理**：为了实现 Linux 与 Windows AD 的互操作性，需要安装：
- `realmd`：域管理工具
- `sssd`：系统安全服务守护进程
- `krb5-user`：Kerberos 客户端
- `acl`：细粒度文件权限控制
- `ftp`：FTP 客户端用于测试

**操作命令**：

```bash
sudo apt update
sudo apt -y install realmd sssd sssd-tools libnss-sss libpam-sss adcli krb5-user packagekit samba-common-bin chrony dnsutils sssd-ad acl ftp
```

**配置交互记录**：在安装过程中，Kerberos 配置向导会弹出提示：
- `Default Kerberos version 5 realm:` 输入 **HOME.LAB**
- `Kerberos servers for your realm:` 输入 **192.168.1.102**
- `Administrative server for your Kerberos realm:` 输入 **192.168.1.102**

---

### 3. 配置时间同步 (NTP)

**操作目的/推理**：AD 域登录认证的核心机制是 Kerberos，该协议为了防止重放攻击，对通信双方的时间差非常敏感（默认容忍误差在 5 分钟以内）。必须确保 Server1 与域控的时间保持严格同步。

**操作命令**：

```bash
sudo timedatectl set-ntp true
chronyc sources -v
```

![时间同步](assets/image-20260108221301376.png)

> 执行后确认已找到最优时间源，且偏差极小（记录显示偏差仅 16ms），满足 Kerberos 认证要求。

---

### 4. 发现并加入 AD 域

**探测域信息**：

```bash
realm discover home.lab
```

![发现域](assets/image-20260108220547648.png)

> 此时输出包含 `configure: no`，表明 Server1 尚未加入域。

**加入域**：

```bash
sudo realm join home.lab -U Administrator
```

> 执行后需输入域管理员密码。

**验证加入状态**：

```bash
realm list
```

![加入域验证](assets/image-20260108234430012.png)

> `configured` 行显示为 `kerberos-member`，证明已成功加入域。

---

### 5. 配置域用户家目录自动创建

**操作目的/推理**：域用户在 Linux 服务器上没有本地预设的家目录。需要配置 PAM 模块自动创建家目录。

**启用自动创建功能**：

```bash
sudo pam-auth-update --enable mkhomedir
```

**修改配置文件细节**：

```bash
sudo nano /etc/pam.d/common-session
```

找到以下行：
```
session optional                        pam_mkhomedir.so
```

修改为：
```
session optional                        pam_mkhomedir.so skel=/etc/skel umask=0022
```

> `umask=0022` 确保新创建的家目录权限为 755。

---

## 二、文件共享权限规划与 FTP 服务配置

### 1. 验证域用户身份与可用性

**操作目的/推理**：FTP 服务（vsftpd）默认使用 Linux 系统 PAM 模块进行认证。在域环境中，域用户通过 SSSD 映射为系统用户。如果底层系统无法识别域用户，FTP 登录必然失败。

**操作命令**：

```bash
id 'teacher01@home.lab'
```

![域用户验证](assets/image-20260109092727661.png)

返回 uid/gid 信息，证明域用户已被本机识别。

---

### 2. 共享目录规划与 ACL 权限配置

**权限设计思路**：
1. **物理隔离**：创建不同子目录（admins/teachers/students），直观展示权限边界
2. **安全基线**：根目录 `/srv/share` 设为 root 所有且不可写，满足 vsftpd `chroot` 安全要求
3. **权限控制**：使用 ACL 实现精细化授权

#### 2.1 创建目录结构

```bash
mkdir -p /srv/share/{admins,teachers,students,public}
```

#### 2.2 设置根目录安全权限

```bash
sudo chown -R root:root /srv/share
sudo chmod 755 /srv/share
```

#### 2.3 配置 ACL 细粒度权限

**权限矩阵设计**：

![权限矩阵](assets/image-20260109152124266.png)

**前置确认域组名称**：

```bash
getent group admins@home.lab
getent group teachers@home.lab
getent group students@home.lab
```

![获取组信息](assets/image-20260109093451367.png)

**定义变量与执行授权**：

```bash
GADM="admins@home.lab"
GTEA="teachers@home.lab"
GSTU="students@home.lab"

# admins 目录：只有 admins rwx
sudo setfacl -m g:"$GADM":rwx /srv/share/admins
sudo setfacl -d -m g:"$GADM":rwx /srv/share/admins
sudo setfacl -m m:rwx /srv/share/admins
sudo setfacl -d -m m:rwx /srv/share/admins

# teachers 目录：admins + teachers rwx
sudo setfacl -m g:"$GADM":rwx,g:"$GTEA":rwx /srv/share/teachers
sudo setfacl -d -m g:"$GADM":rwx,g:"$GTEA":rwx /srv/share/teachers
sudo setfacl -m m:rwx /srv/share/teachers
sudo setfacl -d -m m:rwx /srv/share/teachers

# students 目录：admins + teachers + students rwx
sudo setfacl -m g:"$GADM":rwx,g:"$GTEA":rwx,g:"$GSTU":rwx /srv/share/students
sudo setfacl -d -m g:"$GADM":rwx,g:"$GTEA":rwx,g:"$GSTU":rwx /srv/share/students
sudo setfacl -m m:rwx /srv/share/students
sudo setfacl -d -m m:rwx /srv/share/students

# public：三组只读可进入
sudo mkdir -p /srv/share/public
sudo setfacl -m g:"$GADM":r-x,g:"$GTEA":r-x,g:"$GSTU":r-x /srv/share/public
sudo setfacl -d -m g:"$GADM":r-x,g:"$GTEA":r-x,g:"$GSTU":r-x /srv/share/public
sudo setfacl -m m:r-x /srv/share/public
sudo setfacl -d -m m:r-x /srv/share/public
```

> **注意**：`setfacl -d` 用于设置默认 ACL，确保目录下新建的文件能自动继承父目录权限。

#### 2.4 验证权限设置

```bash
getfacl /srv/share/teachers
getfacl /srv/share/students
getfacl /srv/share/admins
```

**teachers 目录验证**：

![teachers ACL](assets/image-20260109152721033.png)

可以看到 teachers 目录 admin 和 teachers 拥有读写执行权限，符合预期。默认继承规则也生效。

**students 目录验证**：

![students ACL](assets/image-20260109152827115.png)

**admins 目录验证**：

![admins ACL](assets/image-20260109152634309.png)

---

### 3. 安装与配置 FTP 服务 (vsftpd)

#### 3.1 安装服务

```bash
sudo apt update
sudo apt -y upgrade
sudo apt -y install vim ufw net-tools
sudo apt -y install vsftpd
sudo systemctl enable --now vsftpd
sudo systemctl status vsftpd
```

![vsftpd 状态](assets/image-20260108143612052.png)

显示 active 说明 vsftpd 已经启动。

#### 3.2 配置 vsftpd

**配置设计思路**：
1. **安全加固**：禁用匿名登录，限制用户只能在自己的目录活动 (`chroot`)
2. **域集成**：开启本地用户登录以支持域账号
3. **路径统一**：强制所有用户登录后进入 `/srv/share`
4. **网络适配**：配置被动模式端口范围，防止在虚拟化 NAT 网络下数据连接卡死
5. **文件权限**：设置 `local_umask=002`，确保新建文件对组内成员可写

**备份与编辑**：

```bash
sudo cp /etc/vsftpd.conf /etc/vsftpd.conf.bak
sudo vim /etc/vsftpd.conf
```

**配置文件关键内容**：

```ini
# 1) 监听模式：让 FTP 服务在本机 21 端口监听
listen=YES
listen_ipv6=NO

# 2) 禁止匿名登录（实验环境必须禁）
anonymous_enable=NO

# 3) 允许本地用户登录（域用户通过 SSSD 也会被当作"本地可识别用户"）
local_enable=YES

# 4) 允许写入（上传/创建目录等）
write_enable=YES

# 5) 把用户"关"在指定目录里，避免浏览系统敏感目录（安全设计）
chroot_local_user=YES
allow_writeable_chroot=YES

# 6) 登录后默认进入的目录（和 SMB/NFS 统一）
local_root=/srv/share

# 7) 日志（报告排错/截图很有用）
xferlog_enable=YES
log_ftp_protocol=YES

# 8) 被动模式端口：避免客户端卡在 LIST/上传（强烈建议）
pasv_enable=YES
pasv_min_port=40000
pasv_max_port=40100

# 9) 权限掩码设置
local_umask=002
```

#### 3.3 重启验证

```bash
sudo systemctl restart vsftpd
sudo systemctl status vsftpd --no-pager
sudo ss -lntp | grep -E ':21|vsftpd'
```

![FTP 端口监听](assets/image-20260109103036821.png)

确认 21 端口处于监听状态。

---

### 4. 补全域用户家目录

**操作目的/推理**：虽然配置了 PAM 自动创建家目录，但该机制通常在用户**交互式登录**时触发。FTP 登录可能不会触发。如果用户没有家目录，vsftpd 可能会报 500 错误。

**操作命令**（以 admin01 为例）：

```bash
# 第一步：查询家目录路径
H="$(getent passwd admin01 | cut -d: -f6)"
echo "$H"

# 第二步：创建家目录并设置权限
sudo install -d -m 0750 -o admin01 -g "$(id -gn admin01)" "$H"
```

> 对其他 5 个测试用户重复此步骤。

---

## 三、SMB (Samba) 共享服务配置

### 1. 安装 Samba 服务

**操作目的/推理**：Ubuntu Server 默认不包含 SMB 协议支持。为了让 Windows 客户机能够通过"网上邻居"或映射网络驱动器的方式访问 Linux 服务器上的文件，必须安装 samba 服务端。

```bash
sudo apt update
sudo apt install samba smbclient -y
```

**检查服务状态**：

```bash
systemctl status smbd
```

![Samba 状态](assets/image-20260109160708284.png)

服务状态为 active (running)，可以继续配置。

---

### 2. 初始化配置文件

**备份与清空**：

```bash
sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.bak
sudo bash -c 'echo "" > /etc/samba/smb.conf'
```

---

### 3. 配置 Samba 核心参数与共享目录

**配置设计思路**：
1. **加入域信任**：通过 `security = ads` 和 `realm = HOME.LAB` 让 Samba 代理域控进行身份验证
2. **权限对接**：启用 `vfs objects = acl_xattr`，强制 Samba 尊重我们设置的 ACL
3. **共享定义**：分别定义 Teachers、Students、Admins 和 Public 四个共享区

**编辑配置文件**：

```bash
sudo nano /etc/samba/smb.conf
```

**写入配置内容**：

```ini
[global]
   # === 核心鉴权配置 ===
   workgroup = CORP
   security = ads
   realm = HOME.LAB
   
   # 让 Samba 使用 SSSD/Realmd 已经配置好的 Kerberos 凭证
   kerberos method = secrets and keytab
   
   # 日志设置
   log file = /var/log/samba/log.%m
   log level = 1
   max log size = 1000

   # === ID 映射与域支持 ===
   idmap config * : backend = tdb
   idmap config * : range = 3000-7999
   
   # 允许不支持加密的老旧客户端
   server min protocol = SMB2

   # === 文件系统与权限衔接 ===
   vfs objects = acl_xattr
   map acl inherit = yes
   store dos attributes = yes

   # 禁用打印机加载
   load printers = no
   printing = bsd
   printcap name = /dev/null
   disable spoolss = yes

# ================= 共享目录定义 =================

[teachers]
   comment = Teachers Share
   path = /srv/share/teachers
   read only = no
   browsable = yes
   valid users = @"teachers@home.lab" @"admins@home.lab"
   create mask = 0664
   directory mask = 0775

[students]
   comment = Students Share
   path = /srv/share/students
   read only = no
   browsable = yes
   valid users = @"students@home.lab" @"admins@home.lab"
   create mask = 0664
   directory mask = 0775

[admins]
   comment = Admin Only Share
   path = /srv/share/admins
   read only = no
   valid users = @"admins@home.lab"
   create mask = 0660
   directory mask = 0770

[public]
   comment = Public Read Only
   path = /srv/share/public
   read only = yes
   browsable = yes
   guest ok = yes
```

---

### 4. 安装与配置 Winbind

**操作目的/推理**：Samba 服务需要 winbind 组件来处理与 AD 域控制器的 RPC 通信、用户列表获取以及 NTLM 认证转换。

```bash
sudo apt update
sudo apt install winbind libpam-winbind libnss-winbind -y
```

**重启服务生效**：

```bash
sudo systemctl restart smbd nmbd winbind
```

---

### 5. 验证域用户同步状态

```bash
wbinfo -u
```

![域用户同步](assets/image-20260110010439008.png)

此命令列出 Winbind 从 AD 域控制器同步到 Server1 的所有域用户，说明配置正确。

---

## 四、权限验证矩阵

| 用户 | admins 目录 | teachers 目录 | students 目录 | public 目录 |
|------|-------------|---------------|---------------|-------------|
| admin01 | ✅ 读写 | ✅ 读写 | ✅ 读写 | ✅ 只读 |
| teacher01 | ❌ 拒绝 | ✅ 读写 | ✅ 读写 | ✅ 只读 |
| stu01 | ❌ 拒绝 | ❌ 拒绝 | ✅ 读写 | ✅ 只读 |
