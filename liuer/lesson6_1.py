import numpy as np
import matplotlib.pyplot as plt


# 数据集加载
def load_dataset():
    dataMat = np.empty(shape=(0, 3))
    labelMat = np.empty(shape=(0, 1))
    with open("testset.txt", "r+") as file_object:
        lines = file_object.readlines()
        for line in lines:
            line_array = line.strip().split()
            dataMat = np.append(
                dataMat, [[1.0, float(line_array[0]), float(line_array[1])]], axis=0
            )
            labelMat = np.append(labelMat, [[int(line_array[2])]], axis=0)
    return dataMat, labelMat


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
        print("epoch %d error %.3f%%" % (i, error_rate * 100))
    return w


def draw_decision_line(datas, labs, w):
    dic_colors = ["g", "r"]

    # 画数据点
    for i in range(2):
        index = np.where(labs == i)[0]
        sub_datas = datas[index]
        plt.scatter(sub_datas[:, 1], sub_datas[:, 2], s=16.0, c=dic_colors[i])

    # 画判决线
    min_x = np.min(datas[:, 1])
    max_x = np.max(datas[:, 1])
    w = w[:, 0]
    x = np.arange(min_x, max_x, 0.01)
    y = -(x * w[1] + w[0]) / w[2]
    plt.plot(x, y)
    plt.show()


if __name__ == "__main__":
    datas, labs = load_dataset()
    weights = train_LR(datas, labs, alpha=0.001, n_epoch=100)
    print(weights)
    draw_decision_line(datas, labs, weights)
