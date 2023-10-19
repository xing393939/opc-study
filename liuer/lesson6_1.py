import numpy as np
import matplotlib.pyplot as plt


def load_dataset(file):
    with open(file, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    # 取 lab 维度为 N x 1
    labs = [line.split("\t")[-1] for line in lines]
    labs = np.array(labs).astype(np.float32)
    labs = np.expand_dims(labs, axis=-1)  # Nx1

    # 取数据 增加 一维全是1的特征
    datas = [line.split("\t")[:-1] for line in lines]
    datas = np.array(datas).astype(np.float32)
    N, D = np.shape(datas)
    # 增加一个维度
    datas = np.c_[np.ones([N, 1]), datas]
    return datas, labs


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
    lab_det = (h > 0.5).astype(float)
    error_rate = np.sum(np.abs(labs - lab_det)) / N
    return error_rate


def train_LR(datas, labs, n_epoch=2, alpha=0.005):
    N, D = np.shape(datas)
    w = np.ones([D, 1])  # Dx1
    # 进行n_epoch轮迭代
    for i in range(n_epoch):
        w = weight_update(datas, labs, w, alpha)
        error_rate = test_accuracy(datas, labs, w)
        print("epoch %d error %.3f%%" % (i, error_rate * 100))
    return w


def draw_desion_line(datas, labs, w):
    dic_colors = {0: (0.8, 0, 0), 1: (0, 0.8, 0)}

    # 画数据点
    for i in range(2):
        index = np.where(labs == i)[0]
        sub_datas = datas[index]
        plt.scatter(sub_datas[:, 1], sub_datas[:, 2], s=16.0, color=dic_colors[i])

    # 画判决线
    min_x = np.min(datas[:, 1])
    max_x = np.max(datas[:, 1])
    w = w[:, 0]
    x = np.arange(min_x, max_x, 0.01)
    y = -(x * w[1] + w[0]) / w[2]
    plt.plot(x, y)
    plt.show()


if __name__ == "__main__":
    file = "testset.txt"
    datas, labs = load_dataset(file)

    weights = train_LR(datas, labs, alpha=0.001, n_epoch=100)
    print(weights)
    draw_desion_line(datas, labs, weights)
