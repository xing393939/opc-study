import torch
from matplotlib import pyplot as plt
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

x_data = [1.0, 2.0, 3.0]
y_data = [2.0, 4.0, 6.0]
w = torch.tensor([1.0])  # w的初值为1.0
w.requires_grad = True   # 需要计算梯度

def forward(x):
    return x * w         # w是一个Tensor

def loss(x, y):
    y_pred = forward(x)
    return (y_pred - y) ** 2

print("predict (before training)", 4, forward(4).item())

l_lost = []
epoch_list = []
for epoch in range(100):
    for x, y in zip(x_data, y_data):
        '''
        l是一个张量，tensor主要是在建立计算图 forward, compute the loss
        反向传播主要体现在，l.backward()。调用该方法后w.grad由None更新为Tensor类型，且w.grad.data的值用于后续w.data的更新。
        l.backward()会把计算图中所有需要梯度(grad)的地方都会求出来，然后把梯度都存在对应的待求的参数中，最终计算图被释放。
        '''
        l = loss(x, y)
        l.backward()
        '''
        1)w.data 表示张量w的值，其本身也是张量，输出格式tensor[数]。
        2)w.grad 表示张量w的梯度，其本身w.grad是张量
                 标量计算时需要取w.grad.data，表示张量w.grad的值，输出格式tensor[数]
                 梯度输出时需要取w.grad.item()，表示返回的是一个具体的数值，输出格式[数]
        对于元素不止一个的tensor列表，使用item()会报错，向量不行二维更不行，只有标量行。
        item只能对标量做操作，而data返回的其实也是一个Tensor，不过这个Tensor是不计算梯度的
        '''
        print('\tgrad:', x, y, w.grad.item())
        w.data = w.data - 0.01 * w.grad.data  # 权重更新时，注意grad也是一个tensor
        w.grad.data.zero_()                   # set the grad to zero
    epoch_list.append(epoch)
    l_lost.append(l.item())
    print('progress:', epoch, l.item())       # 取出loss使用l.item，不要直接使用l（l是tensor会构建计算图）

print("predict (after training)", 4, forward(4).item())
plt.plot(epoch_list, l_lost)
plt.xlabel('Epoch')
plt.ylabel('lost')
plt.show()