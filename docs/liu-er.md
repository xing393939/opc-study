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
* [numpy在线运行](https://onecompiler.com/python/3zqwrqg2r)
* [float的表示](https://zhuanlan.zhihu.com/p/503336736)：符号(1b)、阶码(8b)、尾数(23b)
  * 0.875：0.111，需要右移1位，阶码=127+(-1)，尾数=11
  * 6.360：110.01011100，需要左移2位，阶码=127+2，尾数=10010111000010100011111
  * 2^23 = 8388608。也就是说，有效数字在±8388608内的整数和小数，精度不会损失

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
* 假设模型是$y = 𝜔 * x$，求𝜔的值，[见图](../images/back-propagation.png)
* 假设模型是$y = 𝜔 * x + b$，[人工智能原理-曲面梯度下降和反向传播](https://blog.csdn.net/wanlin_yang/article/details/129263378)
  * $loss = (𝜔x + b - y)^2 = x^2𝜔^2 + (2x.b - 2x.y)𝜔 + (y^2 + b^2 - 2y.b)$
  * $\frac{𝜕loss}{𝜕𝜔} = 2x(𝜔x + b - y)$
  * $\frac{𝜕loss}{𝜕b} = 2(𝜔x + b - y)$
  * 梯度下降解法：liuer/lesson4_2.py
  * 随机梯度下降：liuer/lesson4_3.py
* 假设模型是$y = 𝜔 * x + b$，计算损失函数相对于各个参数的偏导数来求解梯度。
  * $loss = (\hat{y} - y)^2 \quad \hat{y} = 𝜔 * x + b$
  * $\frac{𝜕loss}{𝜕𝜔} = \frac{𝜕loss}{𝜕\hat{y}}.\frac{𝜕\hat{y}}{𝜕𝜔} = 2(\hat{y} - y).x$
  * $\frac{𝜕loss}{𝜕b} = \frac{𝜕loss}{𝜕\hat{y}}.\frac{𝜕\hat{y}}{𝜕b} = 2(\hat{y} - y).1$
* 假设模型是$y = 𝜔_1.x^2 + 𝜔_2.x + b$
  * $loss = (\hat{y} - y)^2 \quad \hat{y} = 𝜔_1.x^2 + 𝜔_2.x + b$
  * $\frac{𝜕loss}{𝜕𝜔_1} = \frac{𝜕loss}{𝜕\hat{y}}.\frac{𝜕\hat{y}}{𝜕𝜔_1} = 2(\hat{y} - y).x^2$
  * $\frac{𝜕loss}{𝜕𝜔_2} = \frac{𝜕loss}{𝜕\hat{y}}.\frac{𝜕\hat{y}}{𝜕𝜔_2} = 2(\hat{y} - y).x$
  * $\frac{𝜕loss}{𝜕b} = \frac{𝜕loss}{𝜕\hat{y}}.\frac{𝜕\hat{y}}{𝜕b} = 2(\hat{y} - y).1$

#### 第五讲-PyTorch线性回归
* PyTorch的四个步骤：准备数据、定义模型、定义损失函数和优化器、训练周期
* 训练周期的三个步骤：
  * 前馈forward：计算$\hat{y} \quad loss$
  * 反馈backward：反向传播、计算梯度
  * 更新update：更新参数

#### 第六讲-逻辑斯谛回归
* [一篇文章搞懂logit, logistic和sigmoid的区别](https://zhuanlan.zhihu.com/p/358223959)
* 逻辑斯谛回归(Logistic Regression)，简称LR
* sigmoid函数是指某一类形如"S"的函数，例如[这些函数](../images/sigmoid-function.jpg)
* logistic函数也是sigmoid函数，在PyTorch中sigmoid函数即是logistic函数
* logistic回归虽然名为回归，但实际用于分类问题。
* torch.nn.BCELoss是CrossEntropyLoss的一个特例，只用于二分类问题，而CrossEntropyLoss可以用于二分类，也可以用于多分类。
* sigmoid函数的输入记为z，$z = 𝜔_0.x_0 + 𝜔_1.x_1 + ... + 𝜔_n.x_n$，z=0为决策边界，z>0为真，z<0为假
  * 上述公式的向量写法是$z = 𝜔^T.x$，梯度下降公式推导见[逻辑回归(LR)算法详解和实战](https://blog.csdn.net/Mr_Robert/article/details/88888973)
  * $loss = -y\log(\hat{y}) - (1 - y)\log(1 - \hat{y})$
  * $cost = -\frac{1}{N}\sum\limits_{n=1}^N y\log(\hat{y}) + (1 - y)\log(1 - \hat{y})$，从这里开始省略下标n
  * $\frac{𝜕cost}{𝜕𝜔} = \frac{𝜕cost}{𝜕\hat{y}}.\frac{𝜕\hat{y}}{𝜕𝜔}$，其中$\hat{y} = \frac{1}{1 + e^{-z}}$
  * $\frac{𝜕cost}{𝜕𝜔} = -\frac{1}{N}\sum\limits_{n=1}^N (\frac{y}{\hat{y}} - \frac{1-y}{1-\hat{y}}) . (\frac{𝜕\hat{y}}{𝜕z}.\frac{𝜕z}{𝜕𝜔})$，其中$\frac{𝜕\hat{y}}{𝜕z} = \hat{y} . (1 - \hat{y})$
  * $\frac{𝜕cost}{𝜕𝜔} = -\frac{1}{N}\sum\limits_{n=1}^N (\frac{y}{\hat{y}} - \frac{1-y}{1-\hat{y}}) . \hat{y} . (1 - \hat{y}) . x$
  * $\frac{𝜕cost}{𝜕𝜔} = -\frac{1}{N}\sum\limits_{n=1}^N (y - \hat{y}).x$
  * $\frac{𝜕cost}{𝜕𝜔} = \frac{1}{N}\sum\limits_{n=1}^N (\hat{y} - y).x$
* $z = 𝜔_0.x_0 + 𝜔_1.x_1 + 𝜔_2.x_2$，其中$x_0$恒为1
  * 代码liuer/lesson6.py：[机器学习之逻辑回归Logistic Regression](https://blog.csdn.net/qq_41750911/article/details/124889545)
  * 代码liuer/lesson6_1.py：[逻辑回归手动实现（logistic regression）](https://blog.csdn.net/qq_37055672/article/details/124779634)

#### 第七讲-处理多维输入
* 线性模型：y = Ax。线性也就是直线，是一次方程。
* torch.nn.Linear(8, 1)表示输入是8维，输出是1维，即A是1x8，x是8x1，y是1x1
* torch.nn.Linear(8, 6)表示输入是8维，输出是6维，即A是6x8，x是8x1，y是6x1
* 非线性激活函数使得神经网络可以逼近任何非线性函数
* 非线性激活函数[见](https://pytorch.org/docs/stable/nn.html#non-linear-activations-weighted-sum-nonlinearity)，其中有torch.nn.Sigmoid

#### 第八讲-Dataset和DataLoader
* Dataset是抽象类，需要用户编写具体类
* DataLoader需要一个Dataset具体类，生成一个迭代对象

#### 第九讲-多分类问题
* 关于把图片转成tensor格式，参考liuer/image2tensor.py
* 为什么要执行transforms.Normalize((0.1307,), (0.3081,))？

#### 第十讲-卷积神经网络-基础篇
* CNN(Convolution Neural Network)：卷积神经网络
* [卷积神经网络中的激活函数sigmoid、tanh、relu](https://blog.csdn.net/qq_39751352/article/details/124649762)
  * 激活函数的目的：将神经网络非线性化，即提升神经网络的拟合能力，能拟合更复杂的函数。
  * 如果模型只有线性操作，则永远只能表示超平面，无法表示曲面等
* [网络层：池化层、全连接层和激活函数层](https://yey.world/2020/12/16/Pytorch-13/)  
* 卷积神经网络除了输入和输出层之外还有四个基本的神经元层：
  * 卷积层（Convolution）：[torch.nn.Conv2d](https://pytorch.apachecn.org/1.0/nn/#conv2d)
  * 池化层（Pooling）：[torch.nn.MaxPool2d](https://pytorch.apachecn.org/1.0/nn/#maxpool2d)
  * 激活层（Activation）
  * 完全连接层（Fully connected）：每个神经元与上一层所有神经元相连，如果不考虑激活函数的非线性性质，那么全连接层就是对输入数据进行一个线性组合

#### 第十一讲-卷积神经网络-高级篇


#### 第十二讲-循环神经网络-基础篇


#### 第十三讲-循环神经网络-基础篇


