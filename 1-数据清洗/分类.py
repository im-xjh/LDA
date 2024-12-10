import json
import pandas as pd
from collections import Counter
import os

# 文件路径
input_file = '/Users/jhx/Documents/Code/黑神话女性数据/0数据/preprocessed_data.jsonl'
base_output_path = '/Users/jhx/Documents/Code/黑神话女性数据/1-数据清洗/'

# 生成动态文件名
def generate_filename(base_path, source_file, suffix):
    base_name = os.path.splitext(os.path.basename(source_file))[0]
    return os.path.join(base_path, f"{base_name}_{suffix}.jsonl")

retweet_file = generate_filename(base_output_path, input_file, 'repost')
non_retweet_file = generate_filename(base_output_path, input_file, 'no_repost')
output_stats_file = generate_filename(base_output_path, input_file, 'stats.xlsx')

# 数据容器
retweet_data = []
non_retweet_data = []
retweet_counter = Counter()

try:
    # 逐行读取 .jsonl 文件
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line.strip())  # 每一行是一个独立的 JSON 对象
            retweeted_status = data.get('retweeted_status')

            if retweeted_status:
                retweet_data.append(data)
                retweet_counter[retweeted_status['user']['name']] += 1
            else:
                non_retweet_data.append(data)

    # 按用户频数排序
    sorted_users = [user for user, _ in retweet_counter.most_common()]
    sorted_retweet_data = sorted(
        retweet_data,
        key=lambda x: (sorted_users.index(x['retweeted_status']['user']['name']), x['retweeted_status']['user']['name'])
    )

    # 保存转发和无转发数据
    with open(retweet_file, 'w', encoding='utf-8') as file:
        for data in sorted_retweet_data:
            file.write(json.dumps(data, ensure_ascii=False) + '\n')

    with open(non_retweet_file, 'w', encoding='utf-8') as file:
        for data in non_retweet_data:
            file.write(json.dumps(data, ensure_ascii=False) + '\n')

    # 统计频数
    stats_data = [{'Username': user, 'Count': count} for user, count in retweet_counter.most_common()]
    stats_data.append({'Username': 'Empty Retweets', 'Count': len(non_retweet_data)})

    # 输出为Excel
    stats_df = pd.DataFrame(stats_data)
    stats_df.to_excel(output_stats_file, index=False)
    print("数据处理完成，结果已保存。")

except FileNotFoundError:
    print("文件未找到，请检查文件路径是否正确。")
except Exception as e:
    print(f"发生错误：{e}")