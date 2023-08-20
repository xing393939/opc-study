### 线性代数

<style>
span {display:inline-block;vertical-align:middle;}
span sup, span sub{position:relative;display:block;line-height:0.2em;}
</style>

#### 参考资料
* [数学符号及读法大全](https://blog.csdn.net/qq_37212752/article/details/83956265)

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
  * （两者的时间复杂度都是n<sup>3</sup>，但在A不变的情况下，LU分解的第2、3步只需要n<sup>2</sup>）
* 求A的逆矩阵：将 \[A I] 逐步消元成 \[I A<sup>-1</sup>]

![Alt text](image-1.png)

#### 3 Vector Spaces and Subspaces
* 子空间：子空间任意两个向量v和w，它们的线性组合仍然在子空间内。
  * 原点是R<sup>3</sup>的子空间
  * 过原点的直线是R<sup>3</sup>的子空间
  * 过原点的平面是R<sup>3</sup>的子空间
* 四个基本子空间：  
  * 列空间：矩阵A的列空间C(A)是其列向量的所有线性组合所构成的空间。
  * 零空间：矩阵A的零空间N(A)是指满足Ax=0的所有解的集合(所有x的集合)。
  * 行空间：矩阵A的行空间C(A)是其行向量的所有线性组合所构成的空间。
  * 左零空间：矩阵A<sup>T</sup>的零空间，即是矩阵A的左零空间。
  * （对于mxn矩阵，列空间为R<sup>m</sup>的子空间，零空间为R<sup>n</sup>空间的子空间）
* 求解Ax=0，参考[【线性代数】矩阵的零空间](https://blog.csdn.net/tengweitw/article/details/40039373)
  * A消元成U后，有r个主元列，n-r个自由列
  * U继续消元成新矩阵：|<span><sup>I F</sup><sub>0 0</sub></span>|。
  * 零空间（最终的解）：|<span><sup>-F</sup><sub>I</sub></span>|。有列交换则要注意还原
  * （A的列空间的维度是r，零空间的维度是n-r）
* 求解Ax=b，假设有r个主元列
  * r=n=m：R=I，唯一解
  * r=n<m：R=\|<span><sup>I</sup><sub>0</sub></span>|，唯一解或无解
  * r=m<n：R=(I 0)，无穷多解
  * r<n,r<m：R=\|<span><sup>I F</sup><sub>0 0</sub></span>|，无穷多解或无解

#### 4 Orthogonality(正交) 
* 正交向量：若向量x和y正交，则x<sup>T</sup>y=y<sup>T</sup>x=0，xy默认是列向量
  * 零向量与所有向量都正交
* 正交子空间：子空间S与子空间T正交，则S中的任意一个向量都和T中的任意向量正交。
  * 0空间和过原点的直线正交；
  * 经过原点的两条直线若夹角为直角则互相正交。
  * 矩阵的行空间的和零空间正交
  * （一个空间中正交子空间的维数之和不可能超过原空间的维数）
* 在R<sup>3</sup>空间内，A的列空间是一个平面，向量b在此平面的投影是p  
  * 投影矩阵P=A(A<sup>T</sup>A)<sup>-1</sup>A<sup>T</sup>
* 若A的列向量线性无关时，矩阵A<sup>T</sup>A为可逆矩阵。

![Alt text](image-3.jpg)
* 对于上图的三种求解思路：
  1. 从几何上讨论求解：直线上有三个点p1、p2、p3离原始三个点最近，根据p1、p2、p3来求C、D
  2. 最小二乘法矩阵法：向量b投影到矩阵A的列空间得到向量p，投影到矩阵零空间则是e
  3. 最小二乘法代数法：e1<sup>2</sup>+e2<sup>2</sup>+e3<sup>2</sup>表示三个点最小误差的平方和，[C代码实现](https://shatang.github.io/2020/09/05/%E6%9C%80%E5%B0%8F%E4%BA%8C%E4%B9%98%E6%B3%95/)
  4. 梯度下降法，见[机器学习——最小二乘法](https://www.cnblogs.com/BlairGrowing/p/14847772.html)
* 标准正交矩阵：列向量为标准正交向量
  * 什么是标准正交向量？向量长度都是1，且彼此正交
* 正交矩阵：必须是标准正交矩阵，必须是方阵。(正交矩阵是可逆矩阵)
* 如何推导P=Q(Q<sup>T</sup>Q)<sup>-1</sup>Q<sup>T</sup>
  * b向量在空间A的投影是p，b-p=e，e垂直于A，存在投影矩阵P使得p=Pb
  * 所以有A<sup>T</sup>(b-Ax)=0，得到A<sup>T</sup>Ax=A<sup>T</sup>b
  * 两侧都左乘(A<sup>T</sup>A)<sup>-1</sup>，得到x=(A<sup>T</sup>A)<sup>-1</sup>A<sup>T</sup>b
  * p=Ax，所以p=A(A<sup>T</sup>A)<sup>-1</sup>A<sup>T</sup>b
  * p=Pb，所以P=A(A<sup>T</sup>A)<sup>-1</sup>A<sup>T</sup>
* 如何简化P=Q(Q<sup>T</sup>Q)<sup>-1</sup>Q<sup>T</sup>
  * Q为可逆矩阵：P=QQ<sup>-1</sup>(Q<sup>T</sup>)<sup>-1</sup>Q<sup>T</sup>，P=I
  * Q为标准正交矩阵：所以有Q<sup>T</sup>Q=I，进而P=QQ<sup>T</sup>
* 施密特正交化：
  * 线性无关的a、b、c变成标准正交向量A、B、C
  * A = a
  * B = b-xA = b-(A<sup>T</sup>A)<sup>-1</sup>A<sup>T</sup>bA
  * C = c-xA-yB = c-(A<sup>T</sup>A)<sup>-1</sup>A<sup>T</sup>cA-(B<sup>T</sup>B)<sup>-1</sup>B<sup>T</sup>cB
  * 最后ABC除以自身的向量长度得到标准正交向量A、B、C

#### 5 Determinants(行列式)
* 行列式十条性质(只针对方阵)
  1. det(I)=1
  1. 行交换后，行列式会反号
  1. 以二阶方阵为例：
    * a，若某行乘以t则行列式也要乘t
    * b，其中一行不变，另一行可根据加法结合律拆分为两个矩阵
  1. 若存在相同的行，则行列式为0(性质2可推导)
  1. 某行减另一行的t倍，行列式不变(性质3、4可推导)
  1. 某行是零向量，则行列式为0(性质3可推导)
  1. 三角阵的行列式等于对角线数值的乘积(包含上三角和下三角)
  1. 有且仅当矩阵不可逆时，行列式为0
  1. det(AB)=det(A)*det(B)
  1. det(A<sup>T</sup>)=det(A)
* 行列式公式：∑<sub>n!</sub>±a<sub>1α</sub>a<sub>2β</sub>...a<sub>nω</sub>
  * 表示n阶方阵中，行列式等于n!个矩阵的行列式之和
  * 其中列标号（α, β, ...ω）是列标号（1, 2, ...n）的某个排列
* 代数余子式：det(A)=a<sub>11</sub>C<sub>11</sub>+a<sub>12</sub>C<sub>12</sub>+...a<sub>1n</sub>C<sub>1n</sub>
  * 对于a<sub>ij</sub>而言，C<sub>ij</sub>就是它的代数余子式
  * C<sub>ij</sub>表示去掉a<sub>ij</sub>的所在行和列得到的新矩阵的行列式*(-1)<sup>i+j</sup>
  * （C<sub>ij</sub>在i+j为偶数时为正，奇数时为负数。）
* 行列式计算的三种方法：
  * 通过消元得到主元，计算简单
  * 通过行列式公式计算，计算复杂
  * 通过代数余子式计算，计算适中
* 如何计算可逆矩阵的逆矩阵
  1. 高斯消元法：将 \[A I] 逐步消元成 \[I A<sup>-1</sup>]
  1. LU分解法：根据 A=LU 算出 A<sup>-1</sup>=U<sup>-1</sup>L<sup>-1</sup>
  1. QR分解法：根据 A=QR 算出 A<sup>-1</sup>=R<sup>-1</sup>Q<sup>-1</sup>
  1. 代数余子式：A<sup>-1</sup>=C<sup>T</sup>/det(A)
* 如何证明A<sup>-1</sup>=C<sup>T</sup>/det(A)
  * 两边都左乘A，得到AC<sup>T</sup>=det(A)I，继续证明这个等式
  * 可以发现AC<sup>T</sup>对角线都是det(A)，非对角线都是0，所以可证。
* 克莱姆法则：求解Ax=b
  * x=A<sup>-1</sup>b=C<sup>T</sup>b/det(A)
  * x<sub>j</sub>=det(B<sub>j</sub>)/det(A)，B<sub>j</sub>表示矩阵A的第j列用b代替
  * （克莱姆法则求解效率低，中看不中用）
* det(A)=矩阵A构成的几何体的体积
  * 单位矩阵：不管是几阶矩阵，体积都是1
  * 正交矩阵：边长为1，且边相互垂直，体积都是1

#### 6 Eigenvalues and Eigenvectors(特征值和特征向量) 
* 特征值和特征向量(只针对方阵)
  * 若存在Ax=λx，则λ是特征值，x是特征向量。
  * n阶矩阵有n个特征值(特征值可相同)
  * 例1：对于投影矩阵P，它的投影平面和垂直于平面的向量都是特征向量
  * 例2：2阶矩阵|<span><sup>0 1</sup><sub>1 0</sub></span>|，特征向量是(1 1)和(1 -1)

#### 7 The Singular Value Decomposition(奇异值分解) 

#### 8 Linear Transformations(线性变换) 

#### 9 Complex Vectors and Matrices(复向量和矩阵)

#### 10 Applications(应用)

#### 11 Numerical Linear Algebra(数值线性代数) 

#### 12 Linear Algebra in Probability & Statistics(概率统计中的线性代数)
