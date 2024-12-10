import json

# 输入文件路径（原始数据文件）
data_file = "/Users/jhx/Documents/Code/黑神话女性数据/1-数据清洗/黑神话女性原始数据_cleaned.jsonl"
# 用户信息文件路径
user_file = "/Users/jhx/Documents/Code/黑神话女性数据/1-数据清洗/user_cleaned.jsonl"

# 将用户数据载入为字典，键为 id，值为用户信息字典
user_dict = {}
with open(user_file, "r", encoding="utf-8") as uf:
    for line in uf:
        u = json.loads(line.strip())
        user_dict[u["id"]] = u

# 输出文件路径（处理后的数据另存为新文件）
output_file = "/Users/jhx/Documents/Code/黑神话女性数据/1-数据清洗/黑神话女性数据处理结果.jsonl"

with open(data_file, "r", encoding="utf-8") as df, open(output_file, "w", encoding="utf-8") as of:
    for line in df:
        data = json.loads(line.strip())
        
        # 删除指定字段
        for field in ["sentiment", "reposts_count", "likes", "URL"]:
            if field in data:
                del data[field]
        
        # 根据 user_id 替换 user 信息
        if "user" in data and "id" in data["user"]:
            uid = data["user"]["id"]
            if uid in user_dict:
                uinfo = user_dict[uid]
                # 用 user_cleaned.jsonl 中的数据替换 user 字段
                data["user"] = {
                    "id": uinfo["id"],
                    "name": uinfo["nick_name"],
                    "followers_count": uinfo["followers_count"],
                    "friends_count": uinfo["friends_count"],
                    "statuses_count": uinfo["statuses_count"],
                    "gender": uinfo["gender"],
                    "birthday": uinfo["birthday"],
                    "created_at": uinfo["created_at"],
                    "desc_text": uinfo["desc_text"],
                    "ip_location": uinfo["ip_location"]
                }
        
        # 如果存在 retweeted_status，按 name 与 nick_name 匹配替换 retweeted_status.user
        if "retweeted_status" in data and "user" in data["retweeted_status"]:
            rt_user_name = data["retweeted_status"]["user"].get("name", None)
            if rt_user_name:
                matched_uid = None
                for uid, uinfo in user_dict.items():
                    if uinfo["nick_name"] == rt_user_name:
                        matched_uid = uid
                        break
                if matched_uid is not None:
                    uinfo = user_dict[matched_uid]
                    data["retweeted_status"]["user"] = {
                        "id": uinfo["id"],
                        "name": uinfo["nick_name"],
                        "followers_count": uinfo["followers_count"],
                        "friends_count": uinfo["friends_count"],
                        "statuses_count": uinfo["statuses_count"],
                        "gender": uinfo["gender"],
                        "birthday": uinfo["birthday"],
                        "created_at": uinfo["created_at"],
                        "desc_text": uinfo["desc_text"],
                        "ip_location": uinfo["ip_location"]
                    }

        # 将处理后的数据写入新文件
        of.write(json.dumps(data, ensure_ascii=False) + "\n")