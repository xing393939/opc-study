### 缓存模式

#### 五种缓存模式
* [缓存的五种设计模式](https://xie.infoq.cn/article/49947a60376964f1c16369a8b)
* Cache-Aside：&nbsp;&nbsp;userRead(cache)——userRead(db)——userManage(cache)
* Read-Through：userRead(cache)——cacheRead(db)——cacheManage(cache)
* Write-Through：userWrite(cache)——cacheWrite(db)
* Write-Behind：&nbsp;&nbsp;userWrite(cache)——cacheWrite(db)(Async)，也称Write-Back
* Write-Around：&nbsp;&nbsp;userWrite(db)

#### CPU Cache
* [关于 CPU 上的高速缓存](https://www.junmajinlong.com/os/cpu_cache/)
* write-invalidate，Core1修改x=3，则需更新L3，同时通知其他Core的L1、L2失效
* 如果发生cacheHit，有两个策略：
  * write-through: 更新L3，同时写入内存
  * write-back: 更新L3，需要被置换出去时写入内存
* 如果发生cacheMiss，有两个策略：
  * write-allocate: 先载入L3再操作
  * no-write-allocate: 不载入L3直接操作
* 一般采用write-through和no-write-allocate、write-back和write-allocate

#### Server Cache
* [缓存模式以及缓存的数据一致性](https://stephanietang.github.io/2020/04/13/cache-pattern/)
* [dtm-labs缓存一致性](https://www.dtm.pub/app/cache.html)
* [携程最终一致和强一致性缓存实践](https://www.infoq.cn/article/hh4iouiijhwb4x46vxeo)
* 常见方案：Cache-Aside和Write-Invalidate
  * 缺点A：cacheMiss时读取耗时长
  * 缺点B：存在[缓存不一致问题](../images/cache-aside-trouble.png)
* 携程的方案：Cache-Aside和Write-Invalidate，[见图](../images/cache-ctrip.png)
  * 缺点A
  * 缺点C：读DB和写DB有锁
* B站的方案：Cache-Aside和Write-Allocate，[见图](../images/cache-bilibili.png)
  * 缺点D：写写场景下，set(v1)在set(v2)之后执行
  * 缺点E：写写场景下，set(v2)失败导致缓存仍然是v1版本
  * 缺点D的优化：更新锁
  * 缺点E的优化：binlog异步任务补偿cache
* Facebook的方案：[见图](../images/cache-facebook.png)
  * 请求1：cacheMiss并得到leaseId->读v1->set(v1, leaseId)
  * 请求2：writeDB(v2)->delCache并使leaseId失效


