import numpy as np
import matplotlib.pyplot as plt


# 数据集加载
def load_dataset():
    xy = np.loadtxt("redPacket.csv", skiprows=1, delimiter=",", dtype=np.float32)
    x_data = np.insert(xy[:, :-1], 0, 1, axis=1)
    y_data = xy[:, [-1]]
    return x_data, y_data


# sigmod函数，即得分函数,计算数据的概率是0还是1；得到y大于等于0.5是1，y小于等于0.5为0。
def sigmoid(z):
    return 1.0 / (1 + np.exp(-z))


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


def train_LR(datas, labs, n_epoch=2, alpha=0.005):
    N, D = np.shape(datas)
    w = np.ones([D, 1])  # Dx1
    # 进行n_epoch轮迭代
    for i in range(n_epoch):
        w = weight_update(datas, labs, w, alpha)
        error_rate = test_accuracy(datas, labs, w)
        if i % 10000 == 0:
            print("epoch %d error %.3f%%" % (i, error_rate * 100))
    return w


if __name__ == "__main__":
    datas, labs = load_dataset()
    print(datas)
    print(labs)
    weights = train_LR(datas, labs, alpha=0.001, n_epoch=1000000)
    print(weights)
