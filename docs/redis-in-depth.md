### Redis 深度历险

#### 第1篇 基础和应用篇
* 5种基础的数据类型：string、list、hash、set、zset
* 分布式锁：
  * 加锁的原子操作（设置key、设置过期时间）
  * 释放锁的原子操作（匹配value、判断是否删除）
  * 缺点1：T1执行时间超过了锁的过期时间，T2加锁成功并执行
  * 缺点2：主节点刚加锁key还没有同步到从节点就挂了，并发生主从切换，此时T2加锁成功
* 延迟队列和位图
* HyperLogLog的原理：
  * N个随机整数、低位连续0的最大长度K：N = 2 ^ K
  * 假设只有一个桶来存储，可能因为个别离群值导致误差
  * 假设预置1024个桶，把N个整数分散到这1024个桶，最后对1024个桶求和，可以减少误差
  * redis的HyperLogLog有16384个桶，每个桶用6b存储K值，占用内存：16384 * 6 / 8 = 12K
* BloomFilter：
  * 一个元素的指纹空间如果占8b，错误率约2%，最佳hash数量是8 * 0.7
  * 一个元素的指纹空间如果占15b，错误率约0.1%，最佳hash数量是15 * 0.7
  * 使用时先预置好内存（最大数据容量已确定），若后续数据量超过最大容量，则需要重建BloomFilter
* Redis-Cell：限流模块
* GeoHash：地理位置
* scan：分页扫描时，采用“高位进位加法”，保证了不受扩容缩容的影响而导致漏了key（但可能会重复）

#### 第2篇 原理篇
* 线程IO模型：多路复用I/O模型Linux使用epoll、Unix使用kqueue
* 客户端管道：echo -e "PING\r\nPING\r\nPING\r\n"|nc localhost 6379
* redis事务：redis禁止在multi和exec之间执行watch，必须在multi之前执行watch
* 订阅：subscribe阻塞循环读，读其他线程publish的消息
* 小对象压缩：ziplist和intset

#### 第3篇 集群篇
* 主从模式下的wait {nums} {seconds}：一直阻塞直到nums个从节点同步到最新状态，最多等待seconds
* 哨兵：客户端连接哨兵节点获取master的地址和slaves的地址
* codis的优点：分布式的问题借用的是zookeeper/etcd，因此代码简单

#### 第4篇 扩展篇
* stream不借用消费组：
  * xread读取{nums}条消息，阻塞{seconds}，可以指定从某个消息id后读取
* stream借用消费组：
  * xgroup create {streamName} {groupName}
  * xreadgroup {groupName} {consumerName}
  * xack {streamName} {groupName} {messageID}，这里没有指定consumerName，默认是之前指定的consumerName
* 分布式锁redlock：
  * 大多数机制：向多个节点加锁，大多数加锁成功则为成功
  * 需考虑错误重试、时钟漂移
* 懒惰删除：异步线程删除
  * unlink：删除大key
  * flushdb async
  * AOF sync

#### 第5篇 源码篇
* SDS有两种类型：
  * embeded：容量固定是44个字符串，因为jemalloc默认分配的大小是64B，robj(占19B)和embeded的SDS是内存连续的
  * raw：容量大于44个字符串
* DICT的渐进式reahsh：访问的时候搬迁，定时任务搬迁
* 内存紧凑型：
  * ziplist：prevlen可以是1B或5B，encoding可以是1B、2B、5B
  * intset：length和encoding都是4B
* 快表：ziplist+双向链表，压缩深度如果是1，则首尾的ziplist不压缩，其他都压缩
* 跳表：zadd命令如果key已经存在，先删除再插入
* listpack：{encoding, content, length}，注意计算整型值的时候是小端尾序
  * encoding已经包含了content的长度
  * length表示的是content+encoding的长度，使用varint编码
* lru和lfu：
  * lru：lru字段(3B)存储最后一次访问的秒时间戳，大约194天折返
  * lfu：lru字段分为lastDecrementTime(2B)和logisticCounter(1B)
    * lastDecrementTime存储分时间戳，大约45天折返，只在检查淘汰的时候更新（并衰减logisticCounter）
    * logisticCounter存储访问频次的对数值，每次访问key的时候更新
  
  
  
  