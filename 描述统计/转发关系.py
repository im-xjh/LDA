import json
import csv

# 输入文件路径
input_file = '/Users/jhx/Documents/Code/黑神话女性数据/黑神话女性_情感_with_gender.jsonl'
output_file = '/Users/jhx/Documents/Code/黑神话女性数据/黑神话女性_情感_social_network.csv'

# 存储边数据
edges = []

# 读取 JSONL 文件并解析
with open(input_file, 'r', encoding='utf-8') as file:
    for line in file:
        try:
            tweet = json.loads(line.strip())
            
            # 提取转发者信息
            source_name = tweet.get('user', {}).get('name', '')
            source_gender = tweet.get('user', {}).get('gender', '')
            
            # 提取被转发者信息（如果存在转发）
            if 'retweeted_status' in tweet:
                target_name = tweet['retweeted_status'].get('user', {}).get('name', '')
                
                # 仅在 source 和 target 信息有效时添加边数据
                if source_name and target_name:
                    edges.append([source_name, source_gender, target_name])

        except json.JSONDecodeError:
            print(f"Error decoding JSON line: {line.strip()}")

# 将结果保存为 CSV
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # 写入表头
    writer.writerow(['source_name', 'source_gender', 'target_name'])
    # 写入边数据
    writer.writerows(edges)

print(f"数据已导出到 {output_file}")