import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import os

for dirname, _, filenames in os.walk("titanic"):
    for filename in filenames:
        print(os.path.join(dirname, filename))


import matplotlib.pyplot as plt  # for visualization
from tqdm import tqdm  # progress bar library
from sklearn.preprocessing import StandardScaler

# ------------- pytorch ---------------
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")  # GPU or CPU

train_data = pd.read_csv("titanic/train.csv")
test_data = pd.read_csv("titanic/test.csv")
sub = pd.read_csv("titanic/gender_submission.csv")

# Age - filling the NaN values
age_mean = train_data["Age"].dropna().mean()
train_data["Age"].fillna(age_mean, inplace=True)
test_data["Age"].fillna(age_mean, inplace=True)

# Sex - label encoding
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
le.fit(train_data["Sex"])
train_data["Sex"] = le.transform(train_data["Sex"])
test_data["Sex"] = le.transform(test_data["Sex"])

# Embarked - one hot encoding
temp = pd.concat([train_data, test_data], axis=0)
temp_em = pd.get_dummies(temp["Embarked"], dummy_na=True)
temp = pd.concat([temp, temp_em], axis=1)

# split the data
train = temp.iloc[: len(train_data), :]
test = temp.iloc[len(train_data) :, :]


# define features and target
features = ["Pclass", "Sex", "Age", "SibSp", "Parch", "C", "Q", "S", np.nan]
target = "Survived"
train_X = np.array(train[features])
train_Y = np.array(train[target])
test_X = np.array(test[features])
test_Y = np.array(test[target])

# Normalization
Scaler = StandardScaler()
train_X = Scaler.fit_transform(train_X)
test_X = Scaler.fit_transform(test_X)

# numpy to torch
train_X = torch.FloatTensor(train_X[:])
train_Y = torch.LongTensor(train_Y[:])
val_X = torch.FloatTensor(test_X[:])
val_Y = torch.LongTensor(test_Y[:])


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear1 = nn.Linear(len(features), 256)
        self.linear2 = nn.Linear(256, 8)
        self.out = nn.Linear(8, 2)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        x = self.out(x)
        return x


model = Net().to(device)
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

batch_size = 64
batch = len(train_X) // batch_size
n_epochs = 500

loop = tqdm(range(n_epochs))
for epoch in loop:
    total_loss = 0
    num_right = 0
    for i in range(batch):
        start = i * batch_size
        end = start + batch_size
        # Get data to cuda if possible
        x_t = train_X[start:end].to(device)
        y_t = train_Y[start:end].to(device)

        # forward
        output = model(x_t)
        loss = loss_fn(output, y_t)

        # backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        values, labels = torch.max(output, 1)
        num_right += np.sum(labels.cpu().numpy() == y_t.cpu().numpy())
        total_loss += loss.item() * batch_size
    loop.set_postfix(
        loss="{:6f}".format(total_loss / len(train_X)),
        acc="{:6f}".format(num_right / len(train_Y)),
    )


with torch.no_grad():
    test_result = model(val_X.to(device))
    values, labels = torch.max(test_result, 1)
    print(labels, val_Y)
    num_right = np.sum(labels.cpu().numpy() == val_Y.cpu().numpy())
    print(num_right / len(val_Y))
