import json
import re
import os

# 输入文件路径
input_file = '/Users/jhx/Documents/Code/黑神话女性数据/0数据/黑神话女性_cleaned.jsonl'

# 自动生成输出文件路径，在输入文件名后添加 '_cleaned'
base, ext = os.path.splitext(input_file)
output_file = base + '_cleaned' + ext


keywords = [
    r'\[[\u4e00-\u9fff]+\]',  # 匹配 [中文内容]
    '👍', '🤣', '🔻', '1️⃣',
    r'IMG', r'OCR', r'#', r'\$', r'%', r'\^', r'&', r'\*', r'@', r'URL',
    r'OCR:IMG:\[IMG\d+\]',  # 匹配 OCR:IMG:[IMG0] 形式
    '查看图片',
    '评论配图',
    r'凸\d+\[BR\]\[IMG\d+\]\d+-\d+来自iPhone客户端',  # 匹配特定格式
    '来自iPhone客户端',
    r'凸赞\[BR\]\[IMG\d+\]\d+-\d+来自iPhone客户端',
    '回复',
    '，，，，',
    'Repost Weibo', r'Repost',
    '#恋与深空',
    '视频下方评论',
    '请谨慎评论',
    '分享图片',
    
    # 新增匹配规则：
    # 匹配类似[doge]、[笑cry]、[good]、[打call]、[哆啦A梦害怕]等表情标记
    r'\[[^\]]+\]',
    # 匹配URL，如http://t.cn/A68D4wbM
    r'http\S+',
    # 删除特定字符串
    '置顶24-9-1509:13',
    '来自iPhone12ProMax',
    '🤗', '🤩', '💙', r'\.\.\.', r'​​::', r'\[0\]'
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