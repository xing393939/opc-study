### Redis 5设计与源码分析（我分析的源码是redis 2.9）

#### 第9章 命令处理周期
* 一个数据库有16个redisDb
  * redisDb的key只能是字符串，value是robj(redisObject)结构体
    * robj的type、encode对应的map定义在redis.h的182行
* 客户端结构体redisClient
* 服务的结构体redisServer
  * redisServer.commands由populateCommandTable方法初始化（把redisCommandTable数组变成dict）
* 程序运行流程之server初始化：
  * initServerConfig：初始化配置
  * loadServerConfig：加载并解析配置文件
  * initServer：初始化服务端内部变量（支持的客户端数量4064）
  * aeCreateEventLoop：创建事件循环eventLoop（每个客户端一个aeFileEvent、一个aeFiredEvent）
    * aeFileEvent：文件事件
    * aeFiredEvent：已就绪的文件事件
    * 其中aeApiCreate()调用epoll_create创建了epoll
* 程序运行流程之启动监听：
  * listenToPort：创建socket并启动监听（IO多路复用模式，socket读写必须是非阻塞的）
  * aeCreateFileEvent：创建文件事件（即socket事件），处理函数是acceptTcpHandler
  * aeCreateTimeEvent：创建时间事件（全局只有1个），处理函数是serverCron
  * aeMain：开启事件循环，死循环执行aeProcessEvents()，它的功能如下：
    * 调用epoll_wait阻塞等待文件事件的方式（设有超时）
    * epoll_wait返回时，先处理触发的文件事件，再处理事件事件
    * aeCreateFileEvent的文件事件是监听新连接，acceptTcpHandler调用createClient生成新的文件事件
    * 新的文件事件处理函数是readQueryFromClient
* 程序运行流程之命令处理过程：
  * processInputBuffer：命令解析，解析结果放在redisClient的argc、argv
  * processCommand：
    * 如果是quit命令直接addReply并关闭客户端
    * 如果lookupCommand找不到命令则addReplyErrorFormat，否则赋值redisClient的cmd
    * 如果命令参数不合法则addReplyErrorFormat
    * 如果需要auth认证单认证没有通过则addReply
    * 如果maxmemory目录设置的内存超过限制则addReply
    * 其他。。。
  * 返回结果：
    * 状态回复：addReply
    * 错误回复：addReplyErrorFormat
    * 整数回复：addReply
    * 批量回复：多次addReplyMultiBulkLen和addReply
  * 发送到客户端：
    * 先写到输出缓冲区c->buf：_addReplyToBuffer()
    * 如果不为空则写入输出链表c->reply：
      * _addReplyObjectToList
      * _addReplySdsToList
      * _addReplyStringToList
    * 把客户端加入到redisServer->clients_pending_write
    * aeMain中的beforeSleep遍历clients_pending_write，并执行writeToClient
      * 如果writeToClient一次性没有发送完，则创建可写事件
      * 当可写事件触发后继续发送
      
