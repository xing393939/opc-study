### Python+AI小白教程1：excel的分组统计

#### 具体步骤
1. 点击这里下载软件包，解压后运行starter.exe，若显示success则说明环境没有问题。
2. 点击这里下载示例的excel，放到上一步解压的目录。
3. 打开kimi或者文心一言，发送如下内容给AI助手：
```
我有一个Excel，文件名是input_file.xlsx。请写一个python程序，使用pandas包生成一个新的Excel，文件名是output_file.xlsx。要求如下：

1. Excel有若干列，只保留前3列。
2. 第2列是游戏类型，第3列是分数，请以游戏类型为分组，累加同类型的分数。
3. 第1行和第二行是表头，请忽略。
```

4. AI助手会提供python代码给你，复制代码然后替换目录里面的index.py的内容，然后再次运行starter.exe，如果生成一个output_file.xlsx则说明成功了。