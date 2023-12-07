import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn.utils.rnn import pack_padded_sequence, pad_sequence

# 定义你的数据集（用你实际的数据加载代码替换这里）
# X_features 应该是形状为 (num_samples, 3) 的张量
# X_sequence 是一个包含序列的长度不固定的张量列表
# y 应该是形状为 (num_samples,) 的张量

# 示例:
# X_features = ...
# X_sequence = [...]
# y = ...

# 定义模型
class ComplexClassifier(nn.Module):
    def __init__(self, feature_dim, hidden_size, output_size):
        super(ComplexClassifier, self).__init__()

        # 用于序列的嵌入层
        self.embedding = nn.EmbeddingBag(1000, embedding_dim=embedding_dim, sparse=True)

        # 用于处理序列的 LSTM 层
        self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=hidden_size, batch_first=True)

        # 用于固定大小特征的全连接层
        self.fc_features = nn.Linear(feature_dim, hidden_size)

        # 最终的二分类全连接层
        self.fc_final = nn.Linear(hidden_size * 2, output_size)

    def forward(self, x_features, x_sequence, sequence_lengths):
        # 处理固定大小特征
        x_features = torch.relu(self.fc_features(x_features))

        # 嵌入并处理可变长度序列
        x_sequence = self.embedding(x_sequence)
        x_sequence = nn.utils.rnn.pad_packed_sequence(
            pack_padded_sequence(x_sequence, sequence_lengths, batch_first=True, enforce_sorted=False),
            batch_first=True
        )[0]
        _, (x_sequence, _) = self.lstm(x_sequence)

        # 连接特征和序列
        x_combined = torch.cat((x_features, x_sequence.squeeze(0)), dim=1)

        # 最终的分类层
        output = torch.sigmoid(self.fc_final(x_combined))
        return output

# 实例化模型、损失函数和优化器
feature_dim = 3  # 固定大小特征的数量
embedding_dim = 32  # 序列嵌入的维度
hidden_size = 64  # 隐藏层的大小
output_size = 1  # 二分类

model = ComplexClassifier(feature_dim, hidden_size, output_size)
criterion = nn.BCELoss()  # 用于二分类的二元交叉熵损失
optimizer = optim.Adam(model.parameters(), lr=0.01)  # 你可以选择不同的优化器和学习率

# 将你的数据转换为张量并处理可变长度序列

# 训练循环
num_epochs = 100  # 根据需要调整 epoch 数量
for epoch in range(num_epochs):
    # 前向传播
    outputs = model(X_features, X_sequence, sequence_lengths)

    # 计算损失
    loss = criterion(outputs.squeeze(), y.float())  # 将输出挤压为与 y 相同的形状

    # 反向传播和优化
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')


