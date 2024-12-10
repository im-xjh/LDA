import json
import csv

# Path to your JSONL file
jsonl_file = '/Users/jhx/Documents/Code/黑神话女性数据/黑神话女性文本+用户信息.jsonl'

# Counters
total_entries = 0
retweeted_count = 0
type_zhuanfa = 0
type_zhuanping = 0

# Read the JSONL file
with open(jsonl_file, 'r', encoding='utf-8') as f:
    for line in f:
        total_entries += 1
        data = json.loads(line)
        if 'retweeted_status' in data and data['retweeted_status']:
            retweeted_count += 1
            retweeted_status = data['retweeted_status']
            if 'type' in retweeted_status:
                if retweeted_status['type'] == '转发':
                    type_zhuanfa += 1
                elif retweeted_status['type'] == '转评':
                    type_zhuanping += 1

# Write results to CSV
csv_file = 'retweeted_stats.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Total Entries', 'Retweeted Entries', 'Type: 转发', 'Type: 转评'])
    csv_writer.writerow([total_entries, retweeted_count, type_zhuanfa, type_zhuanping])

print(f"Statistics have been written to {csv_file}")
