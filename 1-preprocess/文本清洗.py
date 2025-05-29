import json
import re
import os

# 输入文件路径
input_file = '/Users/jhx/Documents/Code/黑神话女性数据/0数据/antifeminism.jsonl'

# 自动生成输出文件路径，在输入文件名后添加 '_cleaned'
base, ext = os.path.splitext(input_file)
output_file = base + '_cleaned' + ext


keywords = [
    r'\[[\u4e00-\u9fff]+\]', 
    r'\[[^\]]+\]',
    '👍', '🤣', '🔻', '1️⃣','🤗', '🤩', '💙',
    r'IMG', r'OCR', r'URL',
    r'OCR:IMG:\[IMG\d+\]',  # 匹配 OCR:IMG:[IMG0] 形式
    r'凸\d+\[BR\]\[IMG\d+\]\d+-\d+来自iPhone客户端',  
    '来自iPhone客户端',
    r'凸赞\[BR\]\[IMG\d+\]\d+-\d+来自iPhone客户端',
    '回复',
    'Repost Weibo', 
    r'Repost',
    r'http\S+',
    '#恋与深空',
    '视频下方评论',
    '分享图片',
    '查看图片',
    '评论配图',
    '置顶24-9-1509:13',
    r'\.\.\.', r'\[0\]',
    r'\d+分钟前来自iPhone[\dA-Za-z]+',
    r'http\S*[A-Za-z]',
    r'回复@[^:]+:',
    r'@[^:]+:'
]

# 编译正则表达式模式，忽略大小写
patterns = [re.compile(k, re.IGNORECASE) for k in keywords]

# 打开输入和输出文件
with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8') as outfile:
    for line in infile:
        data = json.loads(line)
        text = data.get('text', '')
        
        # 对文本进行清洗，删除指定的关键词或模式
        for pattern in patterns:
            text = pattern.sub('', text)
        
        data['text'] = text.strip()
        
        outfile.write(json.dumps(data, ensure_ascii=False) + '\n')