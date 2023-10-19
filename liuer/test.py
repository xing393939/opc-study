from matplotlib import pyplot as plt  # 调用matplotlib库的pyplot
import numpy as np


def get_beans(counts):  # 构造吃豆豆的函数
    xs = np.random.rand(counts)
    xs = np.sort(xs)  # 进行行排序
    ys = np.array([(0.7 * x + (0.5 - np.random.rand()) / 5 + 0.5) for x in xs])
    return xs, ys


m = 100
xs, ys = get_beans(m)  # 获取100个豆子数据

w = 0.1
b = 0.1
for m in range(500):  # 调整500次全部，0-99的整数，用range 函数进行for循环
    for i in range(100):  # 调整1次全部，可能会导致线不拟合
        x = xs[i]
        y = ys[i]
        # a=x^2
        # b=-2*x*y
        # c=y^2
        # 斜率k=2aw+b
        alpha = 0.01  # 学习率，学习率不可过大也不可过小
        dw = 2 * x**2 * w + 2 * x * (b - y)  # 对w求偏导
        db = 2 * b + 2 * x * w - 2 * y  # 对b求偏导
        w = w - alpha * dw  # 梯度下降
        b = b - alpha * db  # 梯度下降

plt.scatter(xs, ys)

y_pre = w * xs + b
plt.xlim(0, 1)  # plt.xlim()函数限制x轴范围
plt.ylim(0, 1.5)  # plt.ylim()函数限制y轴范围
plt.plot(xs, y_pre)

plt.show()
