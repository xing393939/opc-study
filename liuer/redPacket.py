import numpy as np
import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from timeit import default_timer as timer
import matplotlib.pyplot as plt
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
start = timer()
device = torch.device("cuda:0")


# 1.prepare dataset
class DiabetesDataset(Dataset):
    def __init__(self, filepath):
        xy = np.loadtxt(filepath, skiprows=1, delimiter=",", dtype=np.float32)
        self.len = xy.shape[0]
        self.x_data = torch.from_numpy(xy[:, :-1]).to(device)
        self.y_data = torch.from_numpy(xy[:, [-1]]).to(device)

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.len


dataset = DiabetesDataset("redPacket.csv")
train_loader = DataLoader(dataset=dataset, batch_size=1024, shuffle=True)


# 2.design model using class
class Model(torch.nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.linear = torch.nn.Linear(4, 1)

    def forward(self, x):
        y_pred = torch.sigmoid(self.linear(x))
        return y_pred


model = Model().to(device)


# 3.construct loss and optimizer
criterion = torch.nn.BCELoss(reduction="mean")
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

epoch_list = []
loss_list = []
# 4.training cycle forward, backward, update
for epoch in range(10000):
    for i, data in enumerate(train_loader, 0):
        inputs, labels = data
        y_pred = model(inputs)
        loss = criterion(y_pred, labels)
        if epoch % 100 == 0 and i == 0:
            print("epoch %9d error %.3f" % (epoch, loss.item()), model.linear.weight.data, model.linear.bias.data)
            epoch_list.append(epoch)
            loss_list.append(loss.item())

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

# 5.test
print("w = ", model.linear.weight.data)
print("b = ", model.linear.bias.data)
x_test = torch.Tensor([1903610565, 17100051503, 41, 8.7]).to(device)
y_test = model(x_test)
print("y_pred = ", y_test.data)
print("cost = ", timer() - start)

plt.plot(epoch_list, loss_list)
plt.ylabel("loss")
plt.xlabel("epoch")
plt.show()
