import json
import csv

# 文件路径
input_file = ''
edges_file = ''
nodes_file = ''

# 使用集合存储节点，避免重复
nodes = set()
edges = []

# 解析 JSON 文件，只处理转发微博
with open(input_file, 'r', encoding='utf-8') as file:
    for line in file:
        try:
            tweet = json.loads(line.strip())
            
            # 如果不是转发微博，则跳过
            if 'retweeted_status' not in tweet:
                continue
            
            # 获取信息源（原微博作者）和转发者名称
            source_name = tweet['retweeted_status'].get('user', {}).get('name', '')
            target_name = tweet.get('user', {}).get('name', '')
            
            # 如果两个名称均存在，则记录边和节点
            if source_name and target_name:
                edges.append([source_name, target_name])
                nodes.add(source_name)
                nodes.add(target_name)
                
        except json.JSONDecodeError:
            print(f"Error decoding JSON line: {line.strip()}")

# 写入边表格（供Gephi直接导入）
with open(edges_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Source', 'Target'])
    writer.writerows(edges)

# 写入节点表格（仅包含节点名称）
with open(nodes_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Id'])
    for name in nodes:
        writer.writerow([name])

print(f"边表格已保存到 {edges_file}")
print(f"节点表格已保存到 {nodes_file}")