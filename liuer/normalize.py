from sklearn.preprocessing import StandardScaler
import torchvision.transforms as transforms
import numpy as np
import torch

x_np = np.array([[1.5, -1.0, 2.0], [2.0, 0.0, 0.0]])
scaler = StandardScaler()
x_train = scaler.fit_transform(x_np)
print(x_train, scaler.mean_, scaler.var_)

trans_func = transforms.Normalize((0.1307,), (0.3081,))
x_train = trans_func(torch.from_numpy(x_np))
print(x_train)
