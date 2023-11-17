from matplotlib import pyplot as plt  # 调用matplotlib库的pyplot
import torch

a = torch.tensor(
    [
        [
            [1, 0],
            [2, 0],
        ],
        [
            [3, 0],
            [4, 0],
        ],
        [
            [5, 0],
            [6, 0],
        ],
    ]
)

print(a[:,:,0])
