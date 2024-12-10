

import json
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from matplotlib.font_manager import FontProperties
import os

# 读取JSONL文件
file_path = '/Users/jhx/Documents/Code/黑神话女性数据/黑神话女性all.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = [json.loads(line) for line in file]

# 提取text字段
texts = [entry['text'] for entry in data]

# 读取停词表
stopword_path = '/Users/jhx/Documents/Code/stopword.txt'
with open(stopword_path, 'r', encoding='utf-8') as file:
    stopwords = file.read().splitlines()

# 中文分词
texts_cut = [' '.join(jieba.cut(text)) for text in texts]

# 使用TF-IDF进行词频统计，调整max_features以改变保存的高频词数量
max_features = 100  # 设置保存的高频词数量

# 修改 TfidfVectorizer 的参数，确保与分词后的文本匹配
vectorizer = TfidfVectorizer(stop_words=stopwords, max_features=max_features, token_pattern=r"(?u)\b\w+\b", analyzer='word')

tfidf_matrix = vectorizer.fit_transform(texts_cut)

# 获取词汇和对应的TF-IDF值
feature_names = vectorizer.get_feature_names_out()
tfidf_scores = tfidf_matrix.toarray().sum(axis=0)

# 生成词频统计结果
tfidf_dict = dict(zip(feature_names, tfidf_scores))
sorted_tfidf = sorted(tfidf_dict.items(), key=lambda item: item[1], reverse=True)

# 构建JSON格式的结果
result = [{"word": word, "score": score} for word, score in sorted_tfidf]

# 保存为JSON文件
output_file = '/Users/jhx/Documents/Code/WeiboSpider/output/黑神话.jsonl'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

print("TF-IDF结果已保存为JSON格式。")

# 读取保存的JSON文件
with open(output_file, 'r', encoding='utf-8') as file:
    result = json.load(file)

# 构建词频字典
word_freq = {item['word']: item['score'] for item in result}

# 设置字体路径，确保字体文件存在
font_path = '/Users/jhx/Library/Fonts/SourceHanSansCN-Regular.otf'


# 生成词云图
wordcloud = WordCloud(font_path=font_path, width=800, height=400, background_color='white')

try:
    wordcloud.generate_from_frequencies(word_freq)
except AttributeError as e:
    print("出现 AttributeError，可能是由于 Pillow 库的版本导致的。")
    print("请尝试升级 wordcloud 库或降级 Pillow 库以解决此问题。")
    raise e

# 显示并保存词云图
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("黑神话", fontproperties=FontProperties(fname=font_path))

# 保存图片到与结果json文件相同的文件夹下
output_image_file = '/Users/jhx/Documents/Code/WeiboSpider/output/黑神话.png'
plt.savefig(output_image_file)

plt.show()