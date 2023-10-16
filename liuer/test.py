from matplotlib import pyplot as plt #调用matplotlib库的pyplot
import numpy as np
def get_beans(counts):  #构造吃豆豆的函数
	xs = np.random.rand(counts)
	xs = np.sort(xs)    #进行行排序
	ys = np.array([(0.7*x+(0.5-np.random.rand())/5+0.5) for x in xs])
	return xs,ys

m=100
xs,ys=get_beans(m)  #获取100个豆子数据

print(xs)

#配置图像，坐标信息
plt.title("Size-Toxicity Function", fontsize=12) #设置图像名称
plt.xlabel("Bean Size")                          #设置横坐标的名字
plt.ylabel("Toxicity")                           #设置纵坐标的名字
plt.scatter(xs,ys)                               #画散点图
plt.show()