```
typedef struct redisDb {
    int id;                    // 数据库号码，一般是0~15    
    dict *dict;                // 数据库键空间，保存着数据库中的所有键值对
    dict *expires;             // 键的过期时间，字典的键为键，字典的值为过期事件 UNIX 时间戳   
    dict *blocking_keys;       /* Keys with clients waiting for data (BLPOP) */
    dict *ready_keys;          /* 可以解除阻塞的键，Blocked keys that received a PUSH */   
    dict *watched_keys;        // 正在被 WATCH 命令监视的键
    long long avg_ttl;         // 数据库的键的平均 TTL ，统计信息
} redisDb;
typedef struct redisObject {
    unsigned type:4;     // 类型：0字符串 1list 2set 3zset 4hash
    unsigned encoding:4; // 编码：0sds 1int 2dict 4linkedList 5ziplist 6intset 7skiplist 8sds
    unsigned lru:24;     // 对象最后一次被访问的时间
    int refcount;        // 引用计数
    void *ptr;           // 指向实际值的指针
} robj;
typedef struct redisClient {  
    int fd;                // 套接字描述符
    redisDb *db;           // 当前正在使用的数据库
    robj *name;            // 客户端的名字，set by CLIENT SETNAME 
    time_t lastinteraction;// 最后依次交互的时间，据此判断超时

    sds querybuf;          // 查询缓冲区
    size_t querybuf_peak;  // 查询缓冲区长度峰值，Recent (100ms or more) peak of querybuf size
    struct redisCommand *cmd, *lastcmd; // 记录被客户端执行的命令
    int argc; // 参数数量
    robj **argv; // 参数对象数组
    
    list *reply;               // 回复链表
    unsigned long reply_bytes; // 回复链表中对象的总大小
    int sentlen;               // 已发送字节，处理 short write 用

    int bufpos;        // 回复偏移量
    char buf[16*1024]; // 回复缓冲区
} redisClient;
struct redisServer {
    char *configfile;           // 配置文件的绝对路径
    int hz;                     // serverCron() 每秒调用的次数
    redisDb *db;                // 数据库
    dict *commands;             // 命令表（受到 rename 配置选项的作用）
    aeEventLoop *el;            // 事件状态

    int port;                   /* TCP listening port */
    int tcp_backlog;            /* TCP listen() backlog */
    char *bindaddr[16];         /* Addresses we should bind to */
    int bindaddr_count;         /* Number of addresses in server.bindaddr[] */
    int ipfd[16];               /* TCP socket file descriptors */
    int ipfd_count;             /* Used slots in ipfd[] */

    list *clients;              /* List of active clients */
    list *clients_to_close;     /* Clients to close asynchronously */
    int maxidletime;            /* 客户端最大空转时间，Client timeout in seconds */
};
```

#### 第10章 键的相关命令
* 读取redisDb的dict字典的命令：
  * object refcount {key}
  * object encoding {key}
  * type {key}
* 读取redisDb的expires字典的命令：
  * ttl {key}
  * expire {key} {seconds}
* object encoding {key}的执行流程：
  * readQueryFromClient
  * processCommand会调用lookupCommand赋值c->cmd，并执行call(c)
  * call(c)会执行c->cmd->proc，即实际的处理函数objectCommand
  * objectCommand调用objectCommandLookupOrReply获取key对应的robj
  * 根据robj->encoding字段返回描述

#### 第11章 字符串的相关命令
* c->cmd->proc对应的是setCommand（set命令）
* b processCommand
* set a 100
* 打印请求的三个参数：p *c->argv\[0]、p *c->argv\[1]、p *c->argv\[0]
* 此时的100是字符串：p (char *)c->argv\[2]->ptr
* b tryObjectEncoding
* 此时的100是字符串，tryObjectEncoding之后变成int，p *c->argv\[2]的结果如下：
* {type = 0, encoding = 1, lru = 8272013, refcount = 2, ptr = 0x64}
* set a 10001然后重新debug一遍，p *c->argv\[2]的结果如下：
* {type = 0, encoding = 1, lru = 8273125, refcount = 1, ptr = 0x2711}
* 说明10000以内的整数的robj是redis已经预分配好的，每次使用refcount++，10000以上的则把ptr指针当值用

#### 第12章 散列表hash的相关命令
* c->cmd->proc对应的是hsetCommand（hset命令）
* hset a key val
* hsetCommand()默认robj->ptr是ziplist，hashTypeTryConversion()判断是否转换成dict
  * 然后调用hashTypeSet()设置key和val
  * hashTypeSet()函数内部会判断robj->encoding以执行不同的逻辑
  * hashTypeXXX()函数和hashTypeSet()类似
  
#### 第13章 列表list的相关命令
* c->cmd->proc对应的是lpushCommand（lpush命令）
* 实现栈：lpush、lpop
* 实现队列：lpush、rpop
* lpush：lpushCommand()默认robj->ptr是ziplist，listTypeTryConversion()判断是否转换成linkedList
* bpop的实现流程：
  * bpop {key} {timeout}。timeout=0表示无限期的阻塞
  * 执行bpop后，设置c->bpop->timeout和c->bpop->keys，设置redisDb->blocking_keys，并阻塞
  * 解除情况1：其他客户端执行了push命令，检测key在redisDb->blocking_keys内，找到对应的客户端，执行unblockingClient
  * 解除情况2：serverCron定时遍历所有的客户端，检查c->bpop->timeout，发现超时则执行unblockingClient

