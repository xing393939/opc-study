### TiDB in Action: 故障排查

#### 1.SQL 调优原理
1. EXPLAIN：执行计划由一系列的算子构成。
  * id：后缀带Build总是先于Probe执行
  * estRows：估算的输出条数
  * task：有两种，root在tidb执行，cop在tikv上并发执行
  * access object：算子所访问的数据项，如table、partition、index
  * operator info：算子的其它信息
1. EXPLAIN ANALYZE：真实执行SQL，和执行计划一并返回出来，可以视为EXPLAIN语句的扩展
  * actRows：真实的输出条数
  * execution info：time:总时间, loops:此算子循环了几次
1. 算子读盘或者读TiKV：
  * TableFullScan：这是大家所熟知的 “全表扫” 操作
  * TableRangeScan：带有范围的表数据扫描操作，通常扫描的数据量不大
  * TableRowIDScan：根据上层传递下来的 RowID 精确的扫描表数据的算子
  * IndexFullScan：另一种 “全表扫”，只不过这里扫的是索引数据，不是表数据
  * IndexRangeScan：带有范围的索引数据扫描操作，通常扫描的数据量不大
1. 算子读TiDB：
  * TableReader：汇总 TiKV 上底层扫表算子是 TableFullScan 或 TableRangeScan 的算子。
  * IndexReader：汇总 TiKV 上底层扫表算子是 IndexFullScan 或 IndexRangeScan 的算子。
  * IndexLookUp：先汇总Build端TiKV扫描上来的RowID，再去Probe端上根据RowID取TiKV。Build端是IndexFullScan、IndexRangeScan，Probe端是TableRowIDScan。
  * IndexMerge：和IndexLookup类似，不过支持多个build和Probe
1. 3 种最基本的算子：
  * Selection： 代表了相应的过滤条件，select * from t where a = 5 中的 where a = 5。
  * Projection：投影操作，也用于表达式计算， select c, a + b from t 里面的 c 和 a + b就是投影和表达式计算操作。
  * Join：两个表的连接操作
  
#### 2.TiDB Dashboard
1. 流量可视化：查看热点region
1. SQL 语句分析：查看所有的sql语句的平均执行时间，平均影响行数，执行次数
1. 生成集群诊断报告
1. 日志搜索：搜索集群的系统日志

#### 3.诊断系统表
1. 集群信息表：select type, instance, status_address, uptime from information_schema.cluster_info;
1. 慢查询：select query_time, SUBSTR(query,1,50) from information_schema.slow_query
1. 当前的会话：SHOW FULL PROCESSLIST;
1. Statement Summary 系统表，对同类SQL进行汇总
  * Statement Summary Tables 是内存表
  * tidb_enable_stmt_summary：打开或关闭该功能
  * tidb_stmt_summary_refresh_interval：监控指标的刷新周期
  * tidb_stmt_summary_history_size：历史表保存的历史数量
  * max-stmt-count：保存的 SQL 的种类数量
  * max-sql-length：显示的 SQL 的最大长度
  
#### 4.TiDB 集群监控与报警
* Prometheus主动pull数据，在Grafana展示，用Alertmanager报警
* TiDB层：
  * token-limit配置控制并发的session数量，建议小于500，且99.9%的请求小于0.5秒
  * Get Token Duration 需小于2纳秒
  * Parse SQL to AST 需小于10毫秒
  * AST to Physical Execution Plan 需小于30毫秒
  * tidb_max_chunk_size配置控制一次函数调用返回的数据条数，默认1000
  * 生成的物理执行计划会在【Executor模块】中进行执行
    * 如果是DML语句，先缓存在【Transaction模块】，等待事务提交时进行2PC提交
    * 如果是复杂查询，则需通过【DistSQL模块】并发查多个region
    * tidb_distsql_scan_currency配置控制每次并发查多少个region，默认15
  * Get TSO from PD 需小于30毫秒，为了减少PD的压力，TiDB通过单个线程一次为多个事务分配时间
* TiKV主要由5个模块构成
  * gRPC 是所有请求的入口，写事务给scheduler线程，读事务给unified-readpool
  * scheduler 检测冲突，将复杂的事务转换为简单的kv插入、删除，发送给raftstore线程
  * raftstore 将raft日志复制给多个副本，当日志在多个副本上达成一致后，会发送给apply线程
  * apply 将scheduler线程的kv操作写入RocksDB，通知gRPC线程返回结果给客户端
  * unified-readpool 处理single get、batch get等简单的查询请求
* RocksDB 的三种基本文件格式
  * Memtable 内存文件系统，新数据会被写进Memtable
  * WAL Write Ahead Log 写操作先写入logfile，再写入Memtable
  * SST 在Memtable写满以后，将数据写入磁盘中的SST文件，对应logfile里的log会被安全删除。
* RocksDB 查询流程：先在Memtable内存查找，SST先用布隆过滤器查

#### 5.灾难快速恢复
1. 执行了错误的更新、删除操作【利用 GC 快照读恢复数据】
  * MVCC 当更新/删除数据时，不会做真正的数据删除，只会添加一个新版本数据，并以时间戳来区分版本，后台GC清理久远版本
  * tikv_gc_life_time 默认是10m，即能恢复最近10分钟内的数据，也改成24h
1. 执行了drop或truncate，【Recover/Flashback 命令秒恢复误删表】
  * 在gc时间内，直接执行recover table
  * flashback table不仅支持drop操作，还支持truncate操作
1. 多数副本不可用【多数副本丢失数据恢复指南】
  * Region至少还有1个副本：移除故障节点的peer，让Region重新选举和补充副本
  * Region所有副本都丢失了：创建1个空Region来解决Region不可用的问题
  * 丢失数据处理：检查数据的一致性






  