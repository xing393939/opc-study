import torch

word1 = torch.LongTensor([0, 1, 88])
word2 = torch.LongTensor([88, 1, 2])
embedding = torch.nn.Embedding(89, 5)
print(embedding(word1))
print(embedding(word2))
