### MySQL 是怎样运行的

#### redo、undo、binlog
|操作|redo|undo|
|---|---|---|
|Tx1 write(x, 1) |x=1   |x=0|
|Tx1 write(x, 2) |x=2   |x=1|
|Tx1 commit      |commit|commit|

```
1.如果只有undo日志，则是undo -> data落盘 -> commit标记
  假如commit标记前，data没有落盘，此时宕机，data数据丢失
  假如data落盘后，commit还没有标记就宕机，undo日志回滚此事务
  因为要求必须在commit标记前让data落盘，所以性能很差
2.如果只有redo日志，则是redo -> commit标记 -> data落盘
  假如commit标记后，data没有落盘，此时宕机，redo日志重放恢复
  假如commit还没有标记，data就落盘了，此时宕机data中会存在提交的数据
  因为要求必须在commit标记后data才能落盘：
    问题1，同一个page只要有一个事务还未提交，则不能落盘，需要大量内存维持这种场景
    问题2，假设需要update大表的全部记录，此时产生大量的脏页且不能落盘
3.undo+redo：undo+redo -> commit标记
  data可以随心所欲的落盘
  undo在commit标记后，还不能删除，因为undo还充当mvcc的历史版本，但是可以删除ReadView链最小事务之后的undo
```

#### 表空间
* 表空间：1个表对应1个表空间
* 段：好比一个师，1个索引有2个段（叶子节点段、非叶子节点段），开始表只有2个段，每加1个索引增加2个段，对应的描述是INODE Entry
* 区：好比一个团，1个区有64个物理连续的页，1MB，对应的描述是XDES Entry
* 碎片区：好比一个独立团，处于FREE、FREE_FRAG、FULL_FRAG状态的区直属于表空间
* 注意点1：如果给每个新表都分配一个区(1MB)太浪费，所以开始的数据页先放在公共的碎片区，当表有32个数据页后，开始分配一个区
* 注意点2：表空间默认只有1个INODE类型的页(最多85个INODE Entry)，不够可以新建，并由SEG_INODES_FULL链表、SEG_INODES_FREE链表维护
* 注意点3：每个段需要维护3个链表，它们的基节点信息在INODE Entry，每个表空间也维护3个链表，它们的基节点信息在File Space Header

#### 独立表空间extent0前3页是固定的
* FSP_HDR：存储256个XDES Entry和File Space Header
* IBUF_BITMAP：Change Buffer
* INODE：存储INODE Entry List

#### 独立表空间extent0第0页的File Space Header
* 表空间的ID
* FREE链表的基节点
* FREE_FRAG链表的基节点
* FULL_FRAG链表的基节点
* Next Unused Segment ID：表空间创建新的段时取值并自增

#### 独立表空间extent256、extent512...前2页是固定的
* XDES：存储256个XDES Entry
* IBUF_BITMAP：Change Buffer

#### 系统表空间extent0前8页是固定的
* FSP_HDR
* IBUF_BITMAP
* INODE
* Insert Buffer Header	存储Insert Buffer的头部信息
* Insert Buffer Root	存储Insert Buffer的根页面
* Transaction System	事务系统的相关信息
* First Rollback Segment	第一个回滚段的页面
* Data Dictionary Header	数据字典头部信息

#### 系统表空间extent0的Data Dictionary Header页
* Max Row ID：隐式row_id列的ID，所有库所有表共享。
* Max Table ID：表的ID，所有库所有表共享。
* Max Index ID：索引的ID，所有库所有表共享。
* Max Space ID：表空间的ID，所有库所有表共享。
* Root of SYS_TABLES clust index：本字段代表SYS_TABLES表聚簇索引的根页面的页号。
* Root of SYS_TABLE_IDS sec index：本字段代表SYS_TABLES表为ID列建立的二级索引的根页面的页号。
* Root of SYS_COLUMNS clust index：本字段代表SYS_COLUMNS表聚簇索引的根页面的页号。
* Root of SYS_INDEXES clust index本字段代表SYS_INDEXES表聚簇索引的根页面的页号。
* Root of SYS_FIELDS clust index：本字段代表SYS_FIELDS表聚簇索引的根页面的页号。

