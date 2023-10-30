import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset
from torch.utils.data import DataLoader


# 数据集加载
class DiabetesDataset(Dataset):
    def __init__(self, filepath):
        xy = np.loadtxt(filepath, skiprows=1, delimiter=",", dtype=np.float32)
        self.len = xy.shape[0]
        self.x_data = np.insert(xy[:, :-1], 0, 1, axis=1)
        self.y_data = xy[:, [-1]]

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.len


dataset = DiabetesDataset("redPacket_2.csv")
train_loader = DataLoader(dataset=dataset, batch_size=1024, shuffle=True)


# sigmod函数，得到y大于等于0.5是1，y小于等于0.5为0。
def sigmoid2(z):
    return 1.0 / (1 + np.exp(-z))


def sigmoid(x):
    return 0.5 * (1 + np.tanh(0.5 * x))


# datas NxD
# labs Nx1
# w    Dx1
def weight_update(datas, labs, w, alpha=0.01):
    z = np.dot(datas, w)  # Nx1
    h = sigmoid(z)  # Nx1
    Error = labs - h  # Nx1
    w = w + alpha * np.dot(datas.T, Error)
    return w


def test_accuracy(datas, labs, w):
    N, D = np.shape(datas)
    z = np.dot(datas, w)  # Nx1
    h = sigmoid(z)  # Nx1
    lab_det = (h > 0.5).astype(np.float32)
    error_rate = np.sum(np.abs(labs - lab_det)) / N
    return error_rate


def train_LR(n_epoch=2, alpha=0.005):
    w = np.ones([5, 1])
    # 进行n_epoch轮迭代
    for epoch in range(n_epoch):
        for i, data in enumerate(train_loader, 0):
            datas, labs = data
            w = weight_update(datas, labs, w, alpha)
            if epoch % 1000 == 0 and i == 0:
                error_rate = test_accuracy(datas.numpy(), labs.numpy(), w)
                print("epoch %9d error %.3f%%" % (epoch, error_rate * 100), w.T[0][:-1])
    return w


if __name__ == "__main__":
    weights = train_LR(n_epoch=100000, alpha=0.01)
    print(weights)
