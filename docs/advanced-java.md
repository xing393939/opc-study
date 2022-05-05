### Java工程师进阶知识

#### 参考资料
* [Java工程师进阶知识](https://doocs.gitee.io/advanced-java/#/README)

#### 消息队列
* 优点1：解耦，假设功能A完成一个操作后，需要通知BCD，需要考虑失败处理或者部分失败的情况，用MQ就方便多了
* 优点2：异步，提高接口的响应速度，慢操作可以异步去处理
* 优点3：消峰，在高峰时缓冲待处理操作，提高吞吐
* 缺点：多引用了MQ这个组件，多了一个故障点，系统复杂度增加
* kafka的高可用性：每个partition有多个replica副本，其中一个副本是leader
  * 写数据：只写leader，当所有的follower都同步了消息后，leader通知生产者写入成功
  * 消费：只读leader，当所有的follower都同步了消息后，这个消息才可见
* 重复消费问题：消费消息时要保证消息的幂等
* RabbitMQ如何不丢消息：
  * 生产者：开启异步confirm模式
  * MQ：开启镜像集群模式，消息持久化导磁盘
  * 消费者：关闭自动ack，使用手动ack
* MQ积压了几个小时怎么处理？
  * 停掉原有consumer程序，上新的consumer程序A把消息消费到新的10倍大小的MQ中
  * 上10倍的consumer程序B来消费新的MQ
  * 处理完挤压数据后，恢复原有的consumer程序

#### ElasticSearch
* es写入数据：
  * 1秒后可被搜索：因为数据定时一秒从buffer写入到segment file(即使在os cache也能被搜索)
  * 5秒后可持久化：日志实时从buffer写入到translog，定时5秒执行一次fsync
* 数十亿级别的数据量优化：
  * 机器的内存至少要能容纳数据量的一半
  * 垂直拆分：es只存储搜索字段，查出id后再去DB查询详细字段
  * 写脚本先把数据预热在cache
  * 冷热分离，冷热数据用不同的index
  * es的表设计：先join好数据了再写入es，减少es的查询复杂度
  * 分页性能优化：使用search_after参数

#### Redis缓存

#### Mysql相关

#### 海量数据处理
