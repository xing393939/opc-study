import pandas as pd

def process_excel(input_file, output_file):
    """
    处理Excel文件，按游戏类型分组并累加分数，保存为新的Excel文件。

    :param input_file: 输入的Excel文件路径
    :param output_file: 输出的Excel文件路径
    """
    # 读取Excel文件，跳过前两行表头，且只读取前3列
    df = pd.read_excel(input_file, skiprows=2, usecols=[0, 1, 2], header=None)

    # 设置列名（假设前三列分别为：未知列、游戏类型、分数）
    df.columns = ['未知列', '游戏类型', '分数']

    # 按游戏类型分组并累加分数
    grouped = df.groupby('游戏类型')['分数'].sum().reset_index()

    # 将结果保存为新的Excel文件
    grouped.to_excel(output_file, index=False)

    print(f"处理完成，结果已保存为 {output_file}")

# 调用函数处理Excel
input_file = 'input_file.xlsx'  # 输入的Excel文件
output_file = 'output_file.xlsx'  # 输出的Excel文件
process_excel(input_file, output_file)