#### 第11章 两表连接
* 内连接：from t1, t2 或 from t1 inner join t2。where 条件会过滤记录
* 左连接：from t1 left join t2 ON ... WHERE ...。where 条件会过滤记录，ON 条件不符合的记录仍然展示。
* 右连接：from t1 left join t2 ON ... WHERE ...。where 条件会过滤记录，ON 条件不符合的记录仍然展示。
* 驱动表的EXPLAIN分析和上文描述一致
* 被驱动表EXPLAIN分析的type列：
  * eq_ref：通过主键或者不能为null的唯一索引
  * ref：通过普通索引等值查询，或者可以为null的唯一索引
  * ref_or_null：where key1='a' or key1 is null。null值都在索引的最左边。
  * range：in查询，><查询，like前缀查询
  * index：不能用索引，但是可以用覆盖索引
  * all：全表扫描
* 从驱动表查到的结果集先放到Join Buffer内(默认256K)，然后再到被驱动表查询

#### 第12章 执行计划的成本计算
* 成本计算依赖的数据：
  * 读取1个页面的成本是1
  * 读取1条记录并检测是否满足条件的成本是0.2
  * table信息：Rows表示记录数，Data_length表示聚簇索引占用的字节
  * index信息：Cardinality表示不重复的记录数
* IN查询估算记录数：
  * eq_range_index_dive_limit限制内：使用index dive，基于索引来计算
  * eq_range_index_dive_limit限制外：使用index信息，IN查询的每个元素对应的记录数 = Rows / Cardinality
* 步骤1：找出所有可能使用的索引
* 步骤2：计算全表扫描的代价
  * I/O成本：Data_length / 16KB * 1
  * CPU成本：Rows * 0.2
* 步骤3：计算使用索引uk_key2的代价
  * 访问二级索引I/O成本：因为只有一个扫描区间，所以是1
  * 访问二级索引CPU成本：根据扫描区间的边界估算出记录数=95，所以是95 * 0.2
  * 访问聚簇索引I/O成本：每次回表都算读取1个页面，所以是95 * 1
  * 访问聚簇索引CPU成本：95 * 0.2
* 步骤4：计算使用索引idx_key1的代价
  * 访问二级索引I/O成本：因为有三个单点区间，所以是3
  * 访问二级索引CPU成本：估算出记录数=118，所以是118 * 0.2
  * 访问聚簇索引I/O成本：118 * 1
  * 访问聚簇索引CPU成本：118 * 0.2
* 步骤5：选出代价最低的方案

#### 第13章 InnoDB的统计数据
* mysql.innodb_table_stats：n_rows总记录数、cluster_index_size聚簇索引页面数、sum_of_other_index_sizes其他索引页面数
  * 统计碎片区的页面数：INODE Entry存储有对应的页号
  * 统计叶子节点段和非叶子节点段的页面数：INODE Entry存储有FREE、NOT_FULL、FULL链表的基节点，据此计算页面数
* mysql.innodb_index_stats：size索引页面数、n_leaf_pages叶子节点页面数、n_diff_pfxxx不重复的记录数
* 统计数据如何更新：开启了自动更新后，数据每增长10%就算一次，根据配置的采样数采样统计
* 统计数据可以保存在内存或者磁盘，新版本都是在磁盘
* innodb_stats_method配置：计算不重复的记录数时，每个null值都是重复值、每个null值都不同、忽略null值

#### 第14章 子查询优化
* 子查询一般会出现在3个位置：
  * select子句：select (select m2 from t2 limit 1)
  * from子句：from (select m2 from t2) as tt
  * on/where子句
* 子查询按照返回的结果分类：
  * 标量子查询：where m1 = (select m2 from t2 limit 1)
  * 行子查询：where (m1, n1) = (select m2, n2 from t2 limit 1)
  * 列子查询：where m1 in (select m2 from t2)
  * 表子查询：where (m1, n1) = (select m2, n2 from t2)
* 子查询按照与外层查询的关系分类：
  * 不相关子查询：不依赖外层查询的值，上述SQL都是
  * 相关子查询：where t1.m1 in (select t2.m2 from t2 where t2.n2 = t1.n1)
* 能转换成半连接的IN查询的条件：
  * 不能是NOT IN
  * 外层查询的其他搜索条件必须是AND，不能是OR
  * 子查询必须是单一的查询，不能是由UNION连接起来的查询
  * 子查询不能包含GROUP BY、HAVING语句或者聚集函数如MAX/MIN/COUNT/AVG/SUM
