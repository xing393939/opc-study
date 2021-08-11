### TiDB in Action: 最佳实践

#### 1.适用场景介绍
1. 分库分表的缺点：
  * 业务需要提供切分维度
  * 不支持在线 DDL 操作，不能在线进行扩缩容
  * 不能跨维度 Join / 聚合 / 子查询，不支持分布式事务。
  * 业务程序从单机数据库迁移到分库分表方案时，通常要完成大量的开发适配改造。
  * 不能实现一致性的备份还原，难以实现异地容灾等。

#### 2.硬件选型规划
1. TiDB server 组件
  * 整个系统的瓶颈大概率先出现在 tidb-server
  * tidb-server 的 cpu 高一点，数量多一点是一个更好的选择。
1. PD 组件
  * 推荐使用 SSD 磁盘。至少三个节点。单独部署。
1. TiKV 组件
  * 建议你为 TiKV 多分配或预留些资源
  * 实例个数推荐是副本数的倍数
1. 监控组件：8GB 内存、2核 CPU 在大多数情况下已经够用

#### 3.常见性能压测
1. TPC-C 测试模型给基准测试提供了一种统一的测试标准。
1. BenchmarkSQL 内嵌了 TPC-C 测试脚本，可以测试 PostgreSQL、MySQL、Oracle、TIDB 
1. [NewSql的tpcc测试](https://www.jianshu.com/p/769611dd86b7)
  * percona的sysbench-tpcc测试CRDB和TiDB
  * percona的tpcc-mysql可以测试TiDB
  * TiDB的自家方案：改造BenchmarkSQL
  * CRDB的自家方案：自己开发的，也可以用BenchmarkSQL

```
// 新建配置sysbench/tidb_conf
mysql-host=192.168.xxx.xxx
mysql-port=4000
mysql-user=sysbench
mysql-password=******
mysql-db=test
time=30            //总测试时间
threads=4          //线程数
report-interval=10 //10秒出一次报告
db-driver=mysql    //mysql或pgsql

// 测试insert，若--tables=2，表示插入2张表sbtest1、sbtest2，分别插入10000条数据
sysbench --config-file=sysbench/tidb_conf oltp_point_select --tables=1 --table-size=10000 prepare
// 测试select
sysbench --config-file=sysbench/tidb_conf oltp_point_select --tables=1 --table-size=10000 run
// 测试update index
sysbench --config-file=sysbench/tidb_conf oltp_update_index --tables=1 --table-size=10000 run
```

#### 4.跨数据中心方案
1. 两中心方案：
  * 两中心副本数相同：两中心同时对外提供读写
  * 两中心副本数是2:1：一个是主机房，一个是灾备机房
1. 两地三中心：其中两个机房在同城市，一个机房在其他城市
  * 集群1采用两地三中心，分别为北京 IDC1，北京 IDC2，西安 IDC3，是主集群
  * 集群2从集群1通过binlog复制，机房在西安 IDC3，是从集群

#### 5.数据迁移方案

#### 6.业务适配最佳实践
1. 乐观锁的缺点如下：
  * 两阶段提交，网络交互多。
  * 需要一个中心化的版本管理服务。
  * 事务在 commit 之前，数据写在内存里，数据过大内存就会暴涨
1. 减少乐观锁写写冲突
  * 使用TiDB悲观锁, 或者redis分布式锁
  * 使用消息队列时，将同一行的读写分配到同一个队列，这样就会串行写入TiDB
  * 将大事务拆解成多个小事务以减少单个事务的运行时间
1. tidb的一个事务转化到tikv的查询次数：
  * 一次insert：1次数据insert+相关索引insert
  * 一次delete：1次数据delete flag+相关索引delete flag
  * 一次update：1次数据update+相关索引delete flag和insert
1. 雪花算法uid-generator六十四位方案
  * sign：固定为 0，表示生成的 ID 始终为正数。
  * delta seconds：默认 28 位。基于2016-05-20开始的秒数。最多可支持约 8.7 年。
  * worker node id：默认 22 位。从一个集中式的ID生成器取得(Zookeeper)。最多可支持约420万次启动。
  * sequence：默认 13 位。表示每秒的并发序列，13 位可支持每秒 8192 个并发。
1. 批量update的方案：
  * 坏的：set field1=value1 order by id limit 0,1000
  * 好的：set field1=value1 where id between 100000 and 102000（需事先分好范围）
1. SQL 调优案例
  * 大批量Delete。改成分批Delete
  * 统计信息不准导致查询计划不准。修复：analyze table test.t1;
1. TiDB 分区表
  * 主键和唯一索引必须包含分区表达式中用到的所有列
  * Range 分区可以用于解决业务中大量删除带来的性能问题，支持快速删除分区
  * Hash 分区表来一定程度上解决写热点问题
  * 清理分区：ALTER TABLE employees_attendance TRUNCATE PARTITION p20200306;
  * 更新统计信息：ALTER TABLE employees_attendance ANALYZE PARTITION p20200306;
  
#### 7.常见问题处理思路
1. TiKV 只执行过 INSERT 而没有 UPDATE 和 DELETE 的话（不考虑索引的大小）
  * 单节点 10GB 数据最多占据 (512MB + 1GB + 10GB) * 3 的物理空间
  * 每一层的大小是上一层的十倍，所以倒数第一层是 10GB，倒数第二层是 1GB
  * 512MB 为 L0 的 SST 文件大小
1. TiKV 的写入性能周期性下降问题（10～20 分钟一轮）
  * 由 TiKV 的 GC 引起，可以控制 GC 的速度
  * TiKV 的配置 gc.max-write-bytes-per-sec 建议在 128KB ~ 512KB，默认是 0。
1. RocksDB 中被 GC 删除的数据会很快被 compact 到下一层。
1. TiKV 提供 snappy，zlib，bzip2，lz4，lz4hc，zstd 等六种压缩算法。默认为 ["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]
1. 只有当数据量超过 500G 时 RocksDB 的层数才会超过 4。
1. 只有当数据量超过 500G 部分的数据才会启动 ZSTD 压缩算法。

#### 8.TiDB 调优指南
1. TiDB 常见配置优化
  * max_execution_time，执行时间，超过则终止执行
  * tidb_mem_quota_query，一条查询语句的内存使用阈值，超过则记log
  * tidb_retry_limit，事务重试次数，默认是10
  * tidb_disable_txn_auto_retry，禁用事务重试，默认是On
  * tidb_distsql_scan_concurrency，算子的并发个数
1. TiKV 常见配置优化
  * Raftstore 线程性能问题：增加TiKV节点；调高raftstore.store-pool-size；merge region。
1. 创建索引：通过 admin show ddl 命令来查询 RowCount 和 START_TIME 字段
  * START_TIME表示开始执行时间，RowCount表示已经创建的行数，由此可以判断剩余执行时间