import subprocess
import sys

print("=== Start auto update ===")

# ① 世論調査の更新
subprocess.run([sys.executable, "update_survey.py"], check=True)

# ② 選挙予測の再計算
subprocess.run([sys.executable, "predict.py"], check=True)

print("=== Auto update finished ===")
from datetime import datetime

# update_survey + predict.py 実行後
last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ファイルに書き出す
with open("last_updated.txt", "w", encoding="utf-8") as f:
    f.write(last_updated)