* IN查询的查询策略：
  * 能转换成半连接的IN查询则按半连接的5种查询策略估算成本
  * 能转换成EXISTS查询则先转换，转换成EXISTS也许能用到索引：
    * 原始的：where key1 in (select key3 from s2 where common_field='a') or key2 > 1
    * 转换后：where exists (select 1 from s2 where s2.common_field='a' and s2.key3=s1.key1) or key2 > 1
    * 转换后的子查询，可以用到s2.key3的索引
  * 都不能，则先把子查询变成物化表，再进行连接查询
    * 子查询是不相关子查询：物化后子查询只执行一遍
    * 子查询是相关子查询：物化后子查询可能执行多遍
* IN查询原始SQL：select * from s1 where xxx in (select key1 from s2 where s2.xxx)
* IN查询半连接：select s1.* from s1 JOIN s2 ON s1.xxx = s2.key1 where s2.xxx 
* IN查询半连接的5种查询策略，估算并选择成本最低的策略执行查询：
  * Table Pollout：上述转换成半连接的SQL，如果s2.key1是主键或者唯一索引，则按内连接来查询即可
  * Duplicate Weedout：如果s2.key1不是主键或者唯一索引，在回表之前，还需要对主键记录去重
  * LooseScan：s2是驱动表并且s2正好用到了key1这个普通索引，可以在索引上跳过重复的key1值，再去被驱动表查询
  * Semi-join Materialization：先把子查询变成物化表，再进行连接查询
  * FirstMatch：对于关联子查询，依次取外层查询的一条记录，到子查询里FirstMatch，匹配到则放入结果集

#### 第15章 EXPLAIN详解

