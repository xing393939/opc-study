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
  src="https://static-621585.oss-cn-beijing.aliyuncs.com/mathjax-v3.js">
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
  * 例：$y = x^2 \to \frac{dy}{dx} = 2x \to \frac{d^2y}{dx^2} = 2 $
  * 例：$y = \sin x \quad\to y' = \cos x \quad\quad\to y'' = -\sin x $
  * 例：$y = x^3 - x^2 \to y' = 3x^2 - 2x \to y'' = 6x -2 $
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
* P8.链式法则：$z = f(y)\,y = g(x) => \frac{dz}{dx} = \frac{dz}{dy} \frac{dy}{dx}$
* P9.极限和连续
  * 四种极限的特性情况：
    * $a_n - b_n$：∞ - ∞
    * $a_n \* b_n$：0 \* ∞
    * $a_n / b_n$：0 / 0 或者 ∞ / ∞
    * $a_n^{b_n}$：0 ^ 0 或者 1 ^ ∞
  * 函数连续性的定义：对于任意的ϵ > 0，存在δ > 0，如果∣x − a∣ < δ，那么∣f(x) − f(a)∣ < ϵ 
* P10.逆函数和对数函数
  * 逆函数：y=f(x)的逆函数是x=f<sup>−1</sup>(y)
    * 例1：$y=x^2 \quad=> x=\sqrt{y}$
    * 例2：$A=πr^2 => r=\sqrt{\frac{A}{π}} $ 
    * 例3：$y=e^x \quad=> x=\ln y$
  * 对数函数
    * 性质1：$\ln (AB) = \ln A + \ln B$
    * 性质2：$\ln (y^n) = n\ln y$
* P11.对数函数和反三角函数的导数
  * 对数函数：$\frac{d}{dx} (\ln x) = \frac{1}{x}$
    
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

