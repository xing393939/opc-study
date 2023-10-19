import numpy as np
import matplotlib.pyplot as plt

x_data = [1.0, 2.0, 3.0]
y_data = [2.0, 4.0, 6.0]


# 前馈函数
def forward(x):
    return x * w


# 损失函数
def loss(x, y):
    y_pred = forward(x)
    return (y_pred - y) * (y_pred - y)


w_list = []  # 参数值w
mse_list = []  # 随着参数值变化产生的均方差

for w in np.arange(0.0, 4.1, 0.1):
    print("w=", w)
    l_sum = 0
    # 将x_data, y_data打包成一个个元组（x_val, y_val）
    # 其实就是每次对每个list取一个值放入x_val和y_val
    for x_val, y_val in zip(x_data, y_data):
        y_pred_val = forward(x_val)
        loss_val = loss(x_val, y_val)
        l_sum += loss_val
        print("\t", x_val, y_val, y_pred_val, loss_val)
    print("MSE=", l_sum / 3)
    w_list.append(w)
    mse_list.append(l_sum / 3)
plt.plot(w_list, mse_list)
plt.ylabel("Loss")
plt.xlabel("w")
plt.show()
