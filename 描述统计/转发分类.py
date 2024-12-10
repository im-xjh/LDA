import json

# 输入文件路径
input_file = '/Users/jhx/Documents/Code/黑神话女性数据/黑神话女性文本+用户信息.jsonl'

# 输出文件路径
no_retweet_file = 'no_retweet.jsonl'
zhuanfa_file = 'zhuanfa.jsonl'
zhuanping_file = 'zhuanping.jsonl'

# 打开输出文件
with open(no_retweet_file, 'w', encoding='utf-8') as no_retweet_f, \
     open(zhuanfa_file, 'w', encoding='utf-8') as zhuanfa_f, \
     open(zhuanping_file, 'w', encoding='utf-8') as zhuanping_f:

    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line.strip())
            if 'retweeted_status' not in data or not data['retweeted_status']:
                # 没有转发数据的
                no_retweet_f.write(json.dumps(data, ensure_ascii=False) + '\n')
            else:
                retweeted_status = data['retweeted_status']
                if 'type' in retweeted_status:
                    if retweeted_status['type'] == '转发':
                        # 转发
                        zhuanfa_f.write(json.dumps(data, ensure_ascii=False) + '\n')
                    elif retweeted_status['type'] == '转评':
                        # 转评
                        zhuanping_f.write(json.dumps(data, ensure_ascii=False) + '\n')
                    else:
                        # 其他类型，视为没有转发数据
                        no_retweet_f.write(json.dumps(data, ensure_ascii=False) + '\n')
                else:
                    # 没有type字段，视为没有转发数据
                    no_retweet_f.write(json.dumps(data, ensure_ascii=False) + '\n')

print("数据已分类完成，分别输出到以下文件：")
print(f"没有转发数据的：{no_retweet_file}")
print(f"转发的：{zhuanfa_file}")
print(f"转评的：{zhuanping_file}")
