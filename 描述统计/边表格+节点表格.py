import json
import csv

# 文件路径
input_file = '/Users/jhx/Documents/Code/黑神话女性数据/黑神话女性_情感_with_gender.jsonl'
edges_file = '/Users/jhx/Documents/Code/黑神话女性数据/黑神话_edges.csv'
nodes_file = '/Users/jhx/Documents/Code/黑神话女性数据/黑神话_nodes.csv'

# 存储节点信息和边信息
nodes = {}
edges = []

# 解析 JSON 文件
with open(input_file, 'r', encoding='utf-8') as file:
    for line in file:
        try:
            tweet = json.loads(line.strip())

            # 提取转发者信息
            target_name = tweet.get('user', {}).get('name', '')
            target_gender = tweet.get('user', {}).get('gender', '')

            # 如果存在转发内容，提取被转发者信息
            if 'retweeted_status' in tweet:
                source_name = tweet['retweeted_status'].get('user', {}).get('name', '')

                # 添加边信息
                if source_name and target_name:
                    edges.append([source_name, target_name])

                # 更新节点信息
                if source_name not in nodes:
                    nodes[source_name] = {'gender': ''}  # 默认性别为空

            # 更新转发者节点信息
            if target_name not in nodes:
                nodes[target_name] = {'gender': target_gender}

            # 如果被转发者也存在性别信息，则补充性别
            if source_name in nodes and not nodes[source_name]['gender'] and target_gender:
                nodes[source_name]['gender'] = target_gender

        except json.JSONDecodeError:
            print(f"Error decoding JSON line: {line.strip()}")

# 写入边表格
with open(edges_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Source', 'Target'])  # 表头
    writer.writerows(edges)

# 写入节点表格
with open(nodes_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', 'Gender'])  # 表头
    for name, info in nodes.items():
        writer.writerow([name, info['gender']])

print(f"边表格已保存到 {edges_file}")
print(f"节点表格已保存到 {nodes_file}")