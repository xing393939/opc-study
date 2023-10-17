import torch

# x,y是矩阵，3行1列 也就是说总共有3个数据，每个数据只有1个特征
x_data = torch.tensor([[1.0], [2.0], [3.0]])
y_data = torch.tensor([[2.0], [4.0], [6.0]])

class LinearModel(torch.nn.Module):
    def __init__(self):
        super(LinearModel, self).__init__()
        self.linear = torch.nn.Linear(1, 1) #这里数据集中的x和y的特征都是1维的

    def forward(self, x):
        y_pred = self.linear(x)
        return y_pred

model = LinearModel()
criterion = torch.nn.MSELoss(reduction='sum')
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)  # model.parameters()自动完成参数的初始化操作

# forward, backward, update
for epoch in range(100):
    y_pred = model(x_data)           # forward:predict
    loss = criterion(y_pred, y_data) # forward:loss
    print(epoch, loss.item())

    optimizer.zero_grad() # set the grad to zero
    loss.backward()       # backward: autograd，自动计算梯度
    optimizer.step()      # update 参数，即更新w和b的值

print('w = ', model.linear.weight.item())
print('b = ', model.linear.bias.item())

x_test = torch.tensor([[4.0]])
y_test = model(x_test)
print('y_pred = ', y_test.data)