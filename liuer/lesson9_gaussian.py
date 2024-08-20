# https://www.cnblogs.com/ISGuXing/p/13777895.html
import collections
import math

import numpy as np
from torchvision import datasets
from tqdm import tqdm


def get_train_and_test():
    train_dataset = datasets.MNIST(
        root="~/data/", train=True, download=True
    )
    test_dataset = datasets.MNIST(
        root="~/data/", train=False, download=True
    )
    return train_dataset, test_dataset


class GaussianNBV2(object):
    def __init__(self):
        self.class_prior = None  # 先验概率(10)
        self.means = None  # 均值(10,784)
        self.vars = None  # 方差(10,784)

    def _get_class_prior(self, y):
        cnt = collections.Counter(y)
        self.class_prior = np.log(np.array([v / len(y) for k, v in cnt.items()]))

    def _get_means(self, xx, y):
        self.means = np.array([xx[y == i].mean(axis=0) for i, _ in enumerate(self.class_prior)])

    def _get_vars(self, xx, y):
        self.vars = np.array([xx[y == i].var(axis=0) for i, _ in enumerate(self.class_prior)])
        # 给所有方差加上平滑的值
        self.vars = self.vars + 1e-9 * self.vars.max(initial=0)

    def fit(self, xx, y):
        self._get_class_prior(y)
        self._get_means(xx, y)
        self._get_vars(xx, y)

    @staticmethod
    def _get_gaussian(x, u, var):
        return -(x - u) ** 2 / (2 * var) - math.log(math.sqrt(2 * math.pi * var))

    def predict(self, x):
        dims = len(x)
        likelihoods = []
        for i, _ in enumerate(self.class_prior):
            likelihoods.append(np.sum([
                self._get_gaussian(x[j], self.means[i][j], self.vars[i][j]) for j in range(dims)
            ]))
        all_pros = self.class_prior + likelihoods
        return all_pros.argmax()


if __name__ == "__main__":
    loader_tran, loader_test = get_train_and_test()
    # Train model
    clf = GaussianNBV2()
    data_train, label_train = loader_tran.data.numpy(), loader_tran.targets.numpy()
    data_train = data_train.reshape(len(data_train), -1)
    clf.fit(data_train, label_train)
    # Model evaluation
    data_test, label_test = loader_test.data.numpy(), loader_test.targets.numpy()
    data_test = data_test.reshape(len(data_test), -1)

    y_hat = []
    for a in tqdm(data_test):
        b = clf.predict(a)
        y_hat.append(b)
    y_hat = np.array(y_hat)
    acc = (label_test == y_hat).sum() / len(label_test)
    print("测试集的准确率为：{}".format(acc))
