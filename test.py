import sxtwl
from datetime import datetime, timedelta

# 設定基本資訊
day = sxtwl.fromSolar(2002, 12, 31)
month_gz = day.getMonthGZ()
tg_index = month_gz.tg
dz_index = month_gz.dz

# 判斷大運方向（假設為陽女，step = -1）
step = 1  # ❗ 你可以改成 1 看順行結果

# 干支表
tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 計算大運
da_yun_schedule = []
for i in range(10):
    if step == 1:
        tg = tiangan[(tg_index + i + 1) % 10]
        dz = dizhi[(dz_index + i + 1) % 12]
    else:
        tg = tiangan[(tg_index - (i + 1)) % 10]
        dz = dizhi[(dz_index - (i + 1)) % 12]
    da_yun_schedule.append(f"{tg}{dz}")

# 輸出結果
print("大運干支：")
for dy in da_yun_schedule:
    print(dy)
