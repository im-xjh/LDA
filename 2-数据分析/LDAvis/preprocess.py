# -*- coding: utf-8 -*-

# 文本预处理

import os
import pandas as pd
import re
import jieba
import jieba.posseg as psg
import json
from tqdm import tqdm

# 设置文件路径
data_file = '/Users/jhx/Documents/Code/黑神话女性数据/0数据/黑神话女性_cleaned.jsonl'  # 原始数据文件路径
stop_file = '/Users/jhx/Documents/Code/stopword.txt'  # 停用词文件路径
dic_file = '/Users/jhx/Documents/Code/黑神话女性数据/数据分析/LDAvis/dic.txt'

def main():
    # 1. 读取数据，保留全部原始字段
    data = []
    with open(data_file, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            # 保证text字段存在，不存在则跳过
            text = item.get('text', '')
            if text:
                data.append(item)
    data = pd.DataFrame(data)

    # 2. 文本预处理
    if dic_file:
        try:
            jieba.load_userdict(dic_file)
            print(f"自定义词典 '{dic_file}' 加载成功。")
        except Exception as e:
            print(f"加载自定义词典时发生错误：{e}")
    jieba.initialize()

    try:
        with open(stop_file, encoding='utf-8') as f:
            stopword_list = f.readlines()
    except:
        stopword_list = []
        print("停用词文件读取错误")

    stop_list = [re.sub(u'\n|\\r', '', line).strip() for line in stopword_list]

    def chinese_word_cut(mytext):
        word_list = []
        seg_list = psg.cut(mytext)
        for seg_word in seg_list:
            word = re.sub(u'[^\u4e00-\u9fa5]', '', seg_word.word)
            if len(word) == 0:
                continue
            if word in stop_list:
                continue
            if len(word) < 2:
                continue
            word_list.append(word)
        return ' '.join(word_list)

    tqdm.pandas()
    print("正在进行文本预处理...")
    data['text_processed'] = data['text'].progress_apply(chinese_word_cut)
    print("文本预处理完成。")

    # 3. 保存预处理后的数据，不仅保留text_processed，还保留原始所有字段
    preprocessed_file = 'preprocessed_data.jsonl'
    data.to_json(preprocessed_file, orient='records', lines=True, force_ascii=False)
    print(f"预处理后的数据已保存为 '{preprocessed_file}' 文件。")

if __name__ == '__main__':
    main()