#### 第14章 无序集合set的相关命令
* c->cmd->proc对应的是saddCommand（sadd命令）
* hsetCommand()判断元素的类型是否是整型，是则用intset、否则用dict

```
typedef struct intset {
    uint32_t encoding; // 有三种：INTSET_ENC_INT16、INTSET_ENC_INT32、INTSET_ENC_INT64，支持升级、不支持降级
    uint32_t length;   // 元素个数
    int8_t contents[]; // 一个单位占一个字节，根据encoding类型占用不同单元
}
```

#### 第15章 有序集合zset的相关命令
* zset的robj有两种类型：ziplist和zset
* 使用ziplist：元素按照score大小顺序存储，先存元素，再存score
* 使用zset：dict和skiplist的结合，[为什么有序集合需要同时使用跳跃表和字典来实现？](http://redisbook.com/preview/object/sorted_set.html)
  * 仅使用dict，单个元素的增删改是O(1)，但是ZRANK、ZRANGE需要O(N * logN)
  * 仅使用skiplist，单个元素的增删改是O(logN)，ZRANK、ZRANGE需要O(logN)
  * dict和skiplist的结合：zs->dict->ht\[0].table\[2]->key就是元素robj，zs->zsl下的节点zskiplistNode->robj就是元素robj
* 使用zset：用zadd更新同一个元素的score的流程：
  * 从zs->dict查找元素是否存在，O(1)
  * 在zs->zsl中先zslDelete，再zslInsert。（继续用元素robj，内存块不变），O(logN)
  * 更新zs->dict中对应元素的分值指针，O(1)

```
typedef struct zskiplistNode {
    robj *obj;                         // 成员对象
    double score;                      // 分值
    struct zskiplistNode *backward;    // 后退指针
    struct zskiplistLevel {
        struct zskiplistNode *forward; // 前进指针
        unsigned int span;             // 跨度
    } level[];
} zskiplistNode;

typedef struct zskiplist {  
    struct zskiplistNode *header, *tail; // 表头节点和表尾节点
    unsigned long length;                // 表中节点的数量
    int level;                           // 表中层数最大的节点的层数
} zskiplist;

typedef struct zset {
    dict *dict;     // 键为成员，值为分值   
    zskiplist *zsl; // 跳跃表，按分值排序成员
} zset;
```

#### 第16章 GEO的相关命令
* 先把经纬度geohash，再geohash-int转成long long类型，再用zset结构存储
* 例如geoadd beijing 116.312 40.058 xierqi
  * beijing是键名
  * xierqi是zset的元素
  * 坐标geohash-int后的值是score
  
#### 第17章 HyperLogLog

#### 第18章 Stream
  
#### 第19章 其他命令
* 事务
  * multi：开启事务
  * discard：放弃事务
  * exec：提交事务
  * watch：监听指定的key，如果key发生变化则事务不执行（相当于乐观锁）
  * unwatch：取消监听
* 发布-订阅
  * subscribe {channelName}：订阅频道
  * publish {channelName} {message}：向频道发送消息
* Lua脚本
  * eval "Lua代码"
  * 事务和Lua脚本都可以实现原子性
  
#### 第20章 持久化-RDB快照和AOF日志
* RDB快照的触发方式
  * bgsave命令
  * save 60 1000：60秒内如果有1000个key发生变化则触发
* RDB快照的文件结构，共九项：
  1. 固定为“REDIS”，5B
  1. RDB的版本号，4B
  1. 辅助字段对，如redis-server版本号
  1. DB_NUM，一般是0~15
  1. DB_DICT_SIZE，db_dict的哈希表大小，这样还原时可以直接扩容到此大小
  1. EXPIRE_DICT_SIZE，expire_dict的哈希表大小，这样还原时可以直接扩容到此大小
  1. KEY_VALUE_PAIRS，键值对内容
  1. EOF结束标志，1B
  1. CHECK_SUM，8B
* AOF日志的写入模式
  * appendfsync=no，write后不强制fsync，由操作系统负责刷盘
  * appendfsync=always，每次write后都执行fsync
  * appendfsync=everysec，每秒执行一次fsync
* AOF日志重写的触发方式
  * bgrewriteaof
  * 配置自动重写规则，如aof文件大小比当前增长了100%时触发
* AOF日志重写的两种方式
  * 设置重写时间点，遍历时间点之前的数据生成aof命令日志，拼接上时间点之后产生的aof日志
  * 设置重写时间点，遍历时间点之前的数据生成RDB快照，拼接上时间点之后产生的aof日志（即混合持久化）

#### 第21章 主从复制
* psync2协议解决了主服务器M宕机，从服务器A变为主服务器，从服务器B、C仍然可以从A这里进行“部分重同步”
* 从服务器的流程：
  1. 接收到slaveof命令后连接socket
  1. 发送ping包确保连接正常
  1. 发起密码验证（如果需要）
  1. 发送replconf命令同步信息
  1. 发送psync命令
  1. 接收RDB文件并载入
  1. 等待主服务器的同步命令请求
* 主服务器的流程：
  1. 监听并接收socket
  1. 回复ping包
  1. 回复密码验证
  1. 处理replconf命令：
    * 从服务器的监听端口和IP（端口一般是6379）
    * eof标识：从服务器支持无盘复制
    * psync2标识：从服务器支持psync2协议
    * 从服务器的复制偏移量
  1. 处理psync命令：
    * 如果可以部分重同步，发送+CONTINUE和后续命令
    * 如果需要完全重同步，则先执行RDB快照。然后进行无盘复制或者先写硬盘，再发送
  1. 发送RDB文件  
  1. 每次收到写命令，广播给从服务器
  
```
wireshark抓包：https://ryan4yin.space/posts/tcpdump-and-wireshark/
Kubernetes抓包：推荐直接使用 ksniff

ssh root@localhost "tcpdump -i lo -l -w -" | wireshark -k -i -
```

#### 第22章 哨兵和集群
* 哨兵的配置：
  * 只需要配置Master节点，保证配置文件可写
  * 与Master节点建立连接后，收集Slaves和其他哨兵的信息，并写入配置文件作持久化
* 哨兵的运行流程：
  * 启动监听，默认端口是26379
  * 建立命令连接、消息连接
  * 命令连接：
    * 定时10s：发送info命令收集Slaves的信息
    * 定时1s：发送ping命令探测存活性
    * 定时2s：publish消息给其他哨兵（选举用）
  * 消息连接：
    * 哨兵订阅Master和Slaves的消息，获知其他哨兵的信息
  * PS：哨兵针对Master和Slaves会建立命令连接和消息连接，针对其他哨兵只建立命令连接
* 哨兵确认节点下线：
  * 主观下线：针对Master和Slaves，还有其他哨兵
  * 主观下线：只针对Master
* 哨兵处理主从切换：
  * 选出主哨兵
  * 选择一台Slave作为主节点：
    * 不能是主观下线状态
    * 5s内没有回复ping，不能选
    * slave-priority=0，不能选
    * if 优先级高，选中
    * else if 复制的偏移量大，选中
    * else if runid最小，选中
* 集群的典型例子：三主三从
  * redis把键空间分成了16384个slot
  * 主从节点都有这16384个slot的信息（slot对应的节点ip和port）
  * 如果客户端请求节点，对应的键正好在该节点则直接服务，不在则返回MOVED slot IP:PORT
  * 事实上客户端可以获取16384个slot信息并缓存
  * 从节点默认不提供服务，只作为备份节点，若要提供读服务则要注意2点：
    * 客户端先执行readonly
    * 若键对应的节点是某主节点，则可以直接向它的从节点发起读请求
 * 集群的主从切换：支持手动和自动
 * 集群的副本漂移：例如三主四从，A节点挂了发生主从切换，A处没有从节点了，可以从其他地方挪一个过来



