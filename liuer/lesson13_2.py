# https://www.cnblogs.com/wwj99/p/12231080.html
import torch
import torch.nn as nn
import torch.optim
from torch.autograd import Variable
from collections import Counter
import numpy as np

# 生成的样本数量
samples = 2000
# 训练样本中n的最大值
sz = 10
# 定义不同n的权重，我们按照10:6:4:3:1:1...来配置字符串生成中的n=1,2,3,4,5,...
probability = 1.0 * np.array([10, 6, 4, 3, 1, 1, 1, 1, 1, 1])
# 保证n的最大值为sz
probability = probability[:sz]
# 归一化，将权重变成概率
probability = probability / sum(probability)


# 开始生成samples这么多个样本
train_set = []
for m in range(samples):
    # 对于每一个生成的字符串，随机选择一个n，n被选择的权重被记录在probability中
    n = np.random.choice(range(1, sz + 1), p=probability)
    # 生成这个字符串，用list的形式完成记录
    inputs = [0] * n + [1] * n
    # 在最前面插入3表示起始字符，2插入尾端表示终止字符
    inputs.insert(0, 3)
    inputs.append(2)
    train_set.append(inputs)


# 再生成samples/10的校验样本
valid_set = []
for m in range(samples // 10):
    n = np.random.choice(range(1, sz + 1), p=probability)
    inputs = [0] * n + [1] * n
    inputs.insert(0, 3)
    inputs.append(2)
    valid_set.append(inputs)

# 再生成大一点的校验样本
for m in range(2):
    n = sz + m
    inputs = [0] * n + [1] * n
    inputs.insert(0, 3)
    inputs.append(2)
    valid_set.append(inputs)
np.random.shuffle(valid_set)


# 实现一个简单的RNN模型
class SimpleRNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers=1):
        # 定义
        super(SimpleRNN, self).__init__()

        self.hidden_size = hidden_size
        self.num_layers = num_layers
        # 一个embedding层
        self.embedding = nn.Embedding(input_size, hidden_size)
        # PyTorch的RNN层，batch_first标志可以让输入的张量的第一个维度表示batch指标
        self.rnn = nn.RNN(hidden_size, hidden_size, num_layers, batch_first=True)
        # 输出的全链接层
        self.fc = nn.Linear(hidden_size, output_size)
        # 最后的logsoftmax层
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input, hidden):
        # 先进行embedding层的计算，它可以把一个数值先转化为one-hot向量，再把这个向量转化为一个hidden_size维的向量
        # input的尺寸为：batch_size, num_step, data_dim
        x = self.embedding(input)
        # x的尺寸为：batch_size, num_step, hidden_size
        output, hidden = self.rnn(x, hidden)
        # 从输出output中取出最后一个时间步的数值，注意output输出包含了所有时间步的结果,
        # output输出尺寸为：batch_size, num_step, hidden_size
        output = output[:, -1, :]
        # output尺寸为：batch_size, hidden_size
        output = self.fc(output)
        # output尺寸为：batch_size, output_size
        output = self.softmax(output)
        return output, hidden

    def initHidden(self):
        # 对隐含单元的初始化
        # 注意尺寸是： layer_size, batch_size, hidden_size
        return Variable(torch.zeros(self.num_layers, 1, self.hidden_size))


# 生成一个最简化的RNN，输入size为4，可能值为0,1,2,3，输出size为3，可能值为0,1,2
rnn = SimpleRNN(input_size=4, hidden_size=2, output_size=3)
criterion = torch.nn.NLLLoss()  # 交叉熵损失函数
optimizer = torch.optim.Adam(rnn.parameters(), lr=0.001)  # Adam优化算法
train_loss = 0


def trainRNN(epoch):
    global train_loss
    train_loss = 0
    # 对train_set中的数据进行随机洗牌，以保证每个epoch得到的训练顺序都不一样。
    np.random.shuffle(train_set)
    # 对train_set中的数据进行循环
    for i, seq in enumerate(train_set):
        loss = 0
        hidden = rnn.initHidden()  # 初始化隐含层神经元
        # 对每一个序列的所有字符进行循环
        for t in range(len(seq) - 1):
            # 当前字符作为输入，下一个字符作为标签
            x = Variable(torch.LongTensor([seq[t]]).unsqueeze(0))
            # x尺寸：batch_size = 1, time_steps = 1, data_dimension = 1
            y = Variable(torch.LongTensor([seq[t + 1]]))
            # y尺寸：batch_size = 1, data_dimension = 1
            output, hidden = rnn(x, hidden)  # RNN输出
            # output尺寸：batch_size, output_size = 3
            # hidden尺寸：layer_size =1, batch_size=1, hidden_size
            loss += criterion(output, y)  # 计算损失函数
        loss = 1.0 * loss / len(seq)  # 计算每字符的损失数值
        optimizer.zero_grad()  # 梯度清空
        loss.backward()  # 反向传播，设置retain_variables
        optimizer.step()  # 一步梯度下降
        train_loss += loss  # 累积损失函数值
        # 把结果打印出来
        if i % 500 == 499:
            print(
                "第{}轮, 第{}个，训练Loss:{:.2f}".format(
                    epoch, i + 1, train_loss.data.numpy() / i
                )
            )


valid_loss = 0
errors = 0


def evaluateRNN():
    global valid_loss
    global errors
    global show_out
    valid_loss = 0
    errors = 0
    show_out = ""
    for i, seq in enumerate(valid_set):
        loss = 0
        out_string = ""
        targets = ""
        hidden = rnn.initHidden()  # 初始化隐含层神经元
        for t in range(len(seq) - 1):
            # 对每一个字符做循环
            x = Variable(torch.LongTensor([seq[t]]).unsqueeze(0))
            # x尺寸：batch_size = 1, time_steps = 1, data_dimension = 1
            y = Variable(torch.LongTensor([seq[t + 1]]))
            # y尺寸：batch_size = 1, data_dimension = 1
            output, hidden = rnn(x, hidden)
            # output尺寸：batch_size, output_size = 3
            # hidden尺寸：layer_size =1, batch_size=1, hidden_size
            mm = torch.max(output, 1)[1][0]  # 以概率最大的元素作为输出
            out_string += str(mm.data.numpy())  # 合成预测的字符串
            targets += str(y.data.numpy()[0])  # 合成目标字符串
            loss += criterion(output, y)  # 计算损失函数
        loss = 1.0 * loss / len(seq)
        valid_loss += loss  # 累积损失函数值
        errors += int(out_string[-2:] != targets[-2:])
        show_out = out_string + " " + targets
    return show_out


# 重复进行20次试验
num_epoch = 20
for epoch in range(num_epoch):
    # 调用训练函数
    trainRNN(epoch)
    # 在校验集上测试
    show_out = evaluateRNN()
    # 打印结果
    print(
        "第{}轮, 训练Loss:{:.2f}, 校验Loss:{:.2f}, 错误率:{:.2f}, 预测&标签:{}".format(
            epoch,
            train_loss.data.numpy() / len(train_set),
            valid_loss.data.numpy() / len(valid_set),
            1.0 * errors / len(valid_set),
            show_out,
        )
    )
