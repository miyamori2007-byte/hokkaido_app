import json
from datetime import datetime

SURVEY_FILE = "election_survey.json"

with open(SURVEY_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# 更新日時だけ自動更新（まずはここから）
data["analysis_date"] = datetime.now().strftime("%Y-%m-%d %H:%M")

with open(SURVEY_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("election_survey.json updated")
