import json
import networkx as nx
import pandas as pd
from tqdm import tqdm  # 导入进度条库

# 读取JSONL文件
file_path = '/Users/jhx/Documents/Code/weibospider/output/comment_分词.jsonl'

def read_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return [json.loads(line) for line in lines]

# 构建共现网络
def build_co_occurrence_network(text, window_size=2):
    words = text.split()  # 分词结果是空格分隔的词
    G = nx.Graph()

    # 遍历分词，构建词与词之间的边
    for i in range(len(words) - window_size + 1):
        for j in range(i + 1, i + window_size):
            word1, word2 = words[i], words[j]
            if G.has_edge(word1, word2):
                G[word1][word2]['weight'] += 1  # 增加权重
            else:
                G.add_edge(word1, word2, weight=1)

    return G

# 处理整个数据集，提取并构建网络
def process_data(data):
    G = nx.Graph()

    # 使用 tqdm 显示处理进度
    for entry in tqdm(data, desc="处理数据", unit="条"):
        text_processed = entry.get('tokens', '')
        if text_processed:
            co_occurrence_network = build_co_occurrence_network(text_processed)
            G = nx.compose(G, co_occurrence_network)  # 合并网络

    return G

# 生成边表格和节点表格
def generate_tables(G):
    # 节点表格
    nodes = pd.DataFrame(list(G.nodes), columns=['Id'])
    nodes['Label'] = nodes['Id']  # 节点的标签就是词语本身

    # 边表格
    edges = pd.DataFrame(list(G.edges(data=True)), columns=['Source', 'Target', 'Weight'])
    edges['Weight'] = edges['Weight'].apply(lambda x: x['weight'])  # 提取权重

    return nodes, edges

# 主程序
def main():
    # 读取数据
    data = read_jsonl(file_path)

    # 处理数据并构建网络
    G = process_data(data)

    # 生成节点和边的表格
    nodes, edges = generate_tables(G)

    # 保存表格为CSV文件
    nodes.to_csv('network_nodes3.9.csv', index=False, encoding='utf-8')
    edges.to_csv('network_edges3.9.csv', index=False, encoding='utf-8')

    print("节点表格和边表格已生成并保存为CSV文件。")

# 运行主程序
if __name__ == '__main__':
    main()
