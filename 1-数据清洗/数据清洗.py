import json
import pandas as pd

# 文件路径
input_file = '/Users/jhx/Documents/Code/黑神话女性数据/0数据/preprocessed_data.jsonl'
output_jsonl = '/Users/jhx/Documents/Code/黑神话女性数据/0数据/preprocessed_data1.jsonl'
filtered_jsonl = '/Users/jhx/Documents/Code/黑神话女性数据/0数据/preprocessed_data111.jsonl'
summary_csv = '/Users/jhx/Documents/Code/黑神话女性数据/1-数据清洗/cleaning_summary3.csv'

# 定义关键词集合
A = ["黑神话", "黑猴", "游戏", "黑悟空", "吗喽", "马喽", "3a", "3A", "主创", "杨奇"]
B = ["女", "性别", "集美", "辱女"]
C = ["四妹"] 
D = ["阅文","说唱歌手","材的起点","章小蕙"] 

def contains_any(text, keyword_list):
    """检查文本中是否包含列表中的任意关键词。"""
    return any(k in text for k in keyword_list)

def contains_combination(text, list_a, list_b):
    """检查文本中是否包含list_a中的任意一个词和list_b中的任意一个词。"""
    return contains_any(text, list_a) and contains_any(text, list_b)

# 初始化统计变量
cleaned_data = []
filtered_data = []
original_count = 0

# 打开并逐行读取JSONL文件
try:
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            original_count += 1
            data = json.loads(line.strip())
            txt = data.get("text", "")

            # 如果文本中包含D中的任意一个词，则删除
            if contains_any(txt, D):
                filtered_data.append(data)
            # 否则，如果满足C中的任意关键词（直接保留），或满足A和B的组合，也保留
            elif contains_any(txt, C) or contains_combination(txt, A, B):
                cleaned_data.append(data)
            else:
                filtered_data.append(data)
except FileNotFoundError:
    print(f"输入文件 {input_file} 不存在，请检查路径！")
    exit()

# 保存清洗后的数据为JSONL文件
with open(output_jsonl, 'w', encoding='utf-8') as f:
    for entry in cleaned_data:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

# 保存被过滤的数据为JSONL文件
with open(filtered_jsonl, 'w', encoding='utf-8') as f:
    for entry in filtered_data:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

# 生成清洗结果统计
summary_data = {
    "原始数据总量": [original_count],
    "删除的数据数量": [len(filtered_data)],
    "保留的数据数量": [len(cleaned_data)]
}

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv(summary_csv, index=False, encoding='utf-8')

print(f"清洗完成！统计结果已保存：\n"
      f"保留数据 JSONL: {output_jsonl}\n"
      f"删除数据 JSONL: {filtered_jsonl}\n"
      f"清洗统计: {summary_csv}")