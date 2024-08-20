# https://www.cnblogs.com/ISGuXing/p/13777895.html
import collections

import numpy as np
from sklearn.metrics import classification_report
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


class BernoulliV2(object):
    def __init__(self):
        self.class_prior = None  # 先验概率(10)
        self.condition_prior = None  # 特征条件概率(10,784)

    def _get_class_prior(self, y):
        cnt = collections.Counter(y)
        self.class_prior = np.array([v / len(y) for k, v in cnt.items()])

    def _get_condition_prior(self, xx, y):
        self.condition_prior = np.array([np.mean(xx[y == i] > 0, axis=0) for i, _ in enumerate(self.class_prior)])

    def fit(self, xx, y):
        self._get_class_prior(y)
        self._get_condition_prior(xx, y)

    def predict(self, x):
        dims = len(x)
        likelihoods = []
        for i, _ in enumerate(self.class_prior):
            likelihoods.append(np.prod([
                self.condition_prior[i][j] if x[j] > 0 else 1 - self.condition_prior[i][j] for j in range(dims)
            ]))
        all_pros = self.class_prior * likelihoods
        return all_pros.argmax()


if __name__ == "__main__":
    loader_tran, loader_test = get_train_and_test()
    data_train, label_train = loader_tran.data.numpy(), loader_tran.targets.numpy()
    data_train = data_train.reshape(len(data_train), -1)
    data_test, label_test = loader_test.data.numpy(), loader_test.targets.numpy()
    data_test = data_test.reshape(len(data_test), -1)

    clf = BernoulliV2()
    clf.fit(data_train, label_train)
    predictions = np.array([])
    for x in tqdm(data_test):
        predictions = np.append(predictions, clf.predict(x))
    print(classification_report(label_test, predictions))