```
CREATE TABLE single_table (
    id INT NOT NULL AUTO_INCREMENT,
    key1 VARCHAR(100),
    key2 INT,
    key3 VARCHAR(100),
    key_part1 VARCHAR(100),
    key_part2 VARCHAR(100),
    key_part3 VARCHAR(100),
    common_field VARCHAR(100),
    PRIMARY KEY (id),
    KEY idx_key1 (key1),
    UNIQUE KEY idx_key2 (key2),
    KEY idx_key3 (key3),
    KEY idx_key_part(key_part1, key_part2, key_part3)
) Engine=InnoDB CHARSET=utf8;
create table s1 like single_table;
create table s2 like single_table;
DELIMITER //
create procedure insert_table(in max int(10))
begin
declare i int default 0;
repeat
set i=i+1;
insert into s1 values(NULL,i%100,i,i%10,i,MD5(i),RAND(),i);
insert into s2 values(NULL,i%100,i,i%10,i,MD5(i),RAND(),i);
insert into single_table values(NULL,i%100,i,i%10,i,MD5(i),RAND(),i);
until i=max end repeat;
end//
call insert_table(5000);

1. select_type: 
* SIMPLE: EXPLAIN SELECT * FROM s1 INNER JOIN s2; // 不包含union或者子查询
* PRIMARY: EXPLAIN SELECT * FROM s1 UNION SELECT * FROM s2; // 包含union，最左边的table
* UNION: EXPLAIN SELECT * FROM s1 UNION SELECT * FROM s2; // 包含union，除了最左边的table，其他都是UNION
* UNION RESULT: EXPLAIN SELECT * FROM s1 UNION SELECT * FROM s2; // 使用了临时表来完成去重
* SUBQUERY: EXPLAIN SELECT * FROM s1 WHERE key1 IN (SELECT key1 FROM s2) OR key3 = 'a'; // 子查询不能转成半连接&&决定采用子查询物化的方案
* DEPENDENT SUBQUERY: EXPLAIN SELECT * FROM s1 WHERE key1 IN (SELECT key1 FROM s2 WHERE s1.key2 = s2.key2) OR key3 = 'a'; // 子查询不能转成半连接&&决定采用子查询物化的方案
* DERIVED: EXPLAIN SELECT * FROM (select count(*) from s1 group by key1) as s; // 包含派生表，决定采用派生表物化的方案
* MATERIALIZED : EXPLAIN SELECT * FROM s1 WHERE key1 IN (SELECT key1 FROM s2); // 包含子查询，决定采用子查询物化的方案

2. type
* const: EXPLAIN SELECT * FROM s1 WHERE id = 5; // 主键或者唯一索引（唯一索引可以有多个null值，所以查null值不算）
* eq_ref: EXPLAIN SELECT * FROM s1 INNER JOIN s2 ON s1.id = s2.id; // 连接查询、主键或者不为null的唯一索引
* ref: EXPLAIN SELECT * FROM s1 WHERE key1 = 'a'; // 通过普通索引等值查询，或者唯一索引查null值
* ref_or_null: EXPLAIN SELECT * FROM s1 WHERE key1 = 'a' OR key1 IS NULL; // null值都在索引的最左边。
* unique_subquery: EXPLAIN SELECT * FROM s1 WHERE key2 IN (SELECT id FROM s2 where s1.key1 = s2.key1) OR key3 = 'a'; // IN查询转EXISTS，可用主键或者不为null的唯一索引
* index_subquery: EXPLAIN SELECT * FROM s1 WHERE key2 IN (SELECT key3 FROM s2 where s1.key1 = s2.key1) OR key3 = 'a'; // IN查询转EXISTS，可用普通索引
* range: EXPLAIN SELECT * FROM s1 WHERE key1 IN ('a', 'b', 'c'); // in查询，><查询，like前缀查询
* index: EXPLAIN SELECT key_part2 FROM s1 WHERE key_part3 = 'a'; // 覆盖索引，但是需要扫描全部索引
* all: EXPLAIN SELECT * FROM s1; // 全表扫描
* index_merge：如果2个索引各自取到的索引记录是按照主键排序的，则同时使用这2个索引：
  * 取交集：where key1='1' and key3='3'
  * 取并集：where key1='1' or key3='3'
  * 先排序再取并集：where key1<'1' or key3>'3'（虽然各自的记录不是按照主键排序，但是记录数不多）

3. key_len:
* int4字节、bigint8字节
* char和varchar：假设字符数是n，utf8就是3n，utf8mb4就是4n；允许null值就是3n+1；变长类型就是3n+2

4. ref(type属于const/eq_ref/ref/ref_or_null/unique_subquery/index_subquery时)
* const: EXPLAIN SELECT * FROM s1 WHERE key1 = 'a';
* s1.id: EXPLAIN SELECT * FROM s1 INNER JOIN s2 ON s2.id = s1.id;
* func: EXPLAIN SELECT * FROM s1 INNER JOIN s2 ON s2.key1 = UPPER(s1.key1);

5. rows(全表扫描或者扫描索引，扫描的行数)
* EXPLAIN SELECT * FROM s1 WHERE key1 > 'z'; // 满足key1 > 'z'的条数有266

6. filtered
* EXPLAIN SELECT * FROM s1 WHERE key1 > 'z' AND common_field = 'a'; // 266条记录有filtered%比例的记录满足common_field = 'a'
* EXPLAIN SELECT * FROM s1 INNER JOIN s2 ON s1.key1 = s2.key1 WHERE s1.common_field = 'a'; // 驱动表s1的rows=9688，filtered=10，说明被驱动表要查询约968次

7. Extra
* No tables used: EXPLAIN SELECT 1;
* Impossible WHERE: EXPLAIN SELECT * FROM s1 WHERE 1 != 1;
* No matching min/max row: EXPLAIN SELECT MIN(key1) FROM s1 WHERE key1 = 'abcdefg';
* Using index: EXPLAIN SELECT key1 FROM s1 WHERE key1 = 'a'; // 可用使用覆盖索引
* Using index condition: EXPLAIN SELECT * FROM s1 WHERE key1 > 'z' AND key1 LIKE '%a'; // 使用了索引下推
* Using where: 当搜索条件需要在Server层判断时
* Using join buffer (Block Nested Loop): EXPLAIN SELECT * FROM s1 INNER JOIN s2 ON s1.common_field = s2.common_field; // 不能用索引访问被驱动表时，利用Join Buffer提速
* Using intersect: EXPLAIN SELECT * FROM s1 WHERE key1 = '1' AND key3 = '1';
* Using union: EXPLAIN SELECT * FROM s1 WHERE key1 = '1' OR key3 = '1';
* Using sort_union: EXPLAIN SELECT * FROM s1 WHERE key1 < '1' OR key3 > '99'; // 先把主键排序再合并，再回表
* Using filesort: order by语句不能用到索引时，使用内存排序或者硬盘排序
* Using temporary: 包含DISTINCT、GROUP BY、UNION的子查询，需要借助临时表完成去重、排序等等
* Start temporary, End temporary: explain select * from s1 where key2 in (select key1 from s2 where key3 > '1'); // 半连接策略2，需要临时表来去重
* LooseScan: 半连接策略3
* FirstMatc: EXPLAIN SELECT * FROM s1 WHERE common_field IN (SELECT key1 FROM s2 where s1.key3 = s2.key3); // 半连接策略5
```

