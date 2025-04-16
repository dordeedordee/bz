import sxtwl
from datetime import datetime, timedelta


# 測試生日
birth_datetime = datetime(2002, 12, 31)

birth_year = 2002
birth_month = 12
birth_day = 31
birth_hour = 6
gender = "女"
#gender = "男"


tian_gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
di_zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
# 十神關係對照表（以日元為基準，考慮陰陽）
shishen_table = {
    "甲": {"甲": "比", "乙": "劫", "丙": "食", "丁": "傷", "戊": "財", "己": "才", "庚": "殺", "辛": "官", "壬": "枭", "癸": "印"},
    "乙": {"甲": "劫", "乙": "比", "丙": "傷", "丁": "食", "戊": "才", "己": "財", "庚": "官", "辛": "殺", "壬": "印", "癸": "枭"},
    "丙": {"丙": "比", "丁": "劫", "戊": "食", "己": "傷", "庚": "財", "辛": "才", "壬": "殺", "癸": "官", "甲": "枭", "乙": "印"},
    "丁": {"丙": "劫", "丁": "比", "戊": "傷", "己": "食", "庚": "才", "辛": "財", "壬": "官", "癸": "殺", "甲": "印", "乙": "枭"},
    "戊": {"戊": "比", "己": "劫", "庚": "食", "辛": "傷", "壬": "財", "癸": "才", "甲": "殺", "乙": "官", "丙": "枭", "丁": "印"},
    "己": {"戊": "劫", "己": "比", "庚": "傷", "辛": "食", "壬": "才", "癸": "財", "甲": "官", "乙": "殺", "丙": "印", "丁": "枭"},
    "庚": {"庚": "比", "辛": "劫", "壬": "食", "癸": "傷", "甲": "財", "乙": "才", "丙": "殺", "丁": "官", "戊": "枭", "己": "印"},
    "辛": {"庚": "劫", "辛": "比", "壬": "傷", "癸": "食", "甲": "才", "乙": "財", "丙": "官", "丁": "殺", "戊": "印", "己": "枭"},
    "壬": {"壬": "比", "癸": "劫", "甲": "食", "乙": "傷", "丙": "財", "丁": "才", "戊": "殺", "己": "官", "庚": "枭", "辛": "印"},
    "癸": {"壬": "劫", "癸": "比", "甲": "傷", "乙": "食", "丙": "才", "丁": "財", "戊": "官", "己": "殺", "庚": "印", "辛": "枭"}
}
# 地支十神對照表（根據圖片更新）
dizhi_shishen_table = {
    "甲": {"子": "枭", "丑": "財", "寅": "比", "卯": "劫", "辰": "才", "巳": "傷", "午": "食", "未": "財", "申": "殺", "酉": "官", "戌": "才", "亥": "印"},
    "乙": {"子": "印", "丑": "才", "寅": "劫", "卯": "比", "辰": "財", "巳": "食", "午": "傷", "未": "才", "申": "官", "酉": "殺", "戌": "財", "亥": "枭"},
    "丙": {"子": "官", "丑": "傷", "寅": "枭", "卯": "印", "辰": "食", "巳": "劫", "午": "比", "未": "傷", "申": "財", "酉": "才", "戌": "食", "亥": "殺"},
    "丁": {"子": "殺", "丑": "食", "寅": "印", "卯": "枭", "辰": "傷", "巳": "比", "午": "劫", "未": "食", "申": "才", "酉": "財", "戌": "傷", "亥": "官"},
    "戊": {"子": "才", "丑": "劫", "寅": "殺", "卯": "官", "辰": "比", "巳": "印", "午": "枭", "未": "劫", "申": "食", "酉": "傷", "戌": "比", "亥": "財"},
    "己": {"子": "財", "丑": "比", "寅": "官", "卯": "殺", "辰": "劫", "巳": "枭", "午": "印", "未": "比", "申": "傷", "酉": "食", "戌": "劫", "亥": "才"},
    "庚": {"子": "食", "丑": "印", "寅": "財", "卯": "才", "辰": "枭", "巳": "官", "午": "殺", "未": "印", "申": "比", "酉": "劫", "戌": "枭", "亥": "傷"},
    "辛": {"子": "傷", "丑": "枭", "寅": "才", "卯": "財", "辰": "印", "巳": "殺", "午": "官", "未": "枭", "申": "劫", "酉": "比", "戌": "印", "亥": "食"},
    "壬": {"子": "比", "丑": "官", "寅": "食", "卯": "傷", "辰": "殺", "巳": "財", "午": "才", "未": "官", "申": "印", "酉": "枭", "戌": "殺", "亥": "劫"},
    "癸": {"子": "劫", "丑": "殺", "寅": "傷", "卯": "食", "辰": "官", "巳": "才", "午": "財", "未": "殺", "申": "枭", "酉": "印", "戌": "官", "亥": "比"}
}
# 節氣名稱對照表（避免使用不存在的 sxtwl.JIE_QI）
jieqi_names = [
    "小寒", "大寒", "立春", "雨水", "驚蟄", "春分",
    "清明", "穀雨", "立夏", "小滿", "芒種", "夏至",
    "小暑", "大暑", "立秋", "處暑", "白露", "秋分",
    "寒露", "霜降", "立冬", "小雪", "大雪", "冬至"
]

