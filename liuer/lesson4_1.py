import torch
from matplotlib import pyplot as plt
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

x_data = [1.0, 2.0, 3.0]
y_data = [2.0, 4.0, 6.0]
w1 = torch.Tensor([1.0])
w1.requires_grad = True
w2 = torch.Tensor([1.0])
w2.requires_grad = True
b = torch.Tensor([1.0])
b.requires_grad = True


def forward(x):
    return w1 * x**2 + w2 * x + b


def loss(x, y):
    y_pred = forward(x)
    return (y_pred - y) ** 2


print("Predict (befortraining)", 4, forward(4))
l_lost = []
epoch_list = []
for epoch in range(100):
    l = loss(1, 2)  # 为了在for循环之前定义l,以便之后的输出，无实际意义
    for x, y in zip(x_data, y_data):
        l = loss(x, y)
        l.backward()
        print("\tgrad:", x, y, w1.grad.item(), w2.grad.item(), b.grad.item())
        w1.data = w1.data - 0.01 * w1.grad.data  # 注意这里的grad是一个tensor，所以要取他的data
        w2.data = w2.data - 0.01 * w2.grad.data
        b.data = b.data - 0.01 * b.grad.data
        w1.grad.data.zero_()  # 释放之前计算的梯度
        w2.grad.data.zero_()
        b.grad.data.zero_()
    epoch_list.append(epoch)
    l_lost.append(l.item())
    print("Epoch:", epoch, l.item())

print("Predict(after training)", 4, forward(4).item())
plt.plot(epoch_list, l_lost)
plt.xlabel("Epoch")
plt.ylabel("lost")
plt.show()
