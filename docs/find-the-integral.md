### 求积分

<script>
  MathJax = {
    tex: {
      inlineMath: [['$', '$'], ['\\(', '\\)']],
      displayMath: [["$$", "$$"], ["\\[", "\\]"]],
    },
    options: {
      skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'a', 'annotation', 'annotation-xml']
    },
    svg: {
      fontCache: 'global'
    }
  };
</script>
<script id="MathJax-script" type=text/javascript src="../images/js/tex-mml-chtml.js"></script>

#### 参考资料
* [积分法则](https://www.shuxuele.com/calculus/integration-rules.html)
* [分部积分法](https://www.shuxuele.com/calculus/integration-by-parts.html)
* [换元积分法](https://www.shuxuele.com/calculus/integration-by-substitution.html)

#### 常用函数
* $\ln x$表示以自然数e为底的对数

| 函数               | 积分                  |
|------------------|---------------------|
| $∫x^n dx$        | $x^{n+1}/(n+1) + C$ |
| $∫\sin x dx$     | $-\cos x + C$       |
| $∫\cos x dx$     | $\sin x + C$        |
| $∫\rm e^{cx} dx$ | $\rm e^{cx}/c + C$  |
| $∫\ln x dx$      | $x\ln x - x + C$    |

#### 常用法则

| 法则   | 函数            | 积分                       |
|------|---------------|--------------------------|
| 乘以常量 | $∫cf(x) dx$   | $c∫f(x) dx$              |
| 和法则  | $∫(f + g) dx$ | $∫f dx + ∫g dx$          |
| 差法则  | $∫(f - g) dx$ | $∫f dx - ∫g dx$          |
| 乘法则  | $∫u.v dx$     | $u∫v dx - ∫u'(∫v dx) dx$ |

#### 分部积分法
* 也称乘法则：$∫u.v dx = u∫v dx - ∫u'(∫v dx) dx$
```
$$
\begin{flalign}
∫x \cos(x) dx &= x.\sin(x) - ∫\sin(x)dx \qquad u=x \;\; v=\cos(x)\\
&= x\sin(x) + \cos(x) + C &
\end{flalign}
$$
```

#### 换元积分法
* 换元积分法：$∫f(g(x))g'(x) dx = ∫f(u) du$
```
$$
\begin{flalign}
∫x \cos(x^2)2x dx &= ∫\cos(u)du \qquad u=x^2 \\
&= \sin(u) + C \\
&= \sin(x^2) + C &
\end{flalign}
$$
```