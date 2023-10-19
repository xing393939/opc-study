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
            line_np = np.array([1.0, line_array[0], line_array[1]]).astype(np.float32)
            dataMat = np.append(dataMat, [line_np], axis=0)
            labelMat = np.append(labelMat, [[int(line_array[2])]], axis=0)
    return dataMat, labelMat


# sigmod函数，即得分函数,计算数据的概率是0还是1；得到y大于等于0.5是1，y小于等于0.5为0。
def sigmod(x):
    return 1 / (1 + np.exp(-x))


# 损失函数
# hx是概率估计值，是sigmod(x)得来的值，y是样本真值
def cost(hx, y):
    return -y * np.log(hx) - (1 - y) * np.log(1 - hx)


# 梯度下降
def gradient(current_para, x, y):
    m = len(y)
    matrix_gradient = np.zeros(len(x[0]))
    for i in range(m):
        current_x = x[i]
        current_y = y[i]
        current_x = np.asarray(current_x)
        matrix_gradient += (
            sigmod(np.dot(current_para, current_x)) - current_y
        ) * current_x
    new_para = current_para - 0.001 * matrix_gradient
    return new_para


# 误差计算
def error(para, x, y):
    total = len(y)
    error_num = 0
    for i in range(total):
        current_x = x[i]
        current_y = y[i]
        hx = sigmod(np.dot(para, current_x))  # LR算法
        if cost(hx, current_y) > 0.5:  # 进一步计算损失
            error_num += 1
    return error_num / total


# 绘制图形
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
    x = np.arange(min_x, max_x, 0.01)
    y = -(x * w[1] + w[0]) / w[2]
    plt.plot(x, y)
    plt.show()


dataMat, labelMat = load_dataset()
para = np.ones(3)
print("初始参数：", para)
for i in range(1000):
    para = gradient(para, dataMat, labelMat)  # 梯度下降法
    if i % 100 == 0:
        err = error(para, dataMat, labelMat)
        print("iter:" + str(i) + " ; error:" + str(err))

print("训练所得参数：", para)
draw_decision_line(dataMat, labelMat, para)
