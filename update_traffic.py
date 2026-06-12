import json
import os
import datetime

# 定义文件路径
DATE_STR = datetime.datetime.now().strftime("%Y-%m-%d")
PATHS_JSON = f"traffic/paths_{DATE_STR}.json"
TOTAL_RECORD_JSON = "traffic/historical_total_paths.json"
REPORT_MD = "流量统计报告.md"

# 1. 读取今日数据
if not os.path.exists(PATHS_JSON):
    print("找不到今日的流量 JSON 文件。")
    exit(0)

with open(PATHS_JSON, "r", encoding="utf-8") as f:
    today_data = json.load(f)

# 2. 读取历史累积数据
historical_data = {}
if os.path.exists(TOTAL_RECORD_JSON):
    with open(TOTAL_RECORD_JSON, "r", encoding="utf-8") as f:
        try:
            historical_data = json.load(f)
        except json.JSONDecodeError:
            historical_data = {}

# 3. 数据累加与更新
for item in today_data:
    path = item["path"]
    count = item["count"]
    uniques = item["uniques"]
    
    if path not in historical_data:
        historical_data[path] = {"count": count, "uniques": uniques}
    else:
        if count > historical_data[path]["count"]:
            historical_data[path]["count"] = count
        if uniques > historical_data[path]["uniques"]:
            historical_data[path]["uniques"] = uniques

# 储存更新后的历史总计 JSON
with open(TOTAL_RECORD_JSON, "w", encoding="utf-8") as f:
    json.dump(historical_data, f, indent=2, ensure_ascii=False)

# 4. 排序并生成 Markdown 报告
sorted_paths = sorted(historical_data.items(), key=lambda x: x[1]["count"], reverse=True)

# 读取旧的历史趋势表格 (保留每日 Views/Clones 表格)
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

# 重新写入 Markdown 
with open(REPORT_MD, "w", encoding="utf-8") as f:
    f.write("# LoRaModule 仓库流量统计报告\n")
    f.write("此文件由 GitHub Actions 自动生成，记录历史累计数据。\n\n")
    
    f.write(f"### 🏆 历史热门点击总排行榜 (自自动存档开始累计)\n")
    f.write("| 排名 | 热门点击路径 (Path) | 历史总浏览量 (估计) | 历史总独立访客 |\n")
    f.write("| :--- | :--- | :--- | :--- |\n")
    
    for idx, (path, data) in enumerate(sorted_paths, start=1):
        f.write(f"| {idx} | {path} | {data['count']} | {data['uniques']} |\n")
    
    f.write("\n### 📈 每日流量趋势历史\n")
    if old_hist_data:
        f.write(old_hist_data)

# 5. 🔥【新增】运行完毕后，立刻在本地删除今天的临时 JSON 文件，不留痕迹
try:
    os.remove(PATHS_JSON)
    os.remove(f"traffic/views_{DATE_STR}.json")
    os.remove(f"traffic/clones_{DATE_STR}.json")
    print("临时 JSON 文件已成功清理。")
except Exception as e:
    print(f"清理临时文件时发生错误: {e}")
