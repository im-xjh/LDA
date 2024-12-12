import pandas as pd

# 定义文件路径
csv_file_path = '/Users/jhx/Desktop/gephi数据更新模块化.csv'
excel_file_path = '/Users/jhx/Desktop/gephi数据更新模块化.xlsx'

# 读取CSV文件（确保使用UTF-8编码）
try:
    data = pd.read_csv(csv_file_path, encoding='utf-8')
except UnicodeDecodeError:
    print("文件编码不是UTF-8，请确认编码格式或尝试转换文件编码。")
    exit()

# 保存为Excel文件
try:
    data.to_excel(excel_file_path, index=False, engine='openpyxl')
    print(f"成功将文件转换为Excel格式：{excel_file_path}")
except Exception as e:
    print(f"保存Excel文件时发生错误：{e}")