#### 第16章 使用optimizer trace查询优化器具体工作
* SET optimizer_trace="enabled=on";
* 执行SQL
* SELECT * FROM information_schema.OPTIMIZER_TRACE;
* 单表查询优化器具体工作：
  * steps\[4].rows_estimation.\[0].range_analysis.table_scan：全表扫描的成本
  * steps\[4].rows_estimation.\[0].range_analysis.potential_range_indexes：可能使用到的索引
  * steps\[4].rows_estimation.\[0].range_analysis.analyzing_range_alternatives：可能使用到的索引的成本
  * steps\[4].rows_estimation.\[0].range_analysis.chosen_range_access_summary：最优方案总结
  
#### 第17章 InnoDB的Buffer Pool
* show VARIABLES like 'innodb_buffer_pool_%'
  * innodb_buffer_pool_size：Buffer Pool的总大小
  * innodb_buffer_pool_instances：Buffer Pool的实例数
  * innodb_buffer_pool_chunk_size：Buffer Pool的每个实例下每个chunk的大小
* Buffer Pool在Mysql启动时已经申请好了，用于缓存从硬盘读到的页：
  * free链表，管理Buffer Pool未使用的页
  * flush链表，管理Buffer Pool已使用的、被修改的页
  * lru链表，主要用于淘汰已使用的、但是最近最少使用的页

#### 第18章 事务
* 事务的四个特性：
  * 原子性：强调要么不做，要么都做
  * 隔离性：强调事务之间不能互相影响，如果操作同一个数据，有四个隔离级别
  * 一致性：强调同一时刻，大家看到的数据一致
  * 持久性：强调数据不能丢失

#### 第19章 redo日志
* redo日志的每个block大小是512KB，有三个部分
  * log block header
  * log block body：存放redo记录
    * type：类型
    * space ID：表空间ID
    * page number：页号
    * data：redo内容
  * log block trailer
* 一个事务可有多个SQL语句，一个SQL语句可有多个MTR，一个MTR可有多个redo记录
  * 写入log buffer时：MTR作为一个不可分割的整体写入
  * 崩溃恢复时：MTR作为一个不可分割的整体来处理
* redo日志log buffer刷盘时机
  * log buffer空间不足（默认16MB）
  * 事务提交（innodb_flush_log_at_trx_commit），=0异步刷，=1立即刷，=2写入os层
  * 刷脏页时
  * 后台线程，定时每秒刷一次
  * 正常关闭mysql server
  * 做checkpoint时
* lsn：log sequence number，起始值是8707，写了多少字节的日志，就自增多少  
* redo硬盘日志前四个block记录了一些全局信息：
  * LOG_CHECKPOINT_LSN：最后一次checkpoint的lsn，崩溃恢复从这个lsn开始
* flush链表的lsn：
  * 链表的每个节点都有2个属性，存储节点对应的页的最老lsn和最新lsn
  * 当MTR写入log buffer时，会更新flush链表，同时更新上述2个属性
  * 系统定时做checkpoint，即获取链表所有节点中最老的lsn，并更新LOG_CHECKPOINT_LSN
* 崩溃恢复的过程：
  * 确定lsn起始点，lsn有三个关键的全局变量（这里取LOG_CHECKPOINT_LSN）：
    * lsn：表示log buffer的最新lsn
    * flushed_to_disk_lsn: 表示log buffer已经刷盘的最新lsn
    * LOG_CHECKPOINT_LSN: 表示log buffer已经刷盘的、对应的脏页也刷盘的最新lsn
  * 为了加快恢复速度，同一页的redo日志放一起执行
  * 为了加快恢复速度，对于已经刷盘的页不作处理

#### 第20章 undo日志
* 系统表空间的第5页Transaction System：存储了128个回滚段页的地址，8B（表空间id+页号）
  * 每个回滚段页有1024个undo slot，4B（undo链表第一页的页号）
    * undo链表第一页比其他undo页多了一个结构：Undo Segment Header
    * undo链表第一页Undo Segment Header的TRX_UNDO_STATE属性：
      * TRX_UNDO_ACTIVE：已有事务在使用
      * TRX_UNDO_CACHED：该链表可以重用
      * TRX_UNDO_TO_FREE：该链表不能被重用
      * TRX_UNDO_TO_PURGE：该链表不能被重用
    * undo链表第一页Undo Segment Header的TRX_UNDO_LAST_LOG属性：链表最后一个Undo Log Header的位置
