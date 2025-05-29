import csv
import json

# 文件路径设置
csv_file = '/Users/jhx/Desktop/黑神话kmeans=2.csv'
input_jsonl = '/Users/jhx/Documents/Code/黑神话女性数据/0数据/cleaned_cleaned.jsonl'
output_jsonl_0 = '/Users/jhx/Documents/Code/黑神话女性数据/0数据/KOL文本提取/antifeminism.jsonl'
output_jsonl_1 = '/Users/jhx/Documents/Code/黑神话女性数据/0数据/KOL文本提取/feminism.jsonl'

# 1. 读取 CSV 文件，构建 name 到 modularity_class 的映射字典
csv_mapping = {}
with open(csv_file, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row.get('name')
        modularity_class = row.get('modularity_class')
        if name and modularity_class != '':
            csv_mapping[name] = modularity_class

# 2. 读取 JSONL 文件，匹配并根据 modularity_class 值分别输出到两个文件中
with open(input_jsonl, mode='r', encoding='utf-8') as fin, \
     open(output_jsonl_0, mode='w', encoding='utf-8') as fout0, \
     open(output_jsonl_1, mode='w', encoding='utf-8') as fout1:
    
    for line in fin:
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue  # 跳过无法解析的行

        # 判断 type 字段（先从顶层获取，如果没有则尝试从 retweeted_status 中获取）
        type_field = data.get("type", data.get("retweeted_status", {}).get("type"))
        if type_field == "转发":
            continue  # 删除 type 为转发的数据

        # 提取 retweeted_status → user → name
        retweeted = data.get('retweeted_status', {})
        retweeted_user = retweeted.get('user', {})
        retweeted_name = retweeted_user.get('name')
        
        # 若 retweeted_name 在 CSV 中有对应映射，则新增 modularity_class 字段
        if retweeted_name and retweeted_name in csv_mapping:
            data['modularity_class'] = csv_mapping[retweeted_name]
            # 根据 modularity_class 的值分别输出到不同文件
            if data['modularity_class'] == '0':
                fout0.write(json.dumps(data, ensure_ascii=False) + '\n')
            elif data['modularity_class'] == '1':
                fout1.write(json.dumps(data, ensure_ascii=False) + '\n')
