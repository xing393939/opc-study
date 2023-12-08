### 微积分重点

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
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
</script>

#### 参考资料
* 如果要认真学微积分，其实应该学MIT的1801和1802，但是两门课加起来有70节课，所以选择了本课，本课主要涉及单变量微积分。
* [LaTeX公式手册(全网最全)](https://www.cnblogs.com/1024th/p/11623258.html)
* [学习笔记1](https://www.zhihu.com/column/c_1165312843926171648)
* [学习笔记2](https://blog.csdn.net/shamozhizhoutx/article/details/125126766)

#### 课程笔记1
* 自然常数e：e = 2.718...
  * $(1 + \frac{1}{x})^x$无限趋近于e
* P2.三个重要函数的斜率
  1. $y = x^n \quad=> \frac{dy}{dx} = nx^{n-1}$
  1. $y = \sin x => \frac{dy}{dx} = \cos x$
  1. $y = e^x \quad=> \frac{dy}{dx} = e^x$
* P3.极值和二阶导数
  * 一阶导数可以找到极值，二阶导数告知它是极大值还是极小值
  * 例：$y = x^2 \quad\quad=> y' = 2x \quad\quad\quad=> y'' = 2 $
  * 例：$y = \sin x \quad=> y' = \cos x \quad\quad=> y'' = -\sin x $
  * 例：$y = x^3 - x^2 => y' = 3x^2 - 2x => y'' = 6x -2 $
* P4.指数函数
  * $e = (1 + \frac{1}{x})^x$。在银行存￥1，年利率100%，求一年后的复利
  * 假设一年计息4次，最后本息是$(1 + \frac{1}{4})^4$
  * 假设一年计息x次，最后的本息无限趋近于e
  
#### 课程笔记2
* P5.积分总览
  * 求积分的方法A：例如知道2x的导数是2，则已知导数2就可以反推
  * 求积分的方法B：函数一y的值 = 函数二的面积
* P6.求sinx和cosx的导数
  * $f'(\sin x)=\cos x$
  * $f'(\cos x)=\lim\limits_{\Delta x \to 0} \frac{f(x+\Delta x)-f(x)}{\Delta x}$
  * $\quad\quad\quad\quad=\lim\limits_{\Delta x \to 0} \frac{\cos(x+\Delta x)-\cos x}{\Delta x}$
  * $\quad\quad\quad\quad=\lim\limits_{\Delta x \to 0} \frac{\cos x\cos\Delta x-\sin x\sin \Delta x-\cos x}{\Delta x}$
  * $\quad\quad\quad\quad=\lim\limits_{\Delta x \to 0} \frac{\cos x(\cos\Delta x-1)-\sin x\sin \Delta x}{\Delta x}$
  * $\quad\quad\quad\quad=\lim\limits_{\Delta x \to 0} \left\[\cos x\frac{(\cos\Delta x-1)}{\Delta x}-\sin x\frac{\sin \Delta x}{\Delta x}\right\]$
  * $\quad\quad\quad\quad=\cos x\cdot0-\sin x\cdot1$
  * $\quad\quad\quad\quad=-\sin x$
* P7.乘法法则和除法法则
  * $(f + g)' = f' + g'$
  * $(f - g)' = f' - g'$
  * $(f * g)' = f'g + g'f$
  * $(f / g)' = \frac{f'g - g'f}{g^2}$
* P8.链式法则：$z = f(y) \quad y = g(x) => \frac{dz}{dx} = \frac{dz}{dy} \frac{dy}{dx}$
* P9.极限和连续
  * 四种极限的特殊情况：
    * $a_n - b_n$：∞ - ∞
    * $a_n \* b_n$：0 \* ∞
    * $a_n / b_n$：0 / 0 或者 ∞ / ∞
    * $(a_n)^{b_n}$：0 ^ 0 或者 1 ^ ∞
  * 函数连续性的定义：对于任意的ϵ > 0，存在δ > 0，如果∣x − a∣ < δ，那么∣f(x) − f(a)∣ < ϵ 
* P10.逆函数和对数函数
  * 逆函数：y=f(x)的逆函数是x=f<sup>−1</sup>(y)
    * 例1：$y=x^2 \quad=> x=\sqrt{y}$
    * 例2：$A=πr^2 \; => r=\sqrt{\frac{A}{π}} $ 
    * 例3：$y=e^x \quad=> x=\ln y$
  * 对数函数
    * 性质1：$\ln (AB) = \ln A + \ln B$
    * 性质2：$\ln (y^n) = n\ln y$
* P11.对数函数和反三角函数的导数
  * 对数函数：$\frac{d}{dx} (\ln x) = \frac{1}{x}$，推导如下：
    * $x=ln y$的构造函数：$y=e^x => y=e^{\ln y}$，两边分别求导可得
    * $1 = \frac{d}{dy} (e^{\ln y})$
    * $e^{\ln y} \frac{d}{dy} (\ln y) = 1$
    * $y \frac{d}{dy} (\ln y) = 1$
    * $\frac{d}{dy} (\ln y) = \frac{1}{y}$
  * 反三角函数1：$\frac{d}{dx}(\sin^{-1}x)=\frac{1}{\sqrt{1-x^2}}$，推导如下：
    * $x = \sin^{-1}y$的构造函数：$y = \sin x => y = \sin(\sin^{-1}y)$，两边分别求导可得
    * $1 = \cos(\sin^{-1}y) \frac{d}{dy} \sin^{-1}y $
    * $1 = \sqrt{1-y^2} \frac{d}{dy} \sin^{-1}y $
    * $\frac{d}{dy}(\sin^{-1}y)=\frac{1}{\sqrt{1-y^2}}$
  * （证明$\cos(\sin^{-1}y) = \sqrt{1-y^2}$）  
    * $(\sin θ)^2 + (\cos θ)^2 = 1$，令sinθ=y，则cosθ=cos(sin<sup>-1</sup>y)
    * 可得：$\cos(\sin^{-1}y) = \sqrt{1-y^2}$
  * 反三角函数2：$\frac{d}{dx}(\cos^{-1}x)=-\frac{1}{\sqrt{1-x^2}}$
  
#### 课程笔记3
* P12.增长率和对数图
  * y=x<sup>1.5</sup>，两边同时求对：log y=1.5 * log x
    * 对数图：x轴是log x，y轴是log y，是一条直线
  * y=B * 10<sup>cx</sup>，两边同时求对：log y=log B + cx
    * 对数图：x轴是x，y轴是log y，是一条直线
* P13.线性近似和牛顿法
  * 线性近似：假设选定一个x，求f(x)的值
    * $f'(a) ≈ \frac{f(x) - f(a)}{x - a}$，a为x附近的一个点
    * 例如：求$\sqrt{9.06}$，取a=9可得：
    * $\frac{1}{2\sqrt{9}} ≈ \frac{f(x) - \sqrt{9}}{9.06 - 9}$
    * 最终f(x) ≈ 3.01
  * 牛顿法：求f(x)=0的解
    * 由线性近似的公式可得：$x ≈ a - \frac{f(a)}{f'(a)}$
    * 例如：求x<sup>2</sup> - 9.06 = 0的解，取a=3可得
    * $x = 3 - \frac{-0.06}{2 * 3} = 3.01$
    * 可令a = 3.01继续求解，则可以得到更精确的值
  
#### 课程笔记4
* P14.幂级数及欧拉公式
  * x=a的幂级数：$a_0 + a_1(x - a) + a_2(x - a)^2 + a_3(x - a)^3 + ...$
  * x=0的幂级数：$a_0 + a_1(x) + a_2(x)^2 + a_3(x)^3 + ...$
  * 泰勒级数的[定义](../images/taylor-series.jpg)
  * f(x)关于x=0的泰勒级数：$f(x) = f(0) + f'(0)x + \frac{f''(0)}{2!}x^2 + \frac{f'''(0)}{3!}x^3 + ...$
    * $e^x = 1 + x + \frac{1}{2!}x^2 + \frac{1}{3!}x^3 + ...$，e<sup>x</sup>的所有导数在x=0处都是1
    * $\sin x = x - \frac{1}{3!}x^3 + \frac{1}{5!}x^5 - \frac{1}{7!}x^7 + ...$
    * $\cos x = 1 - \frac{1}{2!}x^2 + \frac{1}{4!}x^4 - \frac{1}{6!}x^6 + ...$
  * 欧拉公式：$e^{ix} = \cos x + i\sin x$，推导如下：
    * $e^{ix} = 1 + ix + \frac{1}{2!}(ix)^2 + \frac{1}{3!}(ix)^3 + \frac{1}{4!}(ix)^4 + ...$
    * $e^{ix} = 1 + ix - \frac{1}{2!}x^2 - \frac{i}{3!}x^3 + \frac{1}{4!}x^4 + ...$
    * $e^{ix} = (1 - \frac{1}{2!}x^2 + \frac{1}{4!}x^4 + ...) + i(x - \frac{1}{3!}x^3 + ...) $
    * $e^{ix} = \cos x + i\sin x$
  * 几何级数及其积分
    * $\frac{1}{1-x} = 1 + x + x^2 + x^3 + ...$，当|x|<1时成立
    * $-\ln(1-x) = x + \frac{x^2}{2} + \frac{x^3}{3} + ...$，当|x|<1时成立

#### 课程笔记5
* P15.关于运动的微分方程
  * 本节讲的是常系数线性二阶微分方程：$m\frac{d^2y}{dt^2} + 2r\frac{dy}{dt} + ky = 0$
    * 常系数：指y和n阶导数前的系数都是常数
    * 线性：指y和n阶导数的幂都是1
    * 二阶微分：最多是二阶导数
  * 当m=0时，$\frac{dy}{dt} = ay$，该微分方程的解为：$y = Ce^{at}$，C为任意值
  * 当r=0时，$\frac{d^2y}{dt^2} = -ω^2y$，该微分方程的解为：$y = C\cos (wt)$或$y = D\sin (wt)$
  * 当r=0,k=0时，$\frac{d^2y}{dt^2} = 0$，该微分方程的解为：y = C + Dt
  * 求解常系数线性二阶微分方程，令$y = e^{λt}$可得：
    * $mλ^2e{λt} + 2rλe^{λt} + ke^{λt} = 0$
    * $mλ^2 + 2rλ + k = 0$
    * $λ_{1,2} = \frac{-r±\sqrt{r^2-km}}{m}$
  * 求解1：y'' + 6y' + 8y = 0
    * $λ^2 + 6λ + 8 = 0$，可得λ=-2或λ=-4
    * $y = Ce^{-2t} + De^{-4t}$
  * 求解2：y'' + 6y' + 10y = 0
    * $λ = \frac{-6±\sqrt{36-40}}{2}$，可得λ=-3±i
    * $y = Ce^{(-3+i)t} + De^{(-3-i)t}$
  * 求解3：y'' + 6y' + 9y = 0
    * $λ^2 + 6λ + 9 = 0$，可得λ=-3
    * $y = Ce^{-3t} + Dte^{-3t}$
* P16.关于人口增长的微分方程
  1. 存款利息问题：$\frac{dy}{dt} = cy$，可得$y = Ae^{ct}$
    * $y(0) = A$，可得$y = y(0)e^{ct}$
    * y(t)：存储账号的钱；y(0)初始金额；c：年利息
    * 假设y(0)=10000, c=0.03，则y(1)=10304.545
  1. 增长可积累或者有消耗：$\frac{dy}{dt} = cy + s$，s>0表示增长可积累，s<0表示增长有消耗
    * $\frac{d}{dt}(y + \frac{s}{c}) = c(y + \frac{s}{c})$
    * $y + \frac{s}{c} = (y(0) + \frac{s}{c})e^{ct}$
    * $y = -\frac{s}{c} + (y(0) + \frac{s}{c})e^{ct}$
  1. 人口增长模型：$\frac{dP}{dt} = cP - sP^2$，c是出生率-死亡率，s是人口因竞争而减少的系数
    * 令$y = \frac{1}{P}$可得：$\frac{dy}{dt} = \frac{dy}{dP}\frac{dP}{dt} = -\frac{1}{P^2}(cP - sP^2)$
    * $\frac{dy}{dt} = -(\frac{c}{P} - s) = -(cy - s)$
    * $y = \frac{s}{c} + (y(0) - \frac{s}{c})e^{ct}$，再带入$y = \frac{1}{P}$可得P
  1. 捕食-猎物模型：$\frac{du}{dt} = -cu + suv \quad \frac{dv}{dt} = cv - suv$
    * u(t)：捕食者的种族数量变化；v(t)：猎物的种族数量变化

#### 课程笔记6
| 积分 | 六函数 | 导数 |
|------|-------|------|
| $x^{n+1}/(n+1)$ | $x^n$ | $nx^{n-1}$ |
| $-\cos x$ | $\sin x$ | $\cos x$ |
| $\sin x$ | $\cos x$ | $-\sin x$ |
| $\rm e^{cx}/c$ | $\rm e^{cx}$ | $c\rm e^{cx}$ |
| $x\ln x - x$ | $\ln x$ | $1/x$ |
| 斜坡函数<br>Ramp function | 阶跃函数<br>Step function | 冲激函数<br>Delta function |

* 六法则
  1. 加法法则：$af(x)+bg(x)$ 的导数为$a\frac{df}{dx} + b\frac{dg}{dx}$
  2. 乘法法则：$f(x)g(x)$ 的导数为$\frac{df}{dx}g(x) + f(x)\frac{dg}{dx}$
  3. 除法法则：$f(x)/g(x)$ 的导数为$(\frac{df}{dx}g - f\frac{dg}{dx})/{g^2}$
  4. 链式法则：$f(g(x))$ 的导数为$\frac{df}{dy}\frac{dy}{dx}$，其中y=g(x)
  5. 逆函数法则：$x=f^{-1}(y)$ 的导数为$\frac{dx}{dy}=\frac{1}{dy/dx}$
  6. 洛必达法则：当x→a，f(x)→0和g(x)→0时，如何求f(x)/g(x)：$\lim\limits_{x\to a}\frac{f(x)}{g(x)}=\frac{df/dx}{dg/dx}=\frac{f'(x)}{g'(x)}$
* 六定理
  1. 微积分的第一基本定理：若$f(x)=\int^x_a s(t)dt$，则$\frac{df}{dx}=s(x)$，$\int$是[积分符号](https://baike.baidu.com/item/%E7%A7%AF%E5%88%86%E5%85%AC%E5%BC%8F/8556651)
  1. 微积分的第二基本定理：若$\frac{df}{dx}=s(x)$，则$\int^b_a s(t)dt=f(b)-f(a)$
  1. 全值定理：假设函数f(x)在闭区间\[a,b]内连续，f(x)可以取到的最大值M最小值m，那么f(x)可以取到M和m之间的所有值。
  1. 中值定理：假设函数f(x)在闭区间\[a,b]内连续，在[开区间](https://www.runoob.com/w3cnote/programming-range.html)\(a,b)可导，则\(a,b)内至少有一点c使得$f'(c)=\frac{f(b)-f(a)}{b-a}$
  1. 泰勒级数：f(x)关于x=a的泰勒级数：$f(x) = f(a) + f'(a)(x-a) + \frac{f''(a)}{2!}(x-a)^2 + \frac{f'''(a)}{3!}(x-a)^3 + ...$
  1. 两项式定理：$(1+x)^p$在x=0处的导数是：p、p(p-1)、p(p-1)(p-2)...，用泰勒公式展开可得：$(1+x)^p=1+px+\frac{p(p-1)}{2!}x^2+\frac{p(p-1)(p-2)}{3!}x^3+...$
    * p=1则有$(1+x)^1 = 1 + x$
    * p=2则有$(1+x)^2 = 1 + 2x + x^2$
    * p=3则有$(1+x)^3 = 1 + 3x + 3x^2 + x^3$
    * p=4则有$(1+x)^4 = 1 + 4x + 6x^2 + 4x^3 + x^4$
