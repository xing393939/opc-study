# https://blog.csdn.net/m0_58058919/article/details/126919767
import numpy as np
from torchvision import datasets, transforms
from tqdm import tqdm


def get_train_and_test():
    transform = transforms.Compose([transforms.PILToTensor()])
    train_dataset = datasets.MNIST(
        root="C:/Users/bookan/data/", train=True, download=True, transform=transform
    )
    test_dataset = datasets.MNIST(
        root="C:/Users/bookan/data/", train=False, download=True, transform=transform
    )
    return train_dataset, test_dataset


def binary(img):
    img_data = img.flatten()
    img_data = np.where(img_data != 0, 1, 0)
    """
    for i, w in enumerate(img_data):
        if i % 28 == 0:
            print()
        print("{} ".format(w), end='')
    print()
    """
    return img_data


def train(train_loader):
    # prior_pro(先验概率）
    prior_pro = np.zeros(10)
    # conditional_pro(条件概率)
    conditional_pro = np.zeros((10, 784))

    for data in tqdm(train_loader):
        img, label = data
        img = binary(img)
        prior_pro[label] += 1
        for j in range(784):
            conditional_pro[label, j] += img[j]

    # 转化为概率
    for w in range(10):
        for n in range(784):
            # 避免分母为0，通常要进行平滑处理，常用拉普拉斯修正的方法
            conditional_pro[w, n] = (conditional_pro[w, n] + 1) / (prior_pro[w] + 10)

    prior_pro = prior_pro / len(train_loader)
    return prior_pro, conditional_pro


def predict(test_loader, prior_pro, conditional_pro):
    acc = 0

    for data in tqdm(test_loader):
        img, label = data
        img = binary(img)

        result = np.zeros(10)
        for j in range(10):
            pro_y = 1
            for m in range(784):
                if img[m] == 1:
                    pro_y *= conditional_pro[j][m]
                else:
                    pro_y *= (1 - conditional_pro[j][m])
            # 为什么没有除P(X)，因为当向量X已知，P(X)相当于常量
            result[j] = prior_pro[j] * pro_y
        if label == np.argmax(result):
            acc += 1
    return acc / len(test_loader)


if __name__ == "__main__":
    loader_tran, loader_test = get_train_and_test()
    pro_prior, pro_cond = train(loader_tran)
    test_out = predict(loader_test, pro_prior, pro_cond)
    print("测试集的准确率为：{}".format(test_out))
