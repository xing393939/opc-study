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


# 2.design model using class
class Model(torch.nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.rnn = torch.nn.RNN(
            input_size=8,
            hidden_size=50,
            num_layers=5,
        )
        self.linear1 = torch.nn.Linear(50, 20)
        self.linear2 = torch.nn.Linear(20, 1)
        self.activate = torch.nn.ReLU()
        self.sigmoid = torch.nn.Sigmoid()

    def forward(self, x):
        hidden = torch.zeros(5, 50, dtype=torch.float)
        x, _ = self.rnn(x, hidden)
        x = x.view(-1, 50)
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
inputs = torch.tensor(
    [
        [1, 2, 3, 4, 5, 6, 7, 8],
        [4, 4, 4, 4, 5, 6, 7, 8],
    ],
    dtype=torch.float,
)
labels = torch.tensor([[1], [0]], dtype=torch.float)
# 4.training cycle forward, backward, update
for epoch in range(50):
    running_loss = 0.0
    running_i = 0
    for i in range(10):
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

plt.plot(epoch_list, loss_list)
plt.ylabel("loss")
plt.xlabel("epoch")
plt.show()
