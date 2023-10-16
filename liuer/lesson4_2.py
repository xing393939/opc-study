import random
import matplotlib.pyplot as plt

x_data = [1.0, 2.0, 3.0]
y_data = [2.0, 4.0, 6.0]

w = 1.0
b = 1.0

def forward(x):
    return x * w + b

# calculate loss function
def loss(x, y):
    y_pred = forward(x)
    return (y_pred - y) ** 2

# 计算梯度（随机梯度下降）
def gradient_w(x, y):
    return 2 * x * x * w + 2 * x * b - 2 * x * y

def gradient_b(x, y):
    return 2 * b + 2 * x * w - 2 * y

epoch_list = []
loss_list = []
print('predict (before training)', 4, forward(4))
for epoch in range(500):
   for x, y in zip(x_data, y_data):
      dw = gradient_w(x, y)
      db = gradient_b(x, y)
      w = w - 0.01 * dw
      b = b - 0.01 * db
      l = loss(x, y)
      epoch_list.append(epoch)
      loss_list.append(l)

print('predict (after training)', 'w=', w, 'b=', b, 4, forward(4))
plt.plot(epoch_list, loss_list)
plt.ylabel('loss')
plt.xlabel('epoch')
plt.show()