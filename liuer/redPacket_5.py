import numpy as np
import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from timeit import default_timer as timer
import torch.nn.functional as F
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
start = timer()
device = torch.device("cpu" if torch.cuda.is_available() else "cpu")

scaler = StandardScaler(with_mean=True, with_std=True)
scaler.mean_ = [
    1.08554986e02,
    1.29016179e02,
    1.20727032e02,
    1.13427473e02,
    1.66467707e04,
    1.54938078e03,
    7.50659189e00,
]
scaler.var_ = [
    2.00737537e03,
    5.77710843e03,
    6.25343194e03,
    5.21506444e03,
    1.29878058e06,
    2.81938577e08,
    1.50334197e02,
]
scaler.scale_ = [
    4.48037428e01,
    7.60072919e01,
    7.90786440e01,
    7.22154031e01,
    1.13964055e03,
    1.67910267e04,
    1.22610846e01,
]


# 1.prepare dataset
class DiabetesDataset(Dataset):
    def __init__(self, filepath):
        xy = np.loadtxt(filepath, skiprows=1, delimiter=",", dtype=np.float32)
        self.len = xy.shape[0]
        x_data = scaler.transform(xy[:, :-1])
        self.x_data = torch.from_numpy(x_data).to(device)
        self.y_data = torch.from_numpy(xy[:, [-1]]).to(device)

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.len


dataset = DiabetesDataset("redPacket_train.csv")
train_loader = DataLoader(dataset=dataset, batch_size=64, shuffle=True)


# 2.design model using class
class Model(torch.nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.conv1 = torch.nn.Linear(7, 8)
        self.conv2 = torch.nn.Linear(8, 7)
        self.linear1 = torch.nn.Linear(7, 4)
        self.linear2 = torch.nn.Linear(4, 1)
        self.activate = torch.nn.ReLU()
        self.sigmoid = torch.nn.Sigmoid()

    def forward(self, x):
        y = self.conv1(x)
        y = self.activate(y)
        y = self.conv2(y)
        x = self.activate(x + y)
        x = self.linear1(x)
        x = self.activate(x)
        x = self.linear2(x)
        x = self.sigmoid(x)
        return x


model = Model().to(device)


# 3.construct loss and optimizer
criterion = torch.nn.BCELoss(reduction="mean")
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

epoch_list = []
loss_list = []
# 4.training cycle forward, backward, update
for epoch in range(50):
    running_loss = 0.0
    running_i = 0
    for i, data in enumerate(train_loader, 0):
        inputs, labels = data
        y_pred = model(inputs)
        loss = criterion(y_pred, labels)
        running_loss += loss.item()
        running_i = i + 1
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(
        "%d %d loss: %.3f" % (epoch, running_i, running_loss / running_i),
        model.linear2.weight.data,
        model.linear2.bias.data,
    )
    epoch_list.append(epoch)
    loss_list.append(running_loss / running_i)

# 5.test
print("cost = ", timer() - start)
dataset = DiabetesDataset("redPacket_test.csv")
train_loader = DataLoader(dataset=dataset, batch_size=99999)
with torch.no_grad():
    for i, data in enumerate(train_loader, 0):
        inputs, labels = data
        y_pred = model(inputs)
        y_pred = y_pred.cpu().numpy()
        y_pred = (y_pred > 0.5).astype(np.float32)
        num_right = np.sum(y_pred == labels.cpu().numpy())
        print(num_right / len(labels))

plt.plot(epoch_list, loss_list)
plt.ylabel("loss")
plt.xlabel("epoch")
plt.show()
