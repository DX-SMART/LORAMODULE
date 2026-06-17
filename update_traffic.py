import json
import os
import datetime

# 定义文件路径
DATE_STR = datetime.datetime.now().strftime("%Y-%m-%d")
PATHS_JSON = f"traffic/paths_{DATE_STR}.json"
REFERRERS_JSON = f"traffic/referrers_{DATE_STR}.json"
TOTAL_RECORD_JSON = "traffic/historical_total_paths.json"
TOTAL_REFERRERS_JSON = "traffic/historical_total_referrers.json"
REPORT_MD = "流量统计报告.md"

# ==================== 1. 处理 热门点击路径 (Paths) ====================
today_paths = []
if os.path.exists(PATHS_JSON):
    with open(PATHS_JSON, "r", encoding="utf-8") as f:
        today_paths = json.load(f)

historical_paths = {}
if os.path.exists(TOTAL_RECORD_JSON):
    with open(TOTAL_RECORD_JSON, "r", encoding="utf-8") as f:
        try: historical_paths = json.load(f)
        except json.JSONDecodeError: historical_paths = {}

for item in today_paths:
    path = item["path"]
    count = item["count"]
    uniques = item["uniques"]
    if path not in historical_paths:
        historical_paths[path] = {"count": count, "uniques": uniques}
    else:
        if count > historical_paths[path]["count"]: historical_paths[path]["count"] = count
        if uniques > historical_paths[path]["uniques"]: historical_paths[path]["uniques"] = uniques

with open(TOTAL_RECORD_JSON, "w", encoding="utf-8") as f:
    json.dump(historical_paths, f, indent=2, ensure_ascii=False)

# ==================== 2. 🔥【新增】处理 引流网站来源 (Referrers) ====================
today_referrers = []
if os.path.exists(REFERRERS_JSON):
    with open(REFERRERS_JSON, "r", encoding="utf-8") as f:
        today_referrers = json.load(f)

historical_referrers = {}
if os.path.exists(TOTAL_REFERRERS_JSON):
    with open(TOTAL_REFERRERS_JSON, "r", encoding="utf-8") as f:
        try: historical_referrers = json.load(f)
        except json.JSONDecodeError: historical_referrers = {}

for item in today_referrers:
    site = item["referrer"]
    count = item["count"]
    uniques = item["uniques"]
    if site not in historical_referrers:
        historical_referrers[site] = {"count": count, "uniques": uniques}
    else:
        # 引流网站通常是每日波动的独立来源，这里我们采用累加(+=)算法来计算全时期总曝光
        historical_referrers[site]["count"] += count
        historical_referrers[site]["uniques"] += uniques

with open(TOTAL_REFERRERS_JSON, "w", encoding="utf-8") as f:
    json.dump(historical_referrers, f, indent=2, ensure_ascii=False)

# ==================== 3. 排序并重新生成 Markdown 报告 ====================
sorted_paths = sorted(historical_paths.items(), key=lambda x: x[1]["count"], reverse=True)
sorted_referrers = sorted(historical_referrers.items(), key=lambda x: x[1]["count"], reverse=True)

old_hist_data = ""
if os.path.exists(REPORT_MD):
    with open(REPORT_MD, "r", encoding="utf-8") as f:
        lines = f.readlines()
        start_collect = False
        for line in lines:
            if "| 日期 |" in line or start_collect:
                start_collect = True
                if "###" not in line or "| 日期 |" in line:
                    old_hist_data += line

with open(REPORT_MD, "w", encoding="utf-8") as f:
    f.write("# LoRaModule 仓库流量统计报告\n")
    f.write("此文件由 GitHub Actions 自动生成，记录历史累计数据。\n\n")
    
    # 路径表格
    f.write(f"### 🏆 历史热门点击总排行榜 (自自动存档开始累计)\n")
    f.write("| 排名 | 热门点击路径 (Path) | 历史总浏览量 (估计) | 历史总独立访客 |\n")
    f.write("| :--- | :--- | :--- | :--- |\n")
    for idx, (path, data) in enumerate(sorted_paths, start=1):
        f.write(f"| {idx} | {path} | {data['count']} | {data['uniques']} |\n")
    
    # 🔥【新增】引流网站来源表格
    f.write(f"\n### 🌐 历史引流渠道总排行榜 (全时期累计)\n")
    f.write("| 排名 | 来源渠道 (Site) | 累计总引流量 (Views) | 累计总独立来访人数 |\n")
    f.write("| :--- | :--- | :--- | :--- |\n")
    for idx, (site, data) in enumerate(sorted_referrers, start=1):
        f.write(f"| {idx} | {site} | {data['count']} | {data['uniques']} |\n")
    
    # 历史趋势
    f.write("\n### 📈 每日流量趋势历史\n")
    if old_hist_data:
        f.write(old_hist_data)

# ==================== 4. 🧹 运行完毕后，在本地删除临时文件 ====================
try:
    for filename in [PATHS_JSON, REFERRERS_JSON, f"traffic/views_{DATE_STR}.json", f"traffic/clones_{DATE_STR}.json"]:
        if os.path.exists(filename): os.remove(filename)
    print("临时 JSON 文件已成功清理。")
except Exception as e:
    print(f"清理临时文件时发生错误: {e}")
