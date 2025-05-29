import json
import csv
import os
import requests
import logging
import sys
import time
from collections import deque

# 定义文件路径
input_file_path = ''    # 输入文件路径
output_file_path = ''   # 输出文件路径
stats_file_path = '' # 统计结果文件路径

# 百度API凭证 (请补充你的API_KEY和SECRET_KEY)
API_KEY = ''
SECRET_KEY = ''

# 设置日志记录
logging.basicConfig(
    filename='运行日志.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8',
)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(console_handler)

# 请求时间记录队列，用于控制 QPS
request_times = deque()


# 获取百度API Access Token
def get_access_token(api_key, secret_key):
    url = f'https://aip.baidubce.com/oauth/2.0/token'
    params = {
        'grant_type': 'client_credentials',
        'client_id': api_key,
        'client_secret': secret_key
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get('access_token')


def sentiment_analysis(text, access_token):
    url = f"https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token={access_token}"
    headers = {'Content-Type': 'application/json'}
    # 根据官方文档应使用 "text" 键传递文本内容
    data = {"text": text}

    # 控制 QPS，不超过每秒 2 次请求
    while True:
        current_time = time.time()
        while request_times and current_time - request_times[0] >= 1:
            request_times.popleft()
        if len(request_times) < 4:
            break
        time.sleep(1 - (current_time - request_times[0]))

    try:
        response = requests.post(url, headers=headers, json=data)
        request_times.append(time.time())
        response.raise_for_status()
        result = response.json()
        item = result.get("items", [{}])[0]
        return item.get("sentiment"), item.get("confidence"), item.get("positive_prob"), item.get("negative_prob")
    except Exception as e:
        logging.error("情感分析请求失败: %s", e)
        return None, None, None, None


def read_data(file_path):
    data = []
    if not os.path.exists(file_path):
        logging.error(f"文件不存在: {file_path}")
        return data
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for line_number, row in enumerate(reader, start=1):
            if "text" not in row or not row["text"]:
                logging.warning(f"第 {line_number} 行缺少 'text' 字段，跳过：{row}")
            else:
                data.append(row)
    logging.info(f"成功读取 {len(data)} 条数据")
    return data


# 写入 JSONL 文件
def write_data(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in data:
            json.dump(item, file, ensure_ascii=False)
            file.write('\n')


# 统计情感数据
def count_sentiments(data):
    sentiment_counts = {0: 0, 1: 0, 2: 0}
    for item in data:
        sentiment = item.get('sentiment')
        if sentiment in sentiment_counts:
            sentiment_counts[sentiment] += 1
    sentiment_labels = {0: '负面', 1: '中性', 2: '正面'}
    stats = {sentiment_labels[k]: v for k, v in sentiment_counts.items()}
    return stats


# 写入统计结果到 CSV
def write_stats_to_csv(stats, file_path):
    with open(file_path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['情感类型', '数量'])
        for sentiment, count in stats.items():
            writer.writerow([sentiment, count])


# 临时保存文件路径
progress_file_path = '/Users/jhx/Documents/Code/黑神话女性数据/0数据/sentiment_analysis_progress1.jsonl'


# 读取已保存的进度
def load_progress(file_path):
    processed_data = []
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                processed_data.append(json.loads(line.strip()))
    logging.info(f"已加载 {len(processed_data)} 条已处理数据")
    return processed_data


# 写入已处理数据到进度文件
def save_progress(data, file_path):
    with open(file_path, 'a', encoding='utf-8') as file:
        for item in data:
            json.dump(item, file, ensure_ascii=False)
            file.write('\n')


# 修改情感分析函数以支持进度保存
def perform_sentiment_analysis(data, access_token, output_file_path, progress_file_path, report_interval=100):
    processed_data = load_progress(progress_file_path)
    # 尝试获取 'text' 字段，如不存在则使用 'content'
    processed_texts = {item.get('text', item.get('content')) for item in processed_data if item.get('text') or item.get('content')}
    total_items = len(data)

    for index, item in enumerate(data):
        # 根据当前记录的数据结构，确保使用 'text' 字段进行对比
        current_text = item.get('text', item.get('content'))
        if current_text in processed_texts:
            continue  # 跳过已处理的内容

        sentiment, confidence, positive_prob, negative_prob = sentiment_analysis(current_text, access_token)
        # 更新记录时统一使用 'text' 字段
        item.update({
            'text': current_text,
            'sentiment': sentiment,
            'confidence': confidence,
            'positive_prob': positive_prob,
            'negative_prob': negative_prob
        })
        save_progress([item], progress_file_path)  # 逐条保存进度

        if (index + 1) % report_interval == 0:
            logging.info(f"已完成 {index + 1}/{total_items} 条情感分析...")
            write_data(data[:index + 1], output_file_path)

    write_data(data, output_file_path)
    return data


# 修改主函数支持进度恢复
def main(input_path, output_path, stats_path, progress_path, api_key, secret_key):
    access_token = get_access_token(api_key, secret_key)
    logging.info("成功获取 Access Token")

    data = read_data(input_path)
    data = perform_sentiment_analysis(data, access_token, output_path, progress_path)
    logging.info("情感分析完成，结果已保存到文件")

    stats = count_sentiments(data)
    write_stats_to_csv(stats, stats_path)
    logging.info(f"情感统计结果已保存到 CSV 文件：{stats_path}")


if __name__ == "__main__":
    main(input_file_path, output_file_path, stats_file_path, progress_file_path, API_KEY, SECRET_KEY)
