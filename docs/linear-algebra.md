### 线性代数

#### 1 introduction to vectors
![Alt text](image-2.png)

#### 2 Solving Linear Equations
* [线性代数 - Machine Learning](https://machine-learning-from-scratch.readthedocs.io/zh_CN/latest/%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0.html)
  * 线性相关：一个向量能被向量组的其他成员线性组合出来；线性无关则不能。
  * 基的定义：向量组中的向量互相线性无关，张成空间V，则它们是空间V的一组基。
  * `选定基之后，向量表示对象，矩阵表示对象的运动，矩阵与向量相乘得到新的向量。一旦理解了这点，线性代数之后的各个主题，包括矩阵乘法、基变换、特征值等都会非常直观易懂。`
  * 旋转矩阵：例如二维矩阵，可以将二维向量按角度旋转，见[二维旋转矩阵与向量旋转](https://zhuanlan.zhihu.com/p/98007510)
  * 变换矩阵：坐标系xyz中的向量v，坐标系XYZ中的向量V，存在变换矩阵R使得`V = R * v`
  * 剪切矩阵：变换矩阵中的一种，例如把正方形往一边挤压，使之成为平行四边形。
* 线性方程组（Ax=b）求解的两种方法：
  * 高斯消元：先得到Ux=b\*，再求解出x
  * LU分解：先由A得到LU，再由Ly=b求解y，再由Ux=y求解x
  * 两者的时间复杂度都是n^3，但在A不变的情况下，LU分解的第2、3步只需要n^2
* 求A的逆矩阵：将 \[A I] 逐步消元成 \[I A^-1]

![Alt text](image-1.png)

#### 3 Vector Spaces and Subspaces
* 子空间：子空间任意两个向量v和w，它们的线性组合仍然在子空间内。
  * 原点是R^3的子空间
  * 过原点的直线是R^3的子空间
  * 过原点的平面是R^3的子空间
* 四个基本子空间：  
  * 列空间：矩阵A的列空间C(A)是其列向量的所有线性组合所构成的空间。
  * 零空间：矩阵A的零空间N(A)是指满足Ax=0的所有解的集合(所有x的集合)。
  * 行空间：矩阵A的行空间C(A)是其行向量的所有线性组合所构成的空间。
  * 左零空间：矩阵A^T的零空间即是矩阵A的左零空间。
  * （对于mxn矩阵，列空间为R^m的子空间，零空间为R^n空间的子空间）
* 求解Ax=0，参考[【线性代数】矩阵的零空间](https://blog.csdn.net/tengweitw/article/details/40039373)
  * A消元成U后，有r个主元列，n-r个自由列
  * U继续消元成新矩阵：第一行是I F，第二行是0 0。
  * 零空间（最终的解）：第一行是-F，第二行是I。有列交换则要注意还原
  * （A的列空间的维度是r，零空间的维度是n-r）
* 求解Ax=b，假设有r个主元列
  * r=n=m：R=I，唯一解
  * r=n<m：R=(第一行是I，第二行是0)，唯一解或无解
  * r=m<n：R=\[I 0]，无穷多解
  * r<n,r<m：R=(第一行是I F，第二行是0 0)，无穷多解或无解

#### 4 Orthogonality(正交) 

#### 5 Determinants(行列式)

#### 6 Eigenvalues and Eigenvectors(特征值和特征向量) 

#### 7 The Singular Value Decomposition(奇异值分解) 

#### 8 Linear Transformations(线性变换) 

#### 9 Complex Vectors and Matrices(复向量和矩阵)

#### 10 Applications(应用)

#### 11 Numerical Linear Algebra(数值线性代数) 

#### 12 Linear Algebra in Probability & Statistics(概率统计中的线性代数)
