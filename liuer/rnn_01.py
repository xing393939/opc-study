import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from matplotlib import pyplot as plt


input_size = 1
hidden_size = 16
output_size = 1


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.rnn = nn.RNN(
            input_size=input_size,  # feature_len=1
            hidden_size=hidden_size,  # 隐藏记忆单元尺寸hidden_len
            num_layers=1,  # 层数
            batch_first=True,  # 在传入数据时,按照[batch,seq_len,feature_len]的格式
        )
        self.linear = nn.Linear(hidden_size, output_size)  # 输出层

    def forward(self, x, hidden_prev):
        out, hidden_prev = self.rnn(x, hidden_prev)
        out = self.linear(out)
        return out, hidden_prev


# 训练过程
model = Net()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)
input_sequence = torch.sin(torch.linspace(0, 4 * np.pi, 100)).view(1, -1, 1).float()
#input_sequence = torch.linspace(0, 99, 100).view(1, -1, 1).float()

for iter in range(3001):
    start = np.random.randint(4, size=1)[0]
    x = input_sequence[:, start : start + 95]
    y = input_sequence[:, start + 1 : start + 96]
    hidden_prev = torch.zeros(1, 1, hidden_size)
    output, _ = model(x, hidden_prev)  # 喂入模型得到输出

    loss = criterion(output, y)  # 计算MSE损失
    model.zero_grad()
    loss.backward()
    optimizer.step()

    if iter % 1000 == 0:
        print("Iteration: {:4d} loss {}".format(iter, loss.item()))


# 测试过程
input = input_sequence[:, [0], :]
new_sequence = []
for _ in range(100):
    pred, hidden_prev = model(input, hidden_prev)
    input = pred
    new_sequence.append(pred.detach().numpy().ravel()[0])

plt.plot(
    torch.linspace(0, 4 * np.pi, 100).detach().numpy(),
    input_sequence.reshape(-1).detach().numpy(),
)
plt.plot(torch.linspace(0, 4 * np.pi, 100).detach().numpy(), new_sequence)
plt.show()
