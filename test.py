import sxtwl
from datetime import datetime, timedelta


# 測試生日
birth_datetime = datetime(2002, 12, 31)

# 干支表
tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 用出生那天取月柱（你 debug snippet 的寫法）
birth_day = sxtwl.fromSolar(birth_datetime.year, birth_datetime.month, birth_datetime.day)
birth_month_gz = birth_day.getMonthGZ()
print("🔹 出生日取得的月柱：", tiangan[birth_month_gz.tg] + dizhi[birth_month_gz.dz])

# 模擬主程式中的處理邏輯：從出生日起往前/後找節氣
step = -1  # 假設是陰陽女用逆行，可改成 +1 測順行
day = sxtwl.fromSolar(birth_datetime.year, birth_datetime.month, birth_datetime.day)
while True:
    day = day.after(step)
    if day.hasJieQi():
        month_gz = day.getMonthGZ()
        print("🔸 主程式找節氣取得的月柱：", tiangan[month_gz.tg] + dizhi[month_gz.dz])
        break

# 設定基本資訊
day = sxtwl.fromSolar(2002, 12, 31)
month_gz = day.getMonthGZ()
tg_index = month_gz.tg
dz_index = month_gz.dz

#print(tg_index)

# 判斷大運方向（假設為陽女，step = -1）
step = 1  # ❗ 你可以改成 1 看順行結果

# 干支表
tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 計算大運
da_yun_schedule = []
for i in range(10):
    if step == 1:
        print(tg_index)
        print(tg_index + i + 1)
        print((tg_index + i + 1) % 10)
        print(tiangan[(tg_index + i + 1) % 10])
        tg = tiangan[(tg_index + i + 1) % 10]
        dz = dizhi[(dz_index + i + 1) % 12]
    else:
        print(tg_index)
        print(tg_index - (i + 1))
        print((tg_index - (i + 1)) % 10)
        print(tiangan[(tg_index - (i + 1)) % 10])
        tg = tiangan[(tg_index - (i + 1)) % 10]
        dz = dizhi[(dz_index - (i + 1)) % 12]
    da_yun_schedule.append(f"{tg}{dz}")

# 輸出結果
#print("大運干支：")
#for dy in da_yun_schedule:
#    print(dy)
