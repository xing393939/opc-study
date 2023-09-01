import numpy as np

A = np.array([[0, 1, 2, 3], [4, 5, 6, 7], [8, 8, 8, 8], [9, 9, 9, 9]])
print ('原矩阵A：\n', A, '\n')
print ('原矩阵A的倒置：\n', A.T, '\n')

x = np.array([1, 1, 1, 1])
print ('矩阵x向量：\n', np.dot(A, x), '\n')

j = complex(1,1)
print ('复数：\n', j, '\n')

B = np.array([x, x])
print ('矩阵x矩阵：\n', np.dot(B, A), '\n')

C= np.fft.fft(A)
print ('一维离散傅里叶变换：\n', C, '\n')

C= np.fft.fft2(A)
print ('二维离散傅里叶变换：\n', C, '\n')

A = np.abs(np.fft.ifft2(C))
print ('还原矩阵A：\n', A, '\n')