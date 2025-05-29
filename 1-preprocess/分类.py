import json
import os

# 文件路径
input_file = '/Users/jhx/Documents/Code/黑神话女性数据/0数据/分开做LDA/蓝色.jsonl'
output_file = '/Users/jhx/Documents/Code/黑神话女性数据/0数据/分开做LDA/蓝色删除转发.jsonl'

# 计数器
delete_count = 0

try:
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            data = json.loads(line.strip())
            
            # 过滤掉所有 "retweeted_status" 中 "type" 为 "转发" 的数据
            if data.get("retweeted_status", {}).get("type") == "转发":
                delete_count += 1
                continue
            
            outfile.write(json.dumps(data, ensure_ascii=False) + '\n')

    print(f"删除了 {delete_count} 条 '转发' 数据。")

except FileNotFoundError:
    print("文件未找到，请检查文件路径是否正确。")
except Exception as e:
    print(f"发生错误：{e}")