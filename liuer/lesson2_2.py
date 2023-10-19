import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

x_data = [1.0, 2.0, 3.0]
y_data = [2.0, 4.0, 6.0]


def forward(x):
    return x * w + b


def loss(x, y):
    y_pred = forward(x)
    return (y_pred - y) * (y_pred - y)


w_list = np.arange(0.0, 4.0, 0.1)
b_list = np.arange(-2, 2.0, 0.1)
w, b = np.meshgrid(w_list, b_list)

l_sum = 0
for x_val, y_val in zip(x_data, y_data):
    loss_val = loss(x_val, y_val)
    l_sum += loss_val
    print(l_sum)
mse = l_sum / 3

fig = plt.figure()
ax = Axes3D(fig, auto_add_to_figure=False)
fig.add_axes(ax)
surf = ax.plot_surface(
    w, b, mse, rstride=1, cstride=1, cmap="coolwarm", linewidth=0, antialiased=False
)
# fig.colorbar(surf, shrink=0.5, aspect=5)
ax.set_xlabel("w")
ax.set_ylabel("b")
plt.title("loss")
plt.show()
