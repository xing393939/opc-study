import torchvision.transforms as transforms
import cv2 as cv

img = cv.imread('test.png')
img = cv.cvtColor(img, cv.COLOR_BGR2RGB) # 通道默认BGR，改成RGB
print(img.shape) # 格式是(H,W,C)，高和宽都是2像素，通道是3通道
print(img[0]) # 第一行有两个像素：[0 0 255]、[255 255 255]
print(img[1]) # 第二行有两个像素：[0 0 0]、[0 255 0]

trans_func = transforms.ToTensor()
img_tensor = trans_func(img)
print(img_tensor.size()) # 格式是(C,H,W)
print(img_tensor[0]) # R层，R数值 / 255
print(img_tensor[1]) # G层，G数值 / 255
print(img_tensor[2]) # B层，B数值 / 255

trans_func = transforms.Normalize((0.1307,), (0.3081,)) # C = (C - mean) / std
img_tensor = trans_func(img_tensor)
print(img_tensor)

img_tensor = img_tensor.view(-1, 12)
print(img_tensor)