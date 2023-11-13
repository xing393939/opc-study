"""
input hello
output ohlol
use RNN
"""
import torch

input_size = 4
hidden_size = 4
num_layers = 1
num_class = 4
batch_size = 1
seq_len = 5
# 准备数据
idx2char = ["e", "h", "l", "o"]
x_data = [[1, 0, 2, 2, 3]]  # hello
y_data = [3, 1, 2, 3, 2]  # ohlol

# 构造输入序列和标签
inputs = torch.LongTensor(x_data)
labels = torch.LongTensor(y_data)


# design model
class Model(torch.nn.Module):
    def __init__(self, input_size, hidden_size, batch_size, num_layers=1):
        super(Model, self).__init__()
        self.num_layers = num_layers
        self.batch_size = batch_size
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.emb = torch.nn.Embedding(num_embeddings=input_size, embedding_dim=5)
        self.rnn = torch.nn.RNN(
            input_size=5,
            hidden_size=self.hidden_size,
            num_layers=self.num_layers,
            batch_first=True,
        )
        self.fc = torch.nn.Linear(hidden_size, num_class)

    def forward(self, x):
        hidden = torch.zeros(self.num_layers, self.batch_size, self.hidden_size)
        x = self.emb(x)
        x, _ = self.rnn(x, hidden)
        x = self.fc(x)
        return x.view(-1, num_class)


net = Model(input_size, hidden_size, batch_size, num_layers)

# loss and optimizer
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(net.parameters(), lr=0.05)

# train cycle
for epoch in range(20):
    optimizer.zero_grad()
    outputs = net(inputs)
    loss = criterion(outputs, labels)
    loss.backward()
    optimizer.step()

    _, idx = outputs.max(dim=1)
    idx = idx.data.numpy()
    print("Predicted: ", "".join([idx2char[x] for x in idx]), end="")
    print(",Epoch [%d/20] loss=%.3f" % (epoch + 1, loss.item()))
