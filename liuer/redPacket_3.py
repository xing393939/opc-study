import numpy as np
import torch

# 1.prepare dataset
xy = np.loadtxt("0.csv", skiprows=1, delimiter=",", dtype=np.float32)
x_data = torch.from_numpy(xy[:, :-1])
y_data = torch.from_numpy(xy[:, [-1]])


# 2.design model using class
class Model(torch.nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.linear1 = torch.nn.Linear(4, 2)
        self.linear2 = torch.nn.Linear(2, 1)
        self.activate = torch.nn.ReLU()
        self.sigmoid = torch.nn.Sigmoid()

    def forward(self, x):
        x = self.sigmoid(self.linear1(x))
        x = self.sigmoid(self.linear2(x))
        return x


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = Model().to(device)
x_data = x_data.to(device)
y_data = y_data.to(device)

# 3.construct loss and optimizer
criterion = torch.nn.BCELoss(reduction="mean")
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# 4.training cycle forward, backward, update
for epoch in range(100000):
    y_pred = model(x_data)
    loss = criterion(y_pred, y_data)
    if epoch % 1000 == 0:
        print(
            "epoch %9d loss %.3f" % (epoch, loss.item()),
            model.linear2.weight.data,
            model.linear2.bias.data,
        )

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
