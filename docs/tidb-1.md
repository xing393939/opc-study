### TiDB 基础知识

#### 基础知识
1. [TiDB 系统管理基础 - 视频](https://learn.pingcap.com/learner/course/30002)
1. [18年的压测](https://www.quora.com/How-does-TiDB-compare-with-MySQL)和[19年的压测](https://www.percona.com/blog/2019/01/24/a-quick-look-into-tidb-performance-on-a-single-server/)表明：TiDB的性能只有MySQL的一半
1. [新一代数据库TiDB在美团的实践](https://tech.meituan.com/2018/11/22/mysql-pingcap-practice.html)
  * 美团对TiDB的定位：支持二级索引；跨region failover；跨region双写
  * TiDB对比ClickHouse：ClickHouse跑低频SQL可以，跑高频SQL不行，且跑全量低频SQL会发生overkill；TiDB则可以胜任。
  * 传统分库分表方案的弊端：业务无法友好的执行分布式事务；跨库的查询需要在中间层上组合(不支持跨库join)；再次拆分的成本高
1. [CatKang - NewSQL数据库概述](http://catkang.github.io/2020/12/01/newsql.html)
  * 分库分表：part1是中间件，part2是单机。代表有阿里云DRDS。
  * Spanner：part1是server层，part2是engine层。代表有TiDB、OceanBase。分布式事务的四个特性：
    * Atomicity：单机靠redo+undo；分布式靠redo+undo+2PC
    * Consistency
    * Isolation：单机靠2PL+MVCC(本地时钟)；分布式靠2PL+MVCC(Lamport or TrueTime时钟)
    * Durability：单机靠redo；分布式靠redo+Multi-Paxos
  * Partition Storage：part1是server、engine层，part2是存储。代表有Aurora、PolarDB。

```
// undo 的流程
日志1记录t=0，数据t=1，标记*
日志2记录t=1，数据t=2
日志3记录t=2，数据t=3，标记*
日志4记录t=3，数据t=4
标记为*后表示事务已提交，此时日志1和日志3可以删除
数据恢复时，只需要恢复日志4和日志2即可

// redo的流程
日志1记录t=1，标记为*，数据t=1
日志2记录t=2
日志3记录t=3，标记为*
日志4记录t=4
标记为*后表示事务已提交，此时需要等数据落盘后才能删除，日志1可以删除，日志3不能
数据恢复时，只需要恢复标记为*日志即可
```

#### 热点问题处理思路
1. [TiDB 最佳实践系列（一）高并发写入常见热点问题及规避方法](https://pingcap.com/blog-cn/tidb-in-high-concurrency-scenarios/)
  * 高并发批量插入会有region热点问题，可以通过预先split region解决
1. [7.2 热点问题处理思路 · TiDB in Action](https://book.tidb.io/session4/chapter7/hotspot-resolved.html)
1. 确认热点问题：Grafana 的 TiKV-Trouble-Shooting 的 Dashboard 的 Hot Read 和 Hot Write 面板
1. 确认热点表或索引：pd-ctl region topwrite|topread 3；TiDB Dashboard的流量可视化。
1. 写入热点的业务场景通常有：
  * 有自增主键：去掉自增主键并设置 SHARD_ROW_ID_BITS（可动态设置，SHARD_ROW_ID_BITS=4表示16个分片）。
  * 存在递增索引，比如时间索引等：手工切分热点 Region。
  * 高并发更新小表：改造小表为 hash 分区表。
  * 秒杀场景下的单行热点问题：业务层面用内存缓存解决。

#### TiKV 架构
1. [TiKV 简介 | PingCAP Docs](https://docs.pingcap.com/zh/tidb/stable/tikv-overview)
1. [RocksDB 简介 | PingCAP Docs](https://docs.pingcap.com/zh/tidb/stable/rocksdb-overview)
1. Region 副本(Peer)的三个角色：Leader负责读写可投票；Follower可随时替换Leader可投票；Learner是不完整的副本，不可投票。
1. 每个 TiKV 实例中有两个 RocksDB 实例
  * 一个用于存储 Raft 日志（通常被称为 raftdb）
  * 一个用于存储用户数据以及 MVCC 信息（通常被称为 kvdb）

#### TiDB Cluster 部署
* 安装：pd是大脑（3台）、tidb是无状态的server（2台）、tikv（3台，默认3个副本）
* 安装：需先安装numactl。tiup cluster template > topology.yaml，去掉TiFlash配置

#### 考试大纲
* TiDB 数据库体系架构	
  * 分布式数据库原理
  * 分布式 SQL 引擎：不支持MySQL的存储过程与函数、触发器、事件、外键
  * 分布式存储系统
  * 基于分布式架构的 HTAP 数据库
  * TiDB 典型应用场景及用户案例
* TiDB 集群管理	
  * TiDB Cluster 部署：tiflash的扩容和缩容略有不同
  * TiDB 的连接管理：MyCli也可以连接
  * TiDB 的配置：
    1. 集群配置（tidb、tikv、pd，需修改配置文件并重启）
    1. 系统配置（存在tikv中，有作用域，session只对当前会话生效，global对新启的会话生效）
  * 用户管理与安全：mysql分用户和角色，attach角色后，用户登录需要执行set role all
  * TiDB 文件与日志管理：tikv和pd有日志和数据、tidb只有日志
  * TiDB 的监控：pd内置Dashboard，Prometheus内置Alert-manager
  * TiDB Cluster的升级：升级TiUP->升级TiUP Cluster->检查集群状态->升级TiDB Cluster
* TiDB 备份恢复	
  * 备份恢复策略
    1. 热备不会锁定如何的读写操作
  * 适用备份恢复工具 BR 进行备份恢复
    1. br是热备、物理备份。不需要额外安装组件。
    1. br可增量备份，指定参数--lastbackupts将备份last_backup_ts到current_ts之间的数据。
    1. br backup all命令把数据备份在各个tikv节点的硬盘下。
    1. br restore all需要各个tikv的硬盘下有全量的备份文件。
* TiDB 数据迁移	
  * 数据导出工具 Dumpling
    1. Dumpling是热备、逻辑备份。不需要额外安装组件。不能增量备份。
    1. 指定参数--consistency snapshot：按照指定的ts导出（ts由--snapshot参数指定）
    1. 指定参数--consistency flush：适合备份MySQL，会短暂的中断DML和DDL操作
    1. Lightning是对应的还原命令
  * 数据导入工具 TiDB Lightning
    1. 不需要额外安装组件。
  * 数据迁移工具 TiDB Data Migration
    1. 需要安装DM集群：包含DM-master、DM-worker组件。
    1. DM可以配置多个源库，把分库分表汇聚到一个TiDB中。
    1. Block/Allow Table Lists 用于过滤库/表的所有操作
    1. Binlog event filter 用于过滤特定表的特定操作
    1. Table routing 指定源库和目标库的对应关系
* TiDB 数据同步与复制	
  * 数据同步工具 TiDB Binlog（已废弃，请使用TiCDC）
    1. 需要在TiDB集群中增加组件：pump（收集binlog），drainer（归并pump的binlog）
  * 数据同步工具 TiCDC
    1. 需要在TiDB集群中增加组件：cdc_server
    1. CDC是基于tikv的change log来实现同步的
    1. CDC的目标库可以是TiDB、MySQL、Kafaka



