### 傅里叶变换

#### 一维离散傅里叶变换DFT
* [2022-04-16 一维离散傅里叶变换DFT - 手算过程](https://juejin.cn/post/7087486616469504036)

![Alt text](image-5.png)

![Alt text](image-6.png)

```python
# python实现的一维离散傅里叶变换
# DFT_slow等价于np.fft.fft
import numpy as np

def DFT_slow(x):
    x = np.asarray(x, dtype=float)
    N = x.shape[0]
    n = np.arange(N)
    k = n.reshape((N, 1))
    M = np.exp(-2j * np.pi * k * n / N)
    return np.dot(M, x)

x = np.array([1,2,3])
y = DFT_slow(x)
print(y)
print(np.fft.fft(x))
```