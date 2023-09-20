### 缓存模式

#### 五种缓存模式
* [缓存的五种设计模式](https://xie.infoq.cn/article/49947a60376964f1c16369a8b)
* Cache aside：cache不存在时去读db；写db，写完删cache
* Read Through：cache不存在时cache去读db
* Write through：先更新cache再更新db，都成功后返回
* Write Behind：先更新cache，再异步更新db，也称Write Back
* Write Around：绕过cache直接更新db

#### CPU Cache
* [关于 CPU 上的高速缓存](https://www.junmajinlong.com/os/cpu_cache/)
* write-invalidate，Core1修改x=3，则需更新L3缓存，同时通知其他Core的L1、L2失效
* 写缓存策略
  * write through + write allocate：未命中时先cache数据再修改
  * write through + no write allocate：未命中则只修改下游缓存
  * write back + write allocate
  * write back + no write allocate
  * （一般采用write through + no write allocate和write back + write allocate）

#### Server Cache
* [缓存模式以及缓存的数据一致性](https://stephanietang.github.io/2020/04/13/cache-pattern/)
* 方案一：Cache aside
  * 优点：仅在cacheMiss时更新缓存
  * 缺点：cacheMiss时读取耗时长，且存在[缓存不一致问题](../images/cache-aside-trouble.png)
* 方案二：Read Through/Write Through
  * 优点：cacheMiss时读取耗时短
  * 缺点：对于读少写多的场景不友好
* 方案三：Read Through/Write Behind
  * 优点：没有方案二的缺点
  * 缺点：因为是异步更新db，可能导致数据丢失
* 方案四：Read Through/Write Around
  * 优点：没有方案二的缺点
  * 缺点：存在缓存不一致问题
* 基于方案一的优化1：[B站的方案](../images/cache-bilibili.png)
  * 请求1：cacheMiss->读v1->setNX
  * 请求2：writeDB(v2)->setEX
  * 写写场景的方案1：binlog异步任务补偿cache
  * 写写场景的方案2：更新锁
* 基于方案一的优化2：[Facebook的方案](../images/cache-facebook.png)
  * 请求1：cacheMiss并得到leaseId->读v1->set(v1, leaseId)
  * 请求2：writeDB(v2)->delCache并使leaseId失效



