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
* [携程最终一致和强一致性缓存实践](https://www.infoq.cn/article/hh4iouiijhwb4x46vxeo)
* 常见方案：Cache-Aside和Write-Invalidate
  * 缺点A：cacheMiss时读取耗时长
  * 缺点B：读写场景下，setCache(v1)在delCache()之后执行，[见图](https://www.plantuml.com/plantuml/duml/JO-z3i8m38JtF8L762hHIgoe_AniR547gp75QX95iO7N1wjBlDtv-uORHR7gEqNdPELSi6A2YdaLAZ0ScZ8KXduuDat1USM57goHpf6Nd2WhH7ggStx6-KLt5fcwxkGhORXTTfz-FxasT7O62EdLZ0rn7YQm1_XlPIMZ1rFRP5gWk6acZPJ3VyaF)
* 携程方案：Cache-Aside和Write-Invalidate，[见图](../images/cache-ctrip.png)
  * 缺点C：读写场景和写写场景需要加锁
* B站方案：Cache-Aside和Write-Allocate，[见图](https://www.plantuml.com/plantuml/duml/SoWkIImgAStDuIhEpimhI2nAp5KeIipBBaujK30oG19CASXKC3GoHH8fI4pEJanF3SaioKbrpCbCpyjDpIjHo4bDA-7YAafDBadCIyz9LL1wiNxtqxQPJ-ViUZPplP92DPU2GdHoOd96gczcSN6ihgvTT55gOegBaqQPeMOiK1APgmi282N5gIL-5J0LIa2egwiGNLwKMP8AKca44aRbGpL1v6fHt0Dq39fx43gDaNGQevbgWYHd0ZRL8JKl1HXo0000)
  * 缺点D：写写场景下，set(v3)在set(v4)之后执行
  * 缺点E：写DB成功，操作cache失败
  * 优化缺点D：写写场景需要加锁
  * 优化缺点E：binlog异步任务补偿cache
* Facebook方案：[见图](https://www.plantuml.com/plantuml/duml/L8wzIiL048NxUOefjGYQW8s4u8-5ZPtTac989d79_YoxewBYkryckSNUwSwSxuFpK8IoV7e7PRCXKIQFcS9ME65tMptdPB7jxgfFeccZbT-jE7vqTWsUWw3ZHQ0lykDu0D4E_rvZjhyn2BbBxX_wcpC9PgBfWzziAMFJ32OppIzFLr_jzGXrQFGKA2pFQXm861nH2pJVsGehtQbQ9zLcTeUc4eGel2_1k62r0E_Hiz_pQK_sp7hQqVQojJSdDR4urJC5LG-ACq3QNivfUB6iyUcEPKzsTC5qG8A1wyNobgSTCmsj59wlMMFuPCUgvxlsFr_H3RVq-QoMPzEtFMsOYMwZXg71y-MJNknlVpPdlkRxFJrF9_GztxqMJVUpJGkVpUc4wNY-jlFfljQdExUzREzziNwg9jHk8oi5c7lXjZtTt_fouMw4Ng05JtPCUJPZFL3esTGEe3gePcCh1LZW8Powi_jfP-_J_eb04QZ-fnlQdYxP2DG9TocoCv_shqSDpTIy50L8y3W0cS1q2000)
  * 请求1：cacheMiss并得到leaseId->readDB(v1)->set(v1, leaseId)
  * 请求2：writeDB(v2)->delCache并使leaseId失效
* rockscache方案，Cache-Aside和Write-Invalidate，[链接](https://www.dtm.pub/app/cache.html)
  * 请求1：cacheMiss->readDB(v1)->set(v1)
  * 请求2：writeDB(v2)->TagDeleted
  * 通过二阶段消息保证DB和cache的一致性

| 缺点 |常见方案| 携程 | B站 | Facebook | rockscache |
| --- | ---   | --- | --- | ---      | --- |
| 缺点A | √    |  √  |     |  √       | √   |
| 缺点B | √    |     |     |          |     |
| 缺点C |      |  √  |     |          | √   |
| 缺点D |      |     |  √  |          |     |
| 缺点E | √    |  √  |  √  |  √       |&nbsp;|
