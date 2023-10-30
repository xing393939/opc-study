import torch
import numpy as np
from torch.utils.data import Dataset
from torch.utils.data import DataLoader

# prepare dataset
device = torch.device("cuda:0")


class DiabetesDataset(Dataset):
    def __init__(self, filepath):
        xy = np.loadtxt(filepath, skiprows=1, delimiter=",", dtype=np.float32)
        self.len = xy.shape[0]  # shape(多少行，多少列)
        self.x_data = torch.from_numpy(xy[:, :-1]).to(device)
        self.y_data = torch.from_numpy(xy[:, [-1]]).to(device)

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.len


dataset = DiabetesDataset("diabetes.csv")
train_loader = DataLoader(dataset=dataset, batch_size=400, shuffle=True)


# design model using class
class Model(torch.nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.linear1 = torch.nn.Linear(8, 6)
        self.linear2 = torch.nn.Linear(6, 4)
        self.linear3 = torch.nn.Linear(4, 1)
        self.sigmoid = torch.nn.Sigmoid()

    def forward(self, x):
        x = self.sigmoid(self.linear1(x))
        x = self.sigmoid(self.linear2(x))
        x = self.sigmoid(self.linear3(x))
        return x


model = Model().to(device)

# construct loss and optimizer
criterion = torch.nn.BCELoss(reduction="mean")
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# training cycle forward, backward, update
if __name__ == "__main__":
    for epoch in range(100000):
        for i, data in enumerate(train_loader, 0):
            inputs, labels = data
            y_pred = model(inputs)
            loss = criterion(y_pred, labels)
            if epoch % 1000 == 0 and i == 0:
                print(
                    "epoch %9d error %.3f" % (epoch, loss.item()),
                    model.linear3.weight.data,
                    model.linear3.bias.data,
                )

            optimizer.zero_grad()
            loss.backward()

            optimizer.step()
