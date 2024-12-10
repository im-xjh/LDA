import json
import re

input_file = '/Users/jhx/Documents/Code/WeiboSpider2/output/user_spider_20241210014305.jsonl'
output_file = '/Users/jhx/Documents/Code/黑神话女性数据/用户信息/用户信息增加.jsonl'

with open(input_file, 'r', encoding='utf-8') as f_in, \
     open(output_file, 'w', encoding='utf-8') as f_out:
    for line in f_in:
        line = line.strip()
        if not line:
            continue  # 跳过空行
        data = json.loads(line)
        
        # 删除指定字段
        fields_to_delete = ['avatar_hd', 'sunshine_credit', 'label_desc', 'crawl_time','verified','description','location','mbrank','mbtype','verified_type','verified_reason']
        for field in fields_to_delete:
            data.pop(field, None)  # 如果字段存在则删除
        
        # 将'id'转换为整数
        if 'id' in data:
            data['id'] = int(data['id'])
        
        # 处理'birthday'字段
        birthday = data.get('birthday', '')
        if birthday:
            # 检查生日是否以日期格式开头
            match = re.match(r'(\d{4}-\d{2}-\d{2})', birthday)
            if match:
                # 仅保留日期部分
                data['birthday'] = match.group(1)
            else:
                # 如果只有星座，设为空字符串
                data['birthday'] = ''
        
        # 将修改后的对象写入输出文件
        f_out.write(json.dumps(data, ensure_ascii=False) + '\n')