def calculate_da_yun_info(birth_datetime: datetime, gender: str, nian_gan: str):
    # 查立春時間以調整出生年是否需視為前一年
    day_check = sxtwl.fromSolar(birth_datetime.year, birth_datetime.month, birth_datetime.day)
    while True:
        if day_check.hasJieQi():
            if jieqi_names[day_check.getJieQi()] == '立春':
                spring_day = day_check
                break
        day_check = day_check.after(-1)

    spring_jd = spring_day.getJieQiJD()
    spring_dt_raw = sxtwl.JD2DD(spring_jd)
    spring_datetime = datetime(int(spring_dt_raw.Y), int(spring_dt_raw.M), int(spring_dt_raw.D), int(spring_dt_raw.h), int(spring_dt_raw.m), int(round(spring_dt_raw.s)))

    # 若出生在立春之前，視為前一年
    adjusted_year = birth_datetime.year - 1 if birth_datetime < spring_datetime else birth_datetime.year

    # 判斷年干陰陽（用年干來判斷大運方向）
    yang_gan = {'甲', '丙', '戊', '庚', '壬'}
    is_yang = nian_gan in yang_gan
    step = 1 if (gender == '男' and is_yang) or (gender == '女' and not is_yang) else -1
    print(gender)
    
    # 🌟 根據陰陽性別選擇順推或逆推節氣
    search_day = sxtwl.fromSolar(birth_datetime.year, birth_datetime.month, birth_datetime.day)
    while True:
        search_day = search_day.after(step)
        if search_day.hasJieQi():
            jieqi_index = search_day.getJieQi()
            jieqi_name = jieqi_names[jieqi_index]
            jieqi_jd = search_day.getJieQiJD()
            t = sxtwl.JD2DD(jieqi_jd)
            jieqi_datetime = datetime(int(t.Y), int(t.M), int(t.D), int(t.h), int(t.m), int(round(t.s)))
            break

    # 顯示取得的節氣名稱與時間
    print(f"取得節氣名稱：{jieqi_name}")
    print(f"節氣時間：{jieqi_datetime}")
    
    # 計算距離天數和時辰（1時辰 = 2小時）
    delta = jieqi_datetime - birth_datetime if step == 1 else birth_datetime - jieqi_datetime
    print(delta)
    total_seconds = abs(delta.total_seconds())
    total_days = int(total_seconds // 86400)
    remaining_seconds = total_seconds % 86400
    remaining_hours = remaining_seconds / 3600
    shichen = int(round(remaining_hours / 2))

    # 三日為一年，一個時辰相當於10天（1/3歲）
    total_days_equiv = total_days + shichen * 10 / 30
    print(total_days_equiv)
    qi_yun_age = int(total_days_equiv // 3) + (1 if total_days_equiv % 3 > 0 else 0)
    print(qi_yun_age)
    
    start_year = birth_datetime.year + qi_yun_age

    tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    #month_gz = day.getMonthGZ()
    #tg_index = month_gz.tg
    #dz_index = month_gz.dz
    # 用出生當日的月柱來當作大運起點
    birth_day = sxtwl.fromSolar(birth_datetime.year, birth_datetime.month, birth_datetime.day)
    birth_month_gz = birth_day.getMonthGZ()
    tg_index = birth_month_gz.tg
    dz_index = birth_month_gz.dz

    print(tg_index)
    print("🌟 大運起始月干支：", tiangan[tg_index], dizhi[dz_index])
    print("🌟 判斷方向：", "順行" if step == 1 else "逆行")


    da_yun_schedule = []
    for i in range(10):
        if step == 1:
            tg = tiangan[(tg_index + i + 1) % 10]
            dz = dizhi[(dz_index + i + 1) % 12]
            print(f"{i+1} 運：{tg}{dz}（干位置：{(tg_index + i + 1) % 10}，支位置：{(dz_index + i + 1) % 12}）")
        else:
            tg = tiangan[(tg_index - (i + 1)) % 10]
            dz = dizhi[(dz_index - (i + 1)) % 12]
        age = int(qi_yun_age) + i * 10 + 1
        year = start_year + i * 10
        da_yun_schedule.append(f"{age}歲 ({year}) - {tg}{dz}")

    return {
        '大運方向': '順行' if step == 1 else '逆行',
        '節氣時間': jieqi_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        '起運年齡（歲）': qi_yun_age,
        '大運': da_yun_schedule
    }


def get_bazi(year: int, month: int, day: int, hour: int):
    day_data = sxtwl.fromSolar(year, month, day)  # 轉換為農曆對象

    # 計算年柱（立春為界）
    yTG = day_data.getYearGZ()  # 以立春為界的年干支
    year_gan = tian_gan[yTG.tg]
    year_zhi = di_zhi[yTG.dz]

    # 計算月柱
    mTG = day_data.getMonthGZ()
    month_gan = tian_gan[mTG.tg]
    month_zhi = di_zhi[mTG.dz]

    # 計算日柱
    dTG = day_data.getDayGZ()
    day_gan = tian_gan[dTG.tg]
    day_zhi = di_zhi[dTG.dz]

    # 計算時柱
    sTG = day_data.getHourGZ(hour)
    hour_gan = tian_gan[sTG.tg]
    hour_zhi = di_zhi[sTG.dz]

    bazi = {
        "公曆": f"{day_data.getSolarYear()}年{day_data.getSolarMonth()}月{day_data.getSolarDay()}日 {hour}:00",
        "年柱": (year_gan, year_zhi),
        "月柱": (month_gan, month_zhi),
        "日柱": (day_gan, day_zhi),
        "時柱": (hour_gan, hour_zhi)
    }
    
    print(f"\n")
    print(f"公曆出生日期: {bazi['公曆']}")
    print("時 日 月 年")
    print(f"{shishen_table[day_gan][bazi['時柱'][0]]} 元 {shishen_table[day_gan][bazi['月柱'][0]]} {shishen_table[day_gan][bazi['年柱'][0]]} ")
    print(f"{bazi['時柱'][0]} {bazi['日柱'][0]} {bazi['月柱'][0]} {bazi['年柱'][0]}")
    print(f"{bazi['時柱'][1]} {bazi['日柱'][1]} {bazi['月柱'][1]} {bazi['年柱'][1]}")
    print(f"{dizhi_shishen_table[day_gan][bazi['時柱'][1]]} {dizhi_shishen_table[day_gan][bazi['日柱'][1]]} {dizhi_shishen_table[day_gan][bazi['月柱'][1]]} {dizhi_shishen_table[day_gan][bazi['年柱'][1]]} ")
    print(f"\n")
    return bazi


bazi = get_bazi(birth_year, birth_month, birth_day, birth_hour)
birth_str = bazi['公曆'].replace("年", "-").replace("月", "-").replace("日", "")
birth_datetime = datetime.strptime(birth_str.split()[0] + " " + birth_str.split()[1], "%Y-%m-%d %H:%M")
nian_gan = bazi['年柱'][0]
da_yun_info = calculate_da_yun_info(birth_datetime, gender, nian_gan)

#for line in da_yun_info['大運']:
#    print(line)
