# 内容七：VPN 服务配置

## 一、方案选型

### 为什么选择 OpenWRT + WireGuard？

原计划使用 iKuai 作为 VPN 服务端，但 iKuai 默认不支持 WireGuard 等现代 VPN 协议。虽然可以通过安装 Docker 容器解决，但存在以下问题：
- Docker 配置不够自由
- Dockerhub 网络问题难解决
- iKuai 没有 HTTP 代理支持

因此选择在 **OpenWRT** 上配置 WireGuard VPN 服务端，获取更多自由度。

---

## 二、WireGuard VPN 配置 (R1 OpenWRT)

### 1. 生成密钥对

通过 OpenWRT 命令行生成两对密钥：
- 服务端密钥对
- 客户端（对等端）密钥对

```bash
# 生成一对私钥+公钥并打印到屏幕上
wg genkey | tee /dev/tty | wg pubkey
```

---

### 2. 创建 VPN 接口

用第一对做服务端密钥创建虚拟 VPN 接口：

```bash
# 1. 创建接口并命名为 'vpn'
uci set network.vpn=interface
uci set network.vpn.proto='wireguard'

# 2. 填入服务端私钥
uci set network.vpn.private_key='<服务端私钥>'

# 3. 设置监听端口
uci set network.vpn.listen_port='51820'

# 4. 设置服务端 VPN IP
uci add_list network.vpn.addresses='10.13.13.1/24'
```

---

### 3. 添加对等节点 (Peer)

用第二对密钥创建一个对等节点：

```bash
# 1. 添加一个 WireGuard Peer 节点
uci add network wireguard_vpn

# 2. 填入客户端公钥
uci set network.@wireguard_vpn[-1].public_key='<客户端公钥>'

# 3. 设置允许该客户端使用的 IP
# 这告诉 OpenWrt：只要源 IP 是 10.13.13.2 的包，就是这个 Peer 发来的
# 发往 10.13.13.2 的包，要用这个公钥加密发给它
uci add_list network.@wireguard_vpn[-1].allowed_ips='10.13.13.2/32'

# 4. 路由允许
uci set network.@wireguard_vpn[-1].route_allowed_ips='1'
```

---

### 4. 应用配置

```bash
uci commit network
/etc/init.d/network restart
```

---

### 5. 配置截图

![WireGuard 配置1](assets/image-20260109151821-j1ifbd8.png)

![WireGuard 配置2](assets/image-20260109114648-v6gtbf8.png)

![WireGuard 配置3](assets/image-20260109151734-ooew7nk.png)

---

## 三、客户端配置文件

### 1. 生成 wg1.conf

编写客户端所用的 WireGuard 配置文件：

```toml
[Interface]
# 接口（客户端）私钥
PrivateKey = CBZIH/5XD2erTfYDMQ5dIsr0MZ0c5fMVyLdwaDGlnkU=
Address = 10.13.13.2/24
DNS = 192.168.1.102

[Peer]
# 对等节点（服务端）公钥
PublicKey = SCJImV92ldhQs1gYoA9fDSaegSW/hhnsqeXJiDVneyQ=
# 对等节点端点 R1 的 WAN1 地址 
Endpoint = 192.168.122.100:51820
AllowedIPs = 10.13.13.0/24, 192.168.1.0/24, 192.168.13.0/24, 192.168.14.0/24
PersistentKeepalive = 25
```

**参数说明**：
- `Address`：客户端在 VPN 网络中的 IP
- `DNS`：使用内网 DNS 服务器（Server3）
- `AllowedIPs`：允许通过 VPN 隧道访问的网段
- `PersistentKeepalive`：保持连接活跃，穿透 NAT

---

## 四、服务器端路由配置

### 解决 Ubuntu Server 双网卡路由问题

为了解决两个 Ubuntu Server 双网卡的路由冲突问题，需要在它们各自的 `netplan` 配置中补充一条前往 VPN 隧道的路由：

```yaml
# /etc/netplan/00-installer-config.yaml
network:
  version: 2
  ethernets:
    enp2s0:
      dhcp4: true
      routes:
        - to: 10.13.13.0/24
          via: 192.168.1.1
```

![服务器路由配置](assets/image-20260109182514-wn1pfay.png)

---

## 五、VPN 连接验证

### 1. 客户端连接

客户端启用 WireGuard 接口后即可访问内网 `home.lab` 域：

![VPN 连接成功](assets/image-20260109153405-roho3bl.png)

### 2. 访问内网服务

**通过 IP 访问 Web 服务**：

![IP 访问 Web](assets/image-20260109173612-du91539.png)

**通过域名访问 Web 服务**：

![域名访问 Web](assets/image-20260109184353-av9wnq9.png)

---

## 六、VPN 网络拓扑

```
┌─────────────────────────────────────────────────────────────────────┐
│                          互联网 / 公网                               │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  远程办公用户1   │  │  远程办公用户2   │  │  远程办公用户3   │
│  VIP: 10.13.13.2│  │  VIP: 10.13.13.3│  │  VIP: 10.13.13.4│
│  WireGuard      │  │  WireGuard      │  │  WireGuard      │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │ WireGuard 隧道
                              │ (UDP 51820)
                              ▼
                    ┌─────────────────┐
                    │  R1 (OpenWRT)   │
                    │  WAN: 122.100   │
                    │  VPN: 10.13.13.1│
                    └────────┬────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│    Server1      │  │    Server2      │  │    Server3      │
│  File (FTP/SMB) │  │  Web (Nginx)    │  │  AD/DNS         │
│  192.168.1.100  │  │  192.168.1.101  │  │  192.168.1.102  │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## 七、VPN 访问权限验证

通过 VPN 连接后可以访问的服务：

| 服务 | 访问方式 | 验证方法 |
|------|----------|----------|
| DNS 解析 | 192.168.1.102:53 | `nslookup server1.home.lab` |
| Web 服务 | http://server2.home.lab | 浏览器访问 |
| SSH | ssh root@server1.home.lab | 终端连接 |
| SMB 共享 | \\\\server1.home.lab | Windows 资源管理器 |
| FTP | ftp://server1.home.lab | FTP 客户端 |
| R1 管理 | http://192.168.122.100:8080 | 浏览器访问 |
| FW 管理 | http://192.168.13.150 | 浏览器访问 |
