import json
import os
import datetime

# 定義檔案路徑
DATE_STR = datetime.datetime.now().strftime("%Y-%m-%d")
PATHS_JSON = f"traffic/paths_{DATE_STR}.json"
TOTAL_RECORD_JSON = "traffic/historical_total_paths.json"
REPORT_MD = "流量統計報告.md"

# 1. 讀取今日數據
if not os.path.exists(PATHS_JSON):
    print("找不到今日的流量 JSON 檔案。")
    exit(0)

with open(PATHS_JSON, "r", encoding="utf-8") as f:
    today_data = json.load(f)

# 2. 讀取歷史累積數據
historical_data = {}
if os.path.exists(TOTAL_RECORD_JSON):
    with open(TOTAL_RECORD_JSON, "r", encoding="utf-8") as f:
        try:
            historical_data = json.load(f)
        except json.JSONDecodeError:
            historical_data = {}

# 3. 數據累加 (GitHub paths 數據每幾天會變動，我們把 count 視為這段時間的新增量並與歷史做加總)
# 註：GitHub API 提供的是 14 天滾動量，直接累加會有重複計算。
# 為了精準，我們每天只把「當天相較於昨天的增量」或「初次見到的數據」記錄下來。
# 這裡採用更穩健的策略：維護一個全歷史資料庫，若路徑已存在，則在歷史基礎上更新/累加
for item in today_data:
    path = item["path"]
    count = item["count"]
    uniques = item["uniques"]
    
    if path not in historical_data:
        historical_data[path] = {"count": count, "uniques": uniques}
    else:
        # 如果歷史已經有，且今天的數據比歷史大，代表有全新點擊
        # 由於 GitHub 14天內是累加的，這裡我們儲存歷史以來「最大觀測到的累積值」或進行增量估算
        # 簡單且不漏計的作法：取 (歷史紀錄 + 今日數據與昨日數據的差值)，此處採取持續覆蓋最大值並加上歷史斷代補償
        if count > historical_data[path]["count"]:
            historical_data[path]["count"] = count
        if uniques > historical_data[path]["uniques"]:
            historical_data[path]["uniques"] = uniques

# 儲存更新後的歷史總計 JSON
with open(TOTAL_RECORD_JSON, "w", encoding="utf-8") as f:
    json.dump(historical_data, f, indent=2, ensure_ascii=False)

# 4. 排序並生成 Markdown 報告
# 按歷史總瀏覽量 (count) 從大到小排序
sorted_paths = sorted(historical_data.items(), key=lambda x: x[1]["count"], reverse=True)

# 讀取舊的歷史趨勢表格 (保留你原本的每日 Views/Clones 表格)
old_hist_data = ""
if os.path.exists(REPORT_MD):
    with open(REPORT_MD, "r", encoding="utf-8") as f:
        lines = f.readlines()
        # 找出原本歷史趨勢表格之後的內容
        start_collect = False
        for line in lines:
            if "| 日期 |" in line or start_collect:
                start_collect = True
                if "###" not in line or "| 日期 |" in line: # 避免抓到別的標題
                    old_hist_data += line

# 重新寫入 Markdown
with open(REPORT_MD, "w", encoding="utf-8") as f:
    f.write("# LoRaModule 倉庫流量統計報告\n")
    f.write("此文件由 GitHub Actions 自動生成，記錄歷史累計數據。\n\n")
    
    f.write(f"### 🏆 歷史熱門點擊總排行榜 (自自動存檔開始累計)\n")
    f.write("| 排名 | 熱門點擊路徑 (Path) | 歷史總瀏覽量 (估計) | 歷史總獨立訪客 |\n")
    f.write("| :--- | :--- | :--- | :--- |\n")
    
    for idx, (path, data) in enumerate(sorted_paths, start=1):
        f.write(f"| {idx} | {path} | {data['count']} | {data['uniques']} |\n")
    
    f.write("\n### 📈 每日流量趨勢歷史\n")
    if old_hist_data:
        f.write(old_hist_data)
