### AWS认证

#### 资料
1. udemy.com 网站排名127
1. ACloudGuru 的视频依然是最好的学习材料，它把它的竞争对手 Linux Academy 收购了。
1. Learning Path - [(SAP-C01) Exam Learning Path](https://jayendrapatil.com/aws-certified-solution-architect-professional-exam-learning-path/)
1. AWS Github Study Guide - https://github.com/keenanromain/AWS-SAA-C02-Study-Guide
1. AWS FAQs https://aws.amazon.com/faqs/
1. WhitePapers https://aws.amazon.com/cn/whitepapers/
1. [中国区AWS价格计算器](https://cloud.engineerdraft.com/ec2)
1. 视频：https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c02/
1. 练习1：https://www.udemy.com/course/aws-certified-solutions-architect-associate-amazon-practice-exams-saa-c02/
1. 练习2：https://www.udemy.com/course/practice-exams-aws-certified-solutions-architect-associate
1. 如何通过console的System Managers登录ec2：
  * ec2需要附加一个role（带2个policy），[参考](https://wangfeng.live/2020/09/aws-uses-session-manager-to-log-in-and-manage-ec2-hosts)
  * ec2需要安装amazon-ssm-agent，[参考](https://aws.amazon.com/cn/premiumsupport/knowledge-center/install-ssm-agent-ec2-linux/)
  * ec2如果不能访问外网，则需要建立内网Endpoints，[参考](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-getting-started-privatelink.html)

#### 存储相关
1. block storage（容量16T）：
  * General Purpose SSD （gp2/gp3）：1.6w IOPS，适合随机IO
  * Provisioned SSD（io1/io2）：6.4w IOPS，适合随机IO，适合数据库
  * io2 Express：25.6w IOPS
  * Throughput Optimized HDD （st1）：500 IOPS，适合顺序IO，频繁访问
  * Cold HDD （sc1）：250 IOPS，适合顺序IO，非频繁访问
  * Instance Store：200w IOPS，关机数据丢失；hibernate数据也会丢失
  * 特点1：io1/io2 现在支持Multi-Instance-Attach（最多支持16个EC2）
  * 特点2：st1和sc1不能作为启动卷，其他包括上一代的磁介质都可以；Instance Store是附带的启动卷，但是不能作为系统盘
  * EBS加密卷，卷与实例之间的传输也是加密的
  * EBS卷可以不停机的更改类型和增加size，除了磁介质；但不能减小size
  * 在EC2 Dashboard可以设置ebs默认开启加密
1. file storage：
  * Amazon Elastic File System：50w IOPS，多ec2共享，容量不限。pay-as-you-use；使用NFS协议
  * Amazon FSx for Windows：network filesystem for Windows，容量64T
  * Amazon FSx For Lustre：100w IOPS，容量不限；可和S3高度集成；适合 HPC(high-performance computing)
  * EFS的模式：性能模式（GP、MAX IO）、吞吐量模式（Provisioned、Bursting）、存储模式（Standard、Infrequent Access）
  * EFS的配置：EFS Access Points to manage access；Attach an IAM policy；VPC security groups
1. object storage：S3，如果出现file storage则不能选S3
  * Standard
  * Intelligent：智能
  * Standard-IA：不经常访问、取回有费用；上传后等30天、文件>128K才能切到此类型
  * One Zone-IA：单AZ；上传后等30天、文件>128K才能切到此类型
  * Glacier：>90天，取回时间1m~12h；不能被Athena查询；默认是加密的
  * Glacier Deep Archive：>180天，取回时间12h~48h
  * 特点1：S3 cross-Region replication 只能复制新增文件；s3 sync命令可以跨region复制
  * 特点2：可以通过default setting或者显式设置文件保留时长，同一个文件不同版本的保留时长可以不一样
  * 特点3：S3 is strongly consistent for all GET, PUT and LIST operations
  * 特点4：S3 event notification 只支持Standard SQS不支持FIFO SQS 
  * 特点5：S3 的 Metadata 不能被加密
1. EBS 的优点：
  * 自动在当前AZ备份，单block failure后自动替换
  * 不停机的更换 type, size, IOPS capacity
1. S3 生命周期
  * 标准 > IA > IT > One-Zone-IA > Glacier > Glacier-Deep，低层不能转换到高层
  * 转换到 IA 和 One-Zone-IA 需要文件大于128K、30天后才能转

#### Auto Scaling Group
1. Auto Scaling Group 特性
  * launch configuration 使用了就不能修改，要修改就新建一个 launch configuration，只能新建一个type的ec2
  * launch template 比lc新，有版本控制，能新建多个type的ec2
  * lifecycle hooks 可以对一个实例使用 custom script 
  * 删除 ASG，会附带删除所有 EC2
1. Auto Scaling Group scaling 策略
  * simple scaling：只有一个门槛，超过会新增实例，为了防止频繁新增，默认有冷却时间（300秒）
  * step scaling：可设多个门槛，例如>50%加1个实例，>60%加2个实例，没有冷却时间
  * target tracking：只设一个门槛（1分钟检查一次，3次超标就xx），傻瓜式的，目的是保持在这个门槛值附近
  * scheduled scaling：支持cron表达式
  * 特点1：scaling activity，先terminate unhealthy instance，再起新的instance；re-balancing activity 则相反
  * 特点2：多个策略同时被触发，scale-out取最大数量的实例
1. Auto Scaling Group terminate 策略
  * 多AZ选择AZ中ec2最多的
  * ec2中配置项最老的
  * ec2中最接近账单周期的
  * 满足以上条件的ec2随机terminate
1. 健康检查：
  * ec2 健康检查：running状态的ec2就是health
  * elb 健康检查：running状态的ec2，且ping检查合格

#### 账号集成
* Access AWS resources using on-premises credentials stored in Active Directory ！！！    
* Amazon Cognito 两大组件
  1. user pools：提供用户登录和directory service，为了安全可启用多重验证(MFA)作为二次验证
  1. identity pools：provide AWS credentials to grant your users access to other AWS services
* 常见组件：
  1. web identity federation：可以和idp服务集成
  1. identity provider (IdP)：提供登录认证 

#### RDS、Aurora、DynamoDB
* Amazon RDS automatically performs a fail-over when：
  1. Loss of availability in primary Availability Zone.
  1. Loss of network connectivity to primary.
  1. Compute unit failure on primary.
  1. Storage failure on primary.
* Amazon RDS Metrics：
  1. regular items：CPU Utilization, Database Connections, Freeable Memory
  1. Enhance items：OS processes, RDS processes, RDS child processes
* RDS fail-over：
  1. 启用了Multi-AZ：Amazon RDS points CNAME to the standby, promoted it an new primary
  1. 启用了Read Replica（须先启用自动备份）：主节点不可用时，手动提升Read Replica为主节点
* Aurora fail-over：
  1. if 启动了 Aurora Replica，将CNAME指向不同AZ的副本
  1. elseif 启动了 Aurora Serverless，在不同AZ重建一个实例
  1. else，在相同AZ重建一个实例
* Aurora 可跨5个region建只读副本（延迟在1秒内）；双写功能不能跨region。
* Aurora 性价比：相同的吞吐量，Aurora 比 DynamoDB 便宜，存储价格两者差不多。
* RDS 只有 MySQL 和 PostgreSQL 支持 IAM auth；SQL Server 不支持，安全连接的方法：
  1. 设置 rds.force_ssl 开启 ssl
  1. 下载 RDS Root CA 到实例内  
* 存储数据库密码、API密钥的方案：
  1. AWS Secrets Manager：manage database credentials, passwords, API keys, arbitrary text. encrypted and regular rotated.
  1. Systems Manager Parameter Store：可以存明文、密文，但是不会 regular rotated.
* RDS 特点
  1. RDS Multi-AZ follows synchronous replication and spans at least two AZ. Read replicas follow asynchronous replication  
  1. RDS 一个没有加密的instance，不能更改加密；不能创建一个加密的replica；只能先创建snapshot，从snapshot创建一个加密的instance
  1. RDS 没有自签名证书
  1. RDS Multi-AZ 更新补丁：先更新standby把它提为primary，再更新旧primary把它提为standby
  1. RDS Multi-AZ 升级版本：standby和primary同时更新，会有downtime
  1. RDS 和 Aurora 都有storage auto-scaling
  1. RDS 修改存储大小需要重启、而设置自动扩容不需要  
  1. 共享数据库给审计部门：共享 encrypted snapshot, 再共享 KMS encryption key
* 备份还原：
  1. RDS 需开启自动备份（间隔5分钟），可设置保留时间（0~35天，默认7天），还原的时候选择还原点（snapshot）创建一个新实例
  1. Aurora 自动备份是默认开启的，可设置保留时间（1~35天，默认1天），可恢复到保留时间内的任意时间点，可选择创建一个新实例（需几小时）或直接回溯（需几分钟）
  1. 手动快照 RDS 和 Aurora 都支持，保留时间随意

#### SQS、SNS、SWF、Step functions
1. SQS retention period is from 1 minute to 14 days
1. SQS 的 ReceiveMessageWaitTimeSeconds 默认是0，表示 Short polling，如果大于0，则是 Long polling
1. SQS FIFO support 3000 messages per second with batching, or up to 300 messages per second；可以消息分组(最多100组)
1. SNS 也能触发lambda，也有FIFO类型
1. Simple Workflow Service (SWF)：creating a decoupled architecture in AWS；不会重复消费任务；适合ec2，已过时，除非有父子进程信号才用
1. Step functions：适合lambda、ECS、API Gateway；替代SWF
1. 特点1：SQS message timers 可以针对单个消息设置延迟；delay queues则针对全局

#### 防火墙
1. AWS Firewall Manager：simplifies your AWS WAF and AWS Shield and VPC Security Groups administration across multiple accounts and resources.
1. Amazon GuardDuty：一种智能威胁检测服务，通过 CloudTrail 日志、VPC 流日志、DNS 日志分析出账户盗用、存储桶入侵、异常 API 调用、恶意 IP 、挖矿病毒等活动，并自动化响应。
1. Amazon Macie：在S3中分析出敏感内容，如密钥、密码、身份证等然后提醒你
1. Amazon Inspector：检查EC2实例是否存在意外的网络可访问性和漏洞。
1. AWS WAF：七层协议的防护（ALB, API Gateway, CloudFront），功能有ACL（封ip、header、url）、SQL注入、XSS、Rate-based for DDoS、Block with IPs or geo。
1. AWS Shield：三层/四层协议、高级的DDoS防护，标准版免费、高级版可以用于EIP、ELB、CloudFront、Global Accelerator、Route53。没有rate-based rules

#### 负载均衡器
1. 同ip多域名https支持(SNI)：CLB不支持，ALB、ELB、CloudFront支持
1. 支持websocket：ALB支持；ELB仅支持HTTP、HTTPs、TCP、UDP、TLS，可以在ec2层实现websocket，然后用TCP->ws，TLS->wss。
1. 只有ALB支持 path-based and host-based routing，ELB不支持Weighted Target Groups
1. Connection Draining：实例会多一种unregistering状态（健康检查异常但没有完全确认），new或者in-flight请求会导到其他机器
1. cross-zone 特性：默认LB只有单zone的能力（假设AZ1有2个ec2，AZ2有8个ec2，AZ1和AZ2只能同时分配50%）
1. ALB、CLB有安全组；NLB、NAT Gateway没有安全组；安全组只有allow rule，没有deny rule；NCALs有deny rule

#### 加速传输
1. Snowball：80T，可用多个；如果用100Mb带宽传，得200天；不能直接存S3 Glacier！！！
1. Snowmobile：100P
1. AWS Storage Gateway：使用S3、FSx等扩展本地机房的存储（不支持EFS）；local caching可以加速访问；
  1. File Gateway：接口是NFS/SMB，底层存储对应S3
  1. Volume Gateway：接口是iSCSI
  1. Tape Gateway：接口是iSCSI
  1. 要记住：block protocols 是 iSCSI and file protocols 是 NFS
1. AWS DataSync：不能加速，接口比较广泛：S3, EFS, Fsx for Windows
1. S3 Transfer Acceleration：全球各地的客户需要上传S3，还能提升下载速度；CloudFront也有相同功效（限1G以内文件）
1. AWS Direct Connect（DX）：需要最少一月的搭建
1. AWS Site to Site VPN（IP-sec）

#### 加速全球访问
1. AWS Global Accelerator：给节点（NLB、ALB、EC2、EIP）加速；good fit for gaming(UDP), IoT(MQTT), static IP(Http)；可以跨region蓝绿部署
1. AWS CloudFront

#### 网络连通
1. VPC endpoints 有三类
  1. gateway endpoints：把S3、DynamoDB变成私网服务，免费
  1. Private Link（Interface endpoints, Gateway Load Balance endpoints）：把非S3、DynamoDB服务等变成私网服务，有ENI，付费
1. Direct Connect Gateway：打通一个本地机房到多个 AWS 的区域
1. AWS VPN CloudHub：打通多个本地机房的连接（依赖VPN或DX）
1. AWS Transit Gateway：可以理解为云上的路由器，在每一个 Region 中创建一个 TGW，就可以将它们 Peering 起来

#### 大数据
1. AWS Kinesis Firehose：是一个消化管道，延迟60秒，不加处理的传给S3、Redshift、ElasticSearch；程序不能直接消费它
1. AWS Kinesis Streams：是实时和自定义的，延迟1秒，可以自定义处理数据；默认保留数据1天；程序可以直接消费它；关键字：real-time analytics；消息是有序的
1. AWS Redshift：支持OLAP，不支持ACID，是最终一致性；不能动态扩容；亚秒级响应
1. AWS DynamoDB：支持毫秒级响应
1. 特点1：Kinesis Agent可以写入Kinesis Streams、Kinesis Firehose，但是如果Kinesis Streams已经连接了Kinesis Firehose，此时不能直接写Kinesis Firehose

#### 容灾
* active-active：每个节点都是主节点；active-passive：一般都是主节点提供服务，从节点容灾
* High Availability：不间断服务；Fault Tolerance：假设需要4个ec2，目前AZ1有2个，AZ2有2个，如果AZ1挂了，虽然是不间断，但是容错能力不够，最好是两个AZ都4个ec2
* Disaster recovery 级别（从低到高）
  1. Backup & Restore：RPO in hours
  1. Pilot Light 最小环境（通常也称为 Cold Standby）：RPO in minutes
  1. Warm Standby 小规模热备环境：RPO in seconds
  1. Multi-Site active-active部署（通常也称为 Hot Standby）：RPO near 0

#### EC2
1. ec2：不是running状态无需付费，但从stopping到hibernate状态需要；预留实例terminated状态也要付费
1. EC2 Spot Block 可以有1-6小时固定预留时间
1. EC2 Scheduled Reserved 必须是每天有固定时间段（周末不用可以允许）
1. EC2 的AMI镜像依赖snapshot的存在
1. EC2 Default instances的母机是不确定的，Dedicated instances的母机是属于同一账号的，Host instances 母机是独享的；Host instances和Dedicated instances可以互相切换
1. EC2 的spread placement group，一个AZ最多放7个实例

#### 其他
1. metadata的Tags配合IAM可以针对用户区分资源  
1. CloudTrail默认把日志存S3且SSE加密
1. Amazon ElasticCache for Redis 默认没有开启 Redis AUTH
1. CloudFront 使文件失效的最佳实践是使用新路径；刷新CDN缓存需要付费
1. 跨 AZ 的流量也会收费
1. lambda 最长执行时间是15分钟，默认只有1000 qps的并发；没有Caching机制
1. lambda 默认在一个全局的VPC网络，一旦启用VPC，则必须借助NAT Gateway连接外网
1. AWS Organization 能用 Service Control Policy (SCP) 控制子账号的资源，比如ec2的型号
1. CloudFormation 可以为 template 配置 security configuration 保证网络安全
1. CloudFormation StackSets can deploy the same template across AWS accounts and regions
1. ECS 的AmazonECSTaskExecutionRolePolicy是用于agent的（拉取镜像、写日志），taskRoleArn 则是运行时的角色
1. ECS 底层除了EC2还可以用Fargate
1. Route 53 的 geo-location：绝对的地理；geo-proximity：基于地理位置的偏移设置
1. VPC sharing 可以实现同组织的账号间共享子网
1. AWS CloudWatch alarms 可以触发ec2重启、sns、Auto Scaling；要触发lambda需要借助sns
1. Amazon API Gateway 利用令牌桶算法来限制请求数；启用API Gateway Caching可以当缓冲层
1. AWS DMS as a bridge between Amazon S3 and Amazon Kinesis Data Streams
1. IAM 三驾马车：Organization SCP、IAM permission boundaries(不能作用于用户组)、IAM permissions
1. route 53 alias可以设置根域名CNAME不能，alias只能指向AWS的资源或者同zone的其他记录
1. Amazon EventBridge is the only event-based service that integrates directly with third-party SaaS partners. 
