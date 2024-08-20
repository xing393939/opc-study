from sklearn.metrics import classification_report
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from torchvision import datasets


def get_train_and_test():
    train_dataset = datasets.MNIST(
        root="~/data/", train=True, download=True
    )
    test_dataset = datasets.MNIST(
        root="~/data/", train=False, download=True
    )
    return train_dataset, test_dataset


if __name__ == "__main__":
    loader_tran, loader_test = get_train_and_test()
    data_train, label_train = loader_tran.data.numpy(), loader_tran.targets.numpy()
    data_train = data_train.reshape(len(data_train), -1)
    data_test, label_test = loader_test.data.numpy(), loader_test.targets.numpy()
    data_test = data_test.reshape(len(data_test), -1)

    for func in [BernoulliNB, GaussianNB]:
        classifier = func()
        classifier.fit(data_train, label_train)
        predictions = classifier.predict(data_test)  # 预测测试集
        print(classification_report(label_test, predictions))  # 输出分类报告
