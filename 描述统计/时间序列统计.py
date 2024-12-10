import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties

from matplotlib.font_manager import FontProperties

# 设置字体路径
font_path = "/Users/jhx/Library/Fonts/SourceHanSansCN-Regular.otf"
font_prop = FontProperties(fname=font_path)

# 输入文件路径
input_file = "/Users/jhx/Documents/Code/黑神话女性数据/黑神话女性all-情感分析.json"

# 加载 JSON 数据
data = []
with open(input_file, "r", encoding="utf-8") as file:
    for line in file:
        data.append(json.loads(line))

# 转换为 DataFrame
df = pd.DataFrame(data)

# 解析时间为 datetime 格式
df['time'] = pd.to_datetime(df['time'])

# 分类统计
df['sentiment'] = df['sentiment'].astype(str)
categories = df['sentiment'].unique()
grouped = df.groupby(['sentiment', pd.Grouper(key='time', freq='H')]).size().reset_index(name='count')

# 绘制时间序列图
plt.figure(figsize=(16, 8))  # 增大图像尺寸

# 按情感分类绘制不同曲线
colors = {"1": "blue", "2": "green", "0": "red"}
for sentiment in categories:
    subset = grouped[grouped['sentiment'] == sentiment]
    plt.plot(subset['time'], subset['count'], label=sentiment, color=colors.get(sentiment, 'gray'))


# 在绘图中显式应用字体
plt.title("情感倾向的讨论量时间序列统计", fontsize=18, fontproperties=font_prop)
plt.xlabel("时间", fontsize=14, fontproperties=font_prop)
plt.ylabel("讨论量", fontsize=14, fontproperties=font_prop)
plt.legend(title="情感倾向", fontsize=12, prop=font_prop)
plt.grid(True, linestyle='--', alpha=0.6)

# 保存结果
output_path = "/Users/jhx/Documents/Code/黑神话女性数据/黑神话情感讨论量统计.png"
plt.tight_layout()
plt.savefig(output_path, dpi=400, format='png')  # 增加分辨率
plt.show()