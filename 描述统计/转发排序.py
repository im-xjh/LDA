import json
import csv
from collections import Counter

# 输入文件路径
zhuanping_file = '/Users/jhx/Documents/Code/黑神话女性数据/cleaned_转评.jsonl'
zhuanfa_file = '/Users/jhx/Documents/Code/黑神话女性数据/cleaned_转发.jsonl'

# 输出文件路径
output_csv = 'retweeted_users_count_sorted.csv'
output_jsonl = 'combined_sorted_by_retweet_count.jsonl'

# 用于统计被转发者的转发次数
user_counter = Counter()

# 定义一个函数来处理文件并统计
def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line.strip())
            if 'retweeted_status' in data and data['retweeted_status']:
                retweeted_status = data['retweeted_status']
                if 'user' in retweeted_status and 'name' in retweeted_status['user']:
                    user_name = retweeted_status['user']['name']
                    user_counter[user_name] += 1

            # 处理转评的数据（转评不包含retweeted_status，但仍需按原帖发布者统计）
            if 'user' in data and 'name' in data['user']:
                user_name = data['user']['name']
                user_counter[user_name] += 0  # 保证也能处理转评（以0次计）

# 处理 zhuanping.jsonl 和 zhuanfa.jsonl 文件
process_file(zhuanping_file)
process_file(zhuanfa_file)

# 将统计结果按转发次数从高到低排序
sorted_users = [user for user, _ in user_counter.most_common()]

# 将结果写入CSV文件
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['name', 'count'])
    for user_name, count in user_counter.most_common():
        csv_writer.writerow([user_name, count])

print(f"统计完成，结果已保存到 {output_csv}")
def filter_and_sort_file(input_file, sorted_users):
    sorted_data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line.strip())
            original_user_name = ''
            if 'retweeted_status' in data and data['retweeted_status']:
                retweeted_status = data['retweeted_status']
                if 'user' in retweeted_status and 'name' in retweeted_status['user']:
                    original_user_name = retweeted_status['user']['name']
                    if original_user_name in sorted_users:
                        sorted_data.append({'type': '转发', **data})
            else:
                if 'user' in data and 'name' in data['user']:
                    original_user_name = data['user']['name']
                    if original_user_name in sorted_users:
                        sorted_data.append({'type': '转评', **data})

    # 按照被转发者的转发次数对数据进行排序
    def get_original_user_name(x):
        if 'retweeted_status' in x and x['retweeted_status']:
            retweeted_status = x['retweeted_status']
            if 'user' in retweeted_status and 'name' in retweeted_status['user']:
                return retweeted_status['user']['name']
        return x['user']['name']

    sorted_data = sorted(sorted_data, key=lambda x: sorted_users.index(get_original_user_name(x)))

    return sorted_data

    

# 合并并排序 zhuanping 和 zhuanfa 文件
sorted_zhuanping_data = filter_and_sort_file(zhuanping_file, sorted_users)
sorted_zhuanfa_data = filter_and_sort_file(zhuanfa_file, sorted_users)

# 合并两部分数据
combined_sorted_data = sorted_zhuanping_data + sorted_zhuanfa_data

# 将排序后的数据写入新的 JSONL 文件
with open(output_jsonl, 'w', encoding='utf-8') as f:
    for item in combined_sorted_data:
        json.dump(item, f, ensure_ascii=False)
        f.write('\n')

print(f"合并并排序后的数据已保存到 {output_jsonl}")
