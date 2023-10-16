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
for epoch in range(2000):
    rc = random.randrange(0, 3)
    x1 = x_data[rc]
    y1 = y_data[rc]
    grad_w = gradient_w(x1, y1)
    grad_b = gradient_b(x1, y1)
    w = w - 0.01 * grad_w
    b = b - 0.01 * grad_b
    l = loss(x1, y1)
    epoch_list.append(epoch)
    loss_list.append(l)

print('predict (after training)', 'w=', w, 'b=', b, 4, forward(4))
plt.plot(epoch_list, loss_list)
plt.ylabel('loss')
plt.xlabel('epoch')
plt.show()