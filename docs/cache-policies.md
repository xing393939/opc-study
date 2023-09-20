### 缓存模式

#### 五种缓存模式
* [缓存的五种设计模式](https://xie.infoq.cn/article/49947a60376964f1c16369a8b)
* Cache aside：cache不存在时去读db；写db，写完删cache
* Read Through：cache不存在时cache去读db
* Write through：先更新cache再更新db，都成功后返回
* Write Behind：先更新cache，再异步更新db，也称Write Back
* Write Around：绕过cache直接更新db

#### CPU Cache
* write-invalidate，Core1修改x=3，则需更新L3缓存，同时通知其他Core的L1、L2失效
* 

#### Server Cache
* 



