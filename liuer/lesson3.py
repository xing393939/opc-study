from matplotlib import pyplot as plt

# prepare the training set
x_data = [1.0, 2.0, 3.0]
y_data = [2.0, 4.0, 6.0]

# initial guess of weight
w = 1.0


# define the model linear model y = w*x
def forward(x):
    return x * w


# define the cost function MSE(均方差）
def cost(xs, ys):
    cost = 0
    for x, y in zip(xs, ys):
        y_pred = forward(x)
        cost += (y_pred - y) ** 2
    return cost / len(xs)


# 计算梯度
def gradient(xs, ys):
    grad = 0
    for x, y in zip(xs, ys):
        grad += 2 * x * (x * w - y)
    return grad / len(xs)


epoch_list = []
cost_list = []
print("Predict (before training)", 4, forward(4))
for epoch in range(100):
    cost_val = cost(x_data, y_data)
    grad_val = gradient(x_data, y_data)
    w -= 0.01 * grad_val
    print("Epoch:", epoch, "w=", w, "loss=", cost_val)
    epoch_list.append(epoch)
    cost_list.append(cost_val)

print("Predict (after training)", 4, forward(4))
plt.plot(epoch_list, cost_list)
plt.xlabel("Epoch")
plt.ylabel("cost")
plt.show()
