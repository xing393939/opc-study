### 刘二大人

<script>
  MathJax = {
    tex: {
      inlineMath: [['$', '$'], ['\\(', '\\)']],
      displayMath: [["$$", "$$"], ["\\[", "\\]"]],
    },
    svg: {
      fontCache: 'global'
    }
  };
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://static-621585.oss-cn-beijing.aliyuncs.com/mathjax-v3.js">
</script>

#### 参考资料
* [刘二大人-cnblog](https://www.cnblogs.com/zhouyeqin/category/2231506.html)
* [刘二大人-zhihu](https://zhuanlan.zhihu.com/p/166104074)

#### 第二讲-线性模型
* MSE：均值平方误差(Mean Square Error)，$MSE=\frac{1}{N} \sum\limits_{n=1}^N (\hat{y}_n - y_n)^2$
* 训练集(1,2)、(2,4)、(3,6)，用穷举法预测x=4时，y的值：
  * 假设模型是y = 𝜔 * x，求𝜔的值
  * for (𝜔=0; 𝜔<4.1; 𝜔+=0.1)，依次求出MSE，取MSE最低时𝜔的值

#### 第三讲-梯度下降法
* 训练集(1,2)、(2,4)、(3,6)，用梯度下降法预测x=4时，y的值：
* 梯度下降：
  * 假设模型是y = 𝜔 * x，求𝜔的值
  * 先选定𝜔=1
  * 下一个$𝜔=𝜔-α\frac{𝜕cost}{𝜕𝜔}$，其中α表示步长，cost即MSE
  * 下一个$𝜔=𝜔-α\frac{1}{N}\sum\limits_{n=1}^N 2.x_n.(x_n.𝜔 - y_n)$
  * 步长定为0.01，迭代100次，观察MSE值是否会收敛
* 随机梯度下降：
  * 假设模型是y = 𝜔 * x，求𝜔的值
  * 先选定𝜔=1
  * 下一个$𝜔=𝜔-α\frac{𝜕loss}{𝜕𝜔}$，其中α表示步长，$loss = (\hat{y}_n - y_n)^2 \quad \frac{𝜕loss}{𝜕𝜔} = 2.x_n.(x_n.𝜔 - y_n)$
  * 步长定为0.01，迭代100次，观察loss值是否会收敛
* 梯度下降和随机梯度下降
  * 随机梯度下降需要等待上一个值运行完才能更新下一个值，无法并行计算
  * 随机梯度下降可以有效解决鞍点问题
  * 折中的办法是mini_batch

#### 第四讲-反向传播
* 假设模型是y = 𝜔 * x，求𝜔的值，[见图](../images/back_propagation.png)
* 假设模型是y = 𝜔 * x + b，[人工智能原理-曲面梯度下降和反向传播](https://blog.csdn.net/wanlin_yang/article/details/129263378)
  * $loss = (y_n - (𝜔x + b))^2 = x_n^2𝜔^2 + (2x_n.b - 2x_n.y_n)𝜔 + (y_n^2 + b^2 - 2y_n.b)$
  * $\frac{𝜕loss}{𝜕𝜔} = 2x_n^2𝜔$










