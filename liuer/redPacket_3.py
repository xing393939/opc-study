import numpy as np
import torch
import matplotlib.pyplot as plt
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

# 1.prepare dataset
xy = np.loadtxt("redPacket_2.csv", skiprows=1, delimiter=",", dtype=np.float32)
x_data = torch.from_numpy(xy[:, :-1])  # 第一个‘：’是指读取所有行，第二个‘：’是指从第一列开始，最后一列不要
y_data = torch.from_numpy(xy[:, [-1]])  # [-1] 最后得到的是个矩阵


# 2.design model using class
class Model(torch.nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.linear1 = torch.nn.Linear(4, 2)  # 输入数据x的特征是8维，x有8个特征
        self.linear3 = torch.nn.Linear(2, 1)
        # self.activate = torch.nn.ReLU()
        self.sigmoid = torch.nn.Sigmoid()  # 将其看作是网络的一层，而不是简单的函数使用

    def forward(self, x):
        # x = self.activate(self.linear1(x))
        # x = self.activate(self.linear2(x))
        x = self.sigmoid(self.linear1(x))
        x = self.sigmoid(self.linear3(x))  # y hat
        return x


device = torch.device("cuda:0")
model = Model().to(device)
x_data = x_data.to(device)
y_data = y_data.to(device)

# 3.construct loss and optimizer
criterion = torch.nn.BCELoss(reduction="mean")
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

epoch_list = []
loss_list = []
# 4.training cycle forward, backward, update
for epoch in range(1000000):
    y_pred = model(x_data)
    loss = criterion(y_pred, y_data)
    if epoch % 10000 == 0:
        print(
            "epoch %9d error %.3f" % (epoch, loss.item()),
            model.linear3.weight.data,
            model.linear3.bias.data,
        )
        epoch_list.append(epoch)
        loss_list.append(loss.item())

    optimizer.zero_grad()
    loss.backward()

    optimizer.step()

# 5.test
print("w = ", model.linear3.weight.data)
print("b = ", model.linear3.bias.data)
x_test = torch.Tensor(
    [0.17647, 0.25628, 0.14754, -0.474747, -0.72813, -0.073025, -0.891546, -0.33333]
).to(device)
y_test = model(x_test)
print("y_pred = ", y_test.data)
x_test = torch.Tensor(
    [-0.0588235, -0.00502513, 0.377049, 0, 0, 0.0551417, -0.735269, -0.0333333]
).to(device)
y_test = model(x_test)
print("y_pred = ", y_test.data)

plt.plot(epoch_list, loss_list)
plt.ylabel("loss")
plt.xlabel("epoch")
plt.show()
