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
* CIDR块：如16.158.165.91/22，子网掩码前22位都是1，起始ip是16.158.164.1，某位是16.158.167.255
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
  * 第三步中X网关把目标ipY变成ipB的过程是DNAT：目标地址转换
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

