* 一个事务分配undo链表的过程：
  * 启动新事务后，找到系统表空间的第5页的128个回滚段页的地址，循环取出一个
  * 找到回滚段页的1024个undo slot，寻找TRX_UNDO_CACHED状态的undo链表
  * 没有，则寻找一个未被使用的undo slot，创建一个新的回滚段，同时标记undo slot
  * 仍然没有，报错
* 一个事务最多分配4个Undo链表（即4个回滚段）：
  * 针对普通表的insert undo链表
  * 针对普通表的update undo链表
  * 针对临时表的insert undo链表
  * 针对临时表的update undo链表
* 事务提交后的处理过程：
  * 若undo链表可以被重用（只使用了1页且不到3/4），标记为TRX_UNDO_CACHED
  * 若undo链表不能被重用：
    * 针对insert undo链表标记为TRX_UNDO_TO_FREE，随后链表被释放，并把undo slot标记为可用
    * 针对update undo链表标记为TRX_UNDO_TO_PURGE，随后undo页挂到history链表，并把undo slot标记为可用
* 崩溃恢复的处理过程：
  * 找到系统表空间的第5页的128个回滚段页的地址
  * 找到每个回滚段页的1024个undo slot
  * 若undo slot对应的undo链表第一页的状态是TRX_UNDO_ACTIVE，则说明事务还未提交就意外终止了
  * 根据此undo链表第一页的TRX_UNDO_LAST_LOG属性，找到最后一个undo记录，执行回滚。

#### 第21章 MVCC
* 事务的四大特性：原子性、隔离性、持久性、一致性
* 事务的四个问题：脏写、脏读、不可重复读、幻读
* SQL的四个级别：读未提交、读提交、可重复读、可串行化。（一定不会出现脏写）
* mvcc两个知识点：
  * 二级索引的delete是mark delete；update是mark delete并insert，[参考](https://www.zhihu.com/question/27674363/answer/38034982)
  * name字段无索引，事务1查询name='1'，事务2修改成name='2'并提交，事务1仍然能搜到name='1'，说明全表扫描时还需要扫描undo版本链。
* mvcc读提交级别：解决了脏读（事务内每次select都是一个新的ReadView）
* mvcc可重复读级别：解决了不可重复读（事务内每次select都同一个ReadView）
* mvcc解决了部分幻读：
  * 事务1根据条件查询出N条记录，事务2执行写操作，事务1再次查询查询出的记录不是N条
* mvcc没有解决的幻读：
  * 事务1先查询id=1的记录为空，事务2执行写操作，事务1执行insert id=1失败或者update id=1成功
  * 事务1先查询id=1的记录非空，事务2执行写操作，事务1执行insert id=1成功或者update id=1失败
* undo日志的回收过程：
  * 在生成ReadView时，它的事务no等于当前系统中最大的事务no+1
  * 在事务提交时，事务对应的一组undo日志的事务no等于当前系统中最大的事务no
  * 由于history链表是按照事务提交的顺序排列undo日志的，所以是按照事务no排序的
  * ReadView按照创建时间连成了链表
  * 后台线程执行purge时，先取ReadView链表最小的那个事务no（ReadView已提交）
  * 每个回滚段有一个history链表，对比上一步的事务no，清理比它小的undo日志
  * （如果undo日志是delete类型，把对应的数据记录也删除掉）

#### 第22章 锁
* 一致性读：利用mvcc的方式读
* 锁定读：在读取记录前加锁，S锁是lock in share mode，X锁是for update
* IS锁和IX锁：属于表级锁，仅仅是为了快速判断表内是否有行级锁
* InnoDB的五个行级锁：
  * Record Lock：只对记录本身加锁
  * Gap Lock：锁间隙
  * Next-Key Lock：锁记录和间隙
  * Insert Intention Lock：insert时碰到间隙锁而生成的锁
  * 隐式锁：insert语句，其他事务想要在它的记录上加锁，需要先给此事务生成锁，再生成意向锁
* 可串行化级别下：
  * autocommit=0，普通的select也会变成锁定读，从而保证了不会出现幻读
  * autocommit=1，因为只有一条select，不存在不可重复读和幻读，所以不需要锁定读

