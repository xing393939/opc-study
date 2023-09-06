### 趣谈网络协议

#### 参考资料
* [趣谈网络协议](https://book.douban.com/subject/35013753/)

#### 第1章 通讯协议概述
* 大前提：两台机器之间必须知道mac地址才能点对点通讯
* 局域网内如何知道对方的mac地址？发送arp广播，对方回应mac地址
* 什么是二层设备？就是对比mac，看看是接收、丢弃还是转发
* 什么是三层设备？就是对比mac，再对比ip，看看是接收、丢弃还是转发
* 机器配置的网关ip必须保证和自己的某一个网卡是同一个网段的
* net-tools：ifconfig命令，已经停止维护
* iproute2：ip addr命令
* CIDR块：如16.158.165.91/22，子网掩码前22位都是1，则ip是16.158.164.0~16.158.167.255
* DHCP：机器没有配置DHCP地址，发送DHCP广播，DHCP服务器会应答并返回它的ip和你的新ip

#### 第2章 从二层到三层
* mac是局域网的定位，ip是跨网络的定位
* 已知对方ip地址求mac地址？发送arp广播
* 两台电脑网线直连：先发送ARP(内核包含此逻辑)获取到mac再通讯
* 三台电脑Hub通讯：Hub每次收到数据就转发给所有的电脑
* 交换机学习的过程：
  * 最开始不知道每台电脑的mac，所以转发给所有的电脑，记住发送方的mac
  * 一段时间后，记住了所有电脑的mac，存入转发表
  * 后续收到数据就转发给指定mac的电脑
* 交换机的vlan：
  * vlan是为了保证隔离，避免局域网内被人抓包
    * [ARP欺骗攻击](https://songly.blog.csdn.net/article/details/104786319)
    * [MAC地址泛洪攻击](https://blog.csdn.net/qq_35733751/article/details/104139771)
  * 链路层的mac头包含：目标mac、源mac、vlan_id
  * 手动设置交换机上每个网口所属的vlan_id，vlan_id相同的包才会互相转发
  * 交换机有个特殊的网口称为Trunk口，可以无视vlan_id转发包，一般用于对接其他交换机
* ping命令：使用了icmp的echo request和echo reply类型
* traceroute命令：发送带ttl的udp包，途径最后一个路由器，路由器返回icmp包
* 转发网关：A机器——X网关左手——X网关右手——B机器
  * A机->X左：macA机，ipA -> macX左，ipB
  * X左->X右：macX左，ipA -> macX右，ipB
  * X右->B机：macX右，ipA -> macB机，ipB
* NAT网关：A机器——X网关——Y网关——B机器
  * A机->X关：macA机，ipA -> macX关，ipY
  * X关->Y关：macX关，ipX -> macY关，ipY
  * Y关->B机：macY关，ipY -> macB机，ipB
  * 其中A机器，ipA是它的内网ip，ipX是它的外网ip，B机器同理
  * 第二步中X网关把源ipA变成ipX的过程是SNAT：源地址转换
  * 第三步中Y网关把目标ipY变成ipB的过程是DNAT：目标地址转换
* 静态路由配置：源ip是？目标ip是？——>经XX网口，下一跳ip是XX  
* 基于距离矢量路由算法的BGP协议：
  * 基于Bellman-Ford算法
  * 如果新路由器加入很快就广播了，而下线则不知道
  * 某路由器更新时发送整个路由表
  * 适合数据中心之间的连接
  * 使用TCP协议，端口是179
* 基于链路状态路由算法的OSPF协议：
  * 基于Dijkstra算法
  * 路由器下线也会广播
  * 某路由器更新时发送变更的部分
  * 适合数据中心内部的连接
  * 使用IP协议，协议编号是89

#### 第3章 最重要的传输层
* TCP和UDP的区别
  * TCP面向连接，接收方和发送方都要维护对应的数据结构；UDP是无连接的，发送数据之前不需要建立连接
  * TCP保证可靠传输；UDP不保证可靠
  * TCP面向字节流；UDP是面向报文的
  * TCP连接是一对一；UDP支持一对一和多播
  * TCP首部开销20~60字节；UDP的首部开销只有8个字节
* UDP定制化的五个例子
  * Google的QUIC，在应用层实现可靠传输、拥塞控制
  * 直播协议，网络不好允许丢包 
  * 实时游戏，只在乎丢包但在乎实时响应 
  * IOT物联网，芯片上内存资源有限，UDP开销小 
  * 移动通讯领域4G的GTP-U，因为GTP协议本身就保证了通讯的可靠
* TCP的四次挥手，以A和B打电话为例：
  * A说“我没啥要说的了”，B回答“我知道了”
  * B可能还会有要说的话，于是B可能又巴拉巴拉说了一通
  * 最后B说“我说完了”，A回答“知道了”。B说完需要等ack后才能关闭连接，A回答完要等2MSL才能关闭：
    * B如果没有收到ack(ack包丢了)，会再发送一次“我说完了”
    * A为什么要等2MSL，因为2MSL内B都没有再发送“我说完了”，证明已经收到ack包了
* 顺序问题和丢包问题：
  * 累计确认，不用一个包一个ack
  * 超时重传，超时时间应>RTT(往返时间)
  * 快速重传，需重传序号7的包：连续三个序号7的ack
  * SACK(选择确认)：`ACK=10,SACK=15-20`表示15~20已收到，10~14没有
* 流量控制：
  * 更新滑动窗口，接收方返回ack的同时返回AdvertiseWindow
  * 若接收方AdvertiseWindow=0，发送方停止发送，定时发送窗口探测包看是否会调整窗口
* 拥塞控制：
  * 慢开始：cwnd=1，每次指数增长
  * 拥塞避免：窗口内包的总大小>ssthresh，每次cwnd+=1/cwnd
  * (重新慢开始)：发生丢包，ssthresh=cwnd/2 && cwnd=1
  * 快重传：收到连续3个ack提示丢包，快速重传
  * 快恢复：快重传时丢包并不严重，cwnd=cwnd/2 && ssthresh=cwnd
  
#### 第4章 最重要的应用层
* Http keep-alive机制：
  * http 1.0：客户端头带上Connection: Keep-Alive，服务器头带上Connection: Keep-Alive
  * http 1.1：默认已经是keep-alive，除非指定Connection: Close
  * Keep-Alive: timeout=5, max=1000 表示空闲时长5秒，可发送的请求量是1000
* TCP keep-alive机制：可对单个socket设置，否则使用内核默认配置
  * setsockopt(sockfd, SOL_SOCKET, SO_KEEPALIVE, (void *)&keepAlive, sizeof(keepAlive)); 开启keepalive
  * setsockopt(sockfd, SOL_TCP, TCP_KEEPIDLE, (void*)&keepIdle, sizeof(keepIdle)); 空闲时长
  * setsockopt(sockfd, SOL_TCP, TCP_KEEPINTVL, (void *)&keepInterval, sizeof(keepInterval)); 探测包间隔时间
  * setsockopt(sockfd, SOL_TCP, TCP_KEEPCNT, (void *)&keepCount, sizeof(keepCount); 失败后尝试几次
* Http 2.0
  * 解决了Http 1.1队首阻塞问题，同一个连接可并行发送多个请求和响应
  * 每个请求可以有多个stream
  * Magic stream是发送方三次握手后的第一帧，接收方ack后意味着H2正式连接，内容固定24B：PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n
  * 不同类型的stream的头部固定是9字节(Magic类型除外)：
    * length(3B)：整个stream的长度
    * type(1B)：类型，0~9依次是DATA/HEADERS/PRIORITY/RST_STREAM/SETTINGS/PUSH_PROMISE/PING/GOAWAY/WINDOW_UPDATE/CONTINUATION
    * flags(1B)：stream类型不同代表的含义也不同
    * streamId(4B)：stream id，最高的1位是预留位
* Http 3.0：基于使用UDP的QUIC协议
  * H2的问题1：受限于[TCP重组](https://blog.csdn.net/jackyzhousales/article/details/78050640)，虽然stream2和stream1没有关联，但是stream1没有到达stream2不能提交给用户，称为TCP层的队首阻塞
  * H2的问题2：受限于TCP四元组，如果发送方网络变化导致IP变化则需要重连，QUIC不使用四元组而是随机数
  * H2的问题3：受限于TCP，拥塞控制粒度是连接，H3的粒度是连接的stream
* HTTPS 加密传输流程：
  * 客户端先client hello发给服务端随机数randomClient
  * 服务端再server hello发给客户端随机数randomServer
  * 服务端发送公钥证书
  * 客户端利用根证书验证此公钥证书
  * 客户端使用公钥证书加密传输随机数pre-master给服务端
  * 后续双方就使用randomClient、randomServer、pre-master加密传输数据
* 流媒体协议、P2P下载

#### 第5章 陌生的数据中心
* cdn一般有glsb，用户->权威ns得到cname->cdn的ns得到cname->cdn的glsb->cdn节点
* httpdns：必须要有客户端sdk，httpdns的服务地址需写死在sdk里
* 动态cdn：1.定时同步db，部署边缘计算；2.优化用户和源站的线路
* 机房中的2层网络
* IPSec VPN（ip层的加密传输）
  * DH（diffie-hellman）算法：在不安全的网络交换对称密钥K
    * A和B都有黄色（指数p和q）
    * A有蓝色（私钥a），B有红色（私钥b）
    * A这边黄色+蓝色=绿色，B这边黄色+红色=橙色，AB交换绿色、橙色
    * A这边橙色+蓝色=棕色，B这边绿色+红色=棕色，棕色是对称密钥K
  * https为什么不用DH算法？DH算法不能验证身份，不能防止中间人攻击
* 在巴塞罗那手机上网为什么不能访问脸书？上网时巴的运营商中转给国内运营商了

#### 第6章 云计算中的网络
* 网络模式之桥接：
  * 同主机的虚机A和虚机B通讯：A和B分别有虚拟网卡A和B，再建立一个网桥bridge0，A、B、主机都在一个网段
  * 主机1的虚机A和主机2的虚机C通讯：主机1和主机2用交换机连接，A、C、主机1、主机2都处于同一个网段
  * [网桥与交换机的区别](https://blog.csdn.net/fivedoumi/article/details/51746798)
* 网络模式之NAT：
  * 同主机的虚机A和虚机B通讯：通过虚拟交换机。A、B通过NAT设备(路由器)与主机通讯，和主机不在一个网段
  * 主机1的虚机A和主机2的虚机C通讯：需要使用overlay方案
* 主机防火墙的五个关卡：
  * PREROUTING：数据包必过
  * INPUT：数据包进入主机
  * FORWARD：转发数据包
  * OUTPUT：数据包从主机出来
  * POSTROUTING：数据包必过
* 主机防火墙的4个规则表优先级高到低：raw –> mangle –> nat –> filter
  * raw，不常用
  * mangle，修改数据包
  * nat，网络地址转换，DNAT和SNAT
  * filter，过滤数据包
* 主机防火墙规则有匹配条件和处理动作组成
  * 链路层匹配条件：源mac、目标mac、vlan_id
  * 链路层处理动作：源mac、目标mac、vlan_id的修改
  * 网络层匹配条件：源ip、目标ip
  * 网络层处理动作：源ip、目标ip的修改
  * 传输层匹配条件：源port、目标port
  * 传输层处理动作：源port、目标port的修改
* k8s的kube-proxy就是利用的iptables做流量转发和负载均衡的
  * service利用nat将相应的流量转发到对应的pod中，另外iptables有一个probability特性，可以设置probability的百分比是多少，从而实现负载均衡
* underlay和overlay：
  * underlay是底层网络，由物理网络设备组成
  * overlay是基于隧道技术实现的，overlay的流量需要跑在underlay之上  
* overlay的三种技术方案：
  * [Calico网络方案](https://www.cnblogs.com/netonline/p/9720279.html)
  * GRE：外层IP头 + GRE头 + 内层IP包，缺点是只能点对点通讯
  * VXLAN：外层UDP头 + UDP主体(VXLAN头 + 内层IP包)，支持组播(多对多通讯)
  * IPIP：IP in IP，ipip包头较vxlan小，安全性不如vxlan

#### 第7章 容器中的网络
* Docker的网络模式默认使用NAT
* Docker容器与主机的端口映射的两种方式（主机的10080->容器的80）：
  * 主机建立docker-proxy进程，监听10080端口，把网络包转发到容器的80端口
  * 主机建立一条DNAT，把10080的网络包转发到容器的80端口
* Flannel项目的UDP模式：主机1的容器A(172.17.8.2)访问主机2的容器B(172.17.9.2)
  * 容器A先发给默认网关，即网桥docker0(172.17.8.1)
  * docker0读取主机1的路由策略，再发给flannel.1网卡
  * 主机1的flanned读取flannel.1网卡的网络包，封装一层UDP头，发给主机2
  * 主机2的flanned收到UDP，解UDP，把原始数据包发给flannel.1网卡
  * flannel.1读取主机2的路由策略，把包发给docker0，再发给容器B
* Flannel项目的VXLAN模式：
  * 容器A先发给默认网关，即网桥docker0(172.17.8.1)
  * docker0读取主机1的路由策略，再发给flannel.1网卡(内核建立的VTEP)
  * 主机1的flannel.1根据主机的ARP表、FDB表封装好VXLAN数据包，发给主机2
  * 主机2的flannel.1解VXLAN数据包，把原始数据包发给flannel.1网卡
  * flannel.1读取主机2的路由策略，把包发给docker0，再发给容器B
  * (主机的route表、ARP表、FDB表由flanneld来维护)
* Calico项目-主机同网段：纯三层网络
  * 去掉网桥docker0，容器配置路由到主机的网卡
  * 主机的网卡充当路由器功能
  * 主机之间用交换机连接
* Calico项目-主机跨网段：IPIP模式

#### 第7章 微服务相关协议
* ONE RPC
  * 协议约定：每次改动都要重写生成stub
  * 传输协议：二进制
  * 服务发现：portmapper
* SOAP(simple object access protocol)
  * 协议约定：服务地址+?wsdl，xml描述文件
  * 传输协议：http + post xml 文本
  * 服务发现：UDDL注册中心
* Spring Cloud
  * 协议约定：Restful接口协议
  * 传输协议：http
  * 服务发现：eureka
* Dubbo
  * 协议约定：Hessian2
  * 传输协议：Netty网络框架
  * 服务发现：各种注册中心如Zookeeper、Redis、Etcd
* gRPC
  * 协议约定：Protocol Buffers
  * 传输协议：http2.0
  * 服务发现：各种注册中心如Envoy
* Dubbo和SpringCloud的优缺点
  * 功能：Dubbo只实现了服务治理，而SpringCloud覆盖了微服务架构下的众多部件
  * 性能：Dubbo使用RPC，SpringCloud使用Http Restful，Dubbo略胜
