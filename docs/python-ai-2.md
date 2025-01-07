### Python+AI小白教程2：基于excel生成图表

#### 背景说明
本文通过一个实际示例演示如何使用Kimi或文心一言生成Python代码来操作Excel并生成图表。原Excel和图表如下图：

![](../python-ai/example01.png)

#### 具体步骤
1. 点击[这里](https://static-621585.oss-cn-beijing.aliyuncs.com/python-ai/2025-01-07-example02.rar)下载软件包，解压后里面的input_file.xlsx就是原始excel。
2. 运行starter.exe，出现success则说明环境没有问题。
3. 打开kimi或者文心一言，发送如下内容给AI助手：
 ```
我有一个Excel，文件名是input_file.xlsx。请写一个python程序，使用pyecharts包生成图表，图表文件名是output_file.html。要求如下：

1. Excel有若干列，第1列是月份，第2列是降水量，第3列是蒸发量，第4列是平均温度。
2. 第1行是表头，请忽略。
3. 生成图表，x轴是月份，请展示降水量、蒸发量、平均温度随月份的变化折线图。
 ```
4. AI助手会提供python代码给你，复制代码然后替换第1步解压的目录里面的index.py的内容。这里提供一份示例代码：
 ```
 import pandas as pd
 df = pd.read_excel('input_file.xlsx', skiprows=2, usecols=[0, 1, 2], header=None)
 df.columns = ['未知列', '游戏类型', '分数']
 grouped = df.groupby('游戏类型')['分数'].sum().reset_index()
 grouped.to_excel('output_file.xlsx', index=False)
 ```
5. 再次运行starter.exe，如果生成一个output_file.xlsx则说明成功了。打开output_file.xlsx就是最终想要的excel。