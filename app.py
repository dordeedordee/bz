import streamlit as st
from datetime import datetime
import sxtwl  # 四象推命庫

tian_gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
di_zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 藏干對照表
zang_gan_table = {
    "子": ["癸"], "丑": ["己", "癸", "辛"], "寅": ["甲", "丙", "戊"], "卯": ["乙"],
    "辰": ["戊", "乙", "癸"], "巳": ["丙", "庚", "戊"], "午": ["丁", "己"],
    "未": ["己", "丁", "乙"], "申": ["庚", "壬", "戊"], "酉": ["辛"],
    "戌": ["戊", "辛", "丁"], "亥": ["壬", "甲"]
}

# 得祿對照表
de_lu_table = {
    "甲": "寅", "乙": "卯", "丙": "巳", "丁": "午", "戊": "巳",
    "己": "午", "庚": "申", "辛": "酉", "壬": "亥", "癸": "子"
}

# 天乙貴人對照表
# 以天干為主，對應可作為天乙貴人的地支
tian_yi_gui_ren = {
    "甲": ["丑", "未"],
    "乙": ["子", "申"],
    "丙": ["亥", "酉"],
    "丁": ["亥", "酉"],
    "戊": ["丑", "未"],
    "己": ["子", "申"],
    "庚": ["丑", "未"],
    "辛": ["寅", "午"],
    "壬": ["卯", "巳"],
    "癸": ["卯", "巳"]
}

# 太極貴人對照表
taiji_gui_ren = {
    "甲": ["子", "午"], "乙": ["子", "午"],
    "丙": ["卯", "酉"], "丁": ["卯", "酉"],
    "戊": ["辰", "戌", "丑", "未"], "己": ["辰", "戌", "丑", "未"],
    "庚": ["寅", "亥"], "辛": ["寅", "亥"],
    "壬": ["巳", "申"], "癸": ["巳", "申"]
}


# 文昌貴人對照表
wenchang_gui_ren = {
    "甲": "巳", "乙": "午", "丙": "申", "丁": "酉",
    "戊": "申", "己": "酉", "庚": "亥", "辛": "子",
    "壬": "寅", "癸": "卯"
}

# 福星貴人對照表（修正後）
fuxing_gui_ren = {
    "甲": ["寅", "子"], "丙": ["寅", "子"],
    "乙": ["卯", "丑"], "癸": ["卯", "丑"],
    "戊": ["申"], "己": ["未"], "丁": ["亥"],
    "庚": ["午"], "辛": ["巳"], "壬": ["辰"]
}

# 月德貴人對照表（修正後）
yuede_gui_ren = {
    "寅": "丙", "午": "丙", "戌": "丙",
    "申": "壬", "子": "壬", "辰": "壬",
    "亥": "甲", "卯": "甲", "未": "甲",
    "巳": "庚", "酉": "庚", "丑": "庚"
}

# 天德貴人對照表
tiande_gui_ren = {
    "寅": "丁", "卯": "申", "辰": "壬", "巳": "辛",
    "午": "亥", "未": "甲", "申": "癸", "酉": "寅",
    "戌": "丙", "亥": "乙", "子": "己", "丑": "庚"
}


# 沖關係對照表
chong_relationships = [
    ("子", "午"), ("丑", "未"), ("寅", "申"), ("卯", "酉"), ("辰", "戌"), ("巳", "亥")
]

# 刑關係對照表
xing_relationships = [
    ("寅", "巳"), ("巳", "申"), ("申", "寅"),  # 寅巳申互刑
    ("丑", "戌"), ("戌", "未"), ("未", "丑"),  # 丑未戌互刑
    ("子", "卯"),  # 子卯相刑
    ("辰", "辰"), ("午", "午"), ("酉", "酉"), ("亥", "亥")  # 自刑
]

# 害關係對照表
hai_relationships = [
    ("子", "未"), ("丑", "午"), ("寅", "巳"), ("卯", "辰"), ("申", "亥"), ("酉", "戌")
]

# 破關係對照表
po_relationships = {
    "子": "酉", "午": "卯", "辰": "丑", "未": "戌",
    "寅": "亥", "申": "巳"
}

# 三合局對照表
sanhe_groups = [
    {"寅", "午", "戌"},
    {"巳", "酉", "丑"},
    {"申", "子", "辰"},
    {"亥", "卯", "未"}
]    


# 三會局對照表
sanhui_groups = [
    {"亥", "子", "丑"},
    {"寅", "卯", "辰"},
    {"巳", "午", "未"},
    {"申", "酉", "戌"}
]

# 天干合對照表
tiangan_he_table = {
    ("甲", "己"): "土", ("乙", "庚"): "金", ("丙", "辛"): "水", ("丁", "壬"): "木", ("戊", "癸"): "火"
}

# 地支六合對照表（並標示合化的五行）
dizhi_hehua_table = {
    ("子", "丑"): "土", ("寅", "亥"): "木", ("卯", "戌"): "火", ("辰", "酉"): "金",
    ("巳", "申"): "水", ("午", "未"): "土"
}

# 桃花星對照表（紅鸞、天喜、咸池）
hongluan_taohua = {
    "子": "卯", "丑": "寅", "寅": "丑", "卯": "子", "辰": "亥", "巳": "戌",
    "午": "酉", "未": "申", "申": "未", "酉": "午", "戌": "巳", "亥": "辰"
}

tianxi_taohua = {
    "子": "酉", "丑": "申", "寅": "未", "卯": "午", "辰": "巳", "巳": "辰",
    "午": "卯", "未": "寅", "申": "丑", "酉": "子", "戌": "亥", "亥": "戌"
}

xianchi_taohua = {
    "子": "酉", "丑": "午", "寅": "卯", "卯": "子", "辰": "酉", "巳": "午",
    "午": "卯", "未": "子", "申": "酉", "酉": "午", "戌": "卯", "亥": "子"
}

# 紅艷桃花對照表
hongyan_taohua = {
    "甲": "午", "乙": "申", "丙": "寅", "丁": "未", "戊": "辰",
    "己": "辰", "庚": "戌", "辛": "酉", "壬": "子", "癸": "申"
}

# 沐浴桃花對照表
muyu_taohua = {
    "甲": "子", "乙": "巳", "丙": "卯", "丁": "申", "戊": "卯",
    "己": "申", "庚": "午", "辛": "亥", "壬": "酉", "癸": "寅"
}

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


def calculate_da_yun_info(birth_datetime: datetime, gender: str, ri_gan: str):
    """
    計算八字大運的起運時間與方向與完整大運表
    """
    yang_gan = {'甲', '丙', '戊', '巧', '壬'}
    is_yang = ri_gan in yang_gan

    if (gender == '男' and is_yang) or (gender == '女' and not is_yang):
        direction = '順行'
        step = 1
    else:
        direction = '逆行'
        step = -1

    # 取得起始日物件
    day = sxtwl.fromSolar(birth_datetime.year, birth_datetime.month, birth_datetime.day)

    # 開始尋找最近的節氣
    while True:
        day = day.after(step)
        if day.hasJieQi():
            jieqi_index = day.getJieQi()
            jd = day.getJieQiJD()
            t = sxtwl.JD2DD(jd)

            # 將 sxtwl.Time 格式手動轉換為 datetime（避免 float 問題）
            jieqi_datetime = datetime(t.Y, t.M, t.D, int(t.h), int(t.m), int(round(t.s)))

            days_diff = (jieqi_datetime - birth_datetime).total_seconds() / 86400
            qi_yun_age = abs(days_diff) / 3

            # 開始年份
            start_year = birth_datetime.year + int(qi_yun_age)

            # 十天干與十二地支表
            tiangan = ['甲','乙','丙','丁','戊','己','巧','辛','壬','癸']
            dizhi = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥']

            # 找出月干支作為起點
            month_gz = day.getMonthGZ()
            tg_index = month_gz.tg
            dz_index = month_gz.dz

            # 大運表生成
            da_yun_schedule = []
            for i in range(10):
                offset = (i + 1) * step  # 第一柱從下一個干支開始
                tg = tiangan[(tg_index + offset) % 10]
                dz = dizhi[(dz_index + offset) % 12]
                age = int(qi_yun_age) + i * 10 + 1  # 虛歲起運
                year = start_year + i * 10
                da_yun_schedule.append(f"{age}歲 ({year}) - {tg}{dz}")

            return {
                '大運方向': direction,
                '節氣時間': jieqi_datetime,
                '距離出生天數': round(days_diff, 2),
                '起運年齡（歲）': round(qi_yun_age, 1),
                '大運': da_yun_schedule
            }


def count_tian_yi_gui_ren(bazi):
    day_gan = bazi["日柱"][0]  # 日干
    year_gan = bazi["年柱"][0]  # 年干
    
    # 獲取對應的天乙貴人地支
    day_gui_ren = set(tian_yi_gui_ren.get(day_gan, []))
    year_gui_ren = set(tian_yi_gui_ren.get(year_gan, []))
    
    # 檢查八字中的地支是否匹配天乙貴人
    count = 0
    matches = []
    for pillar, value in bazi.items():
        if pillar == "公曆":
            continue
        zhi = value[1]  # 取地支
        pillar_label = pillar[0]  # 取「年、月、日、時」
        if zhi in day_gui_ren:
            count += 1
            matches.append(f"日干 {day_gan} - {pillar_label}支 {zhi}")
        if zhi in year_gui_ren:
            count += 1
            matches.append(f"年干 {year_gan} - {pillar_label}支 {zhi}")
    
    return count, matches

def count_taiji_gui_ren(bazi):
    day_gan = bazi["日柱"][0]  # 日干
    year_gan = bazi["年柱"][0]  # 年干
    taiji_zhi_day = taiji_gui_ren.get(day_gan, [])
    taiji_zhi_year = taiji_gui_ren.get(year_gan, [])
    
    count = 0
    matches = []
    for pillar, value in bazi.items():
        if pillar == "公曆":
            continue
        zhi = value[1]  # 取地支
        pillar_label = pillar[0]  # 取「年、月、日、時」
        if zhi in taiji_zhi_day:
            count += 1
            matches.append(f"日干 {day_gan} - {pillar_label}支 {zhi}")
        if zhi in taiji_zhi_year:
            count += 1
            matches.append(f"年干 {year_gan} - {pillar_label}支 {zhi}")
    
    return count, matches

def count_wenchang_gui_ren(bazi):
    day_gan = bazi["日柱"][0]  # 日干
    wenchang_zhi = wenchang_gui_ren.get(day_gan, "")
    
    count = 0
    matches = []
    for pillar, value in bazi.items():
        if pillar == "公曆":
            continue
        zhi = value[1]  # 取地支
        pillar_label = pillar[0]  # 取「年、月、日、時」
        if zhi == wenchang_zhi:
            count += 1
            matches.append(f"日干 {day_gan} - {pillar_label}支 {zhi}")
    
    return count, matches

def count_fuxing_gui_ren(bazi):
    day_gan = bazi["日柱"][0]  # 日干
    year_gan = bazi["年柱"][0]  # 年干
    fuxing_zhi_day = fuxing_gui_ren.get(day_gan, [])
    fuxing_zhi_year = fuxing_gui_ren.get(year_gan, [])
    
    count = 0
    matches = []
    for pillar, value in bazi.items():
        if pillar == "公曆":
            continue
        zhi = value[1]  # 取地支
        pillar_label = pillar[0]  # 取「年、月、日、時」
        if zhi in fuxing_zhi_day:
            count += 1
            matches.append(f"日干 {day_gan} - {pillar_label}支 {zhi}")
        if zhi in fuxing_zhi_year:
            count += 1
            matches.append(f"年干 {year_gan} - {pillar_label}支 {zhi}")
    
    return count, matches


def count_yuede_gui_ren(bazi):
    month_zhi = bazi["月柱"][1]  # 月支
    yuede_gan = yuede_gui_ren.get(month_zhi, "")
    
    count = 0
    matches = []
    for pillar, value in bazi.items():
        if pillar == "公曆":
            continue
        gan = value[0]  # 取天干
        pillar_label = pillar[0]  # 取「年、月、日、時」
        if gan == yuede_gan:
            count += 1
            matches.append(f"{pillar_label}干 {gan} - 月支 {month_zhi}")
    
    return count, matches

def count_tiande_gui_ren(bazi):
    month_zhi = bazi["月柱"][1]  # 月支
    tiande_gan = tiande_gui_ren.get(month_zhi, "")
    
    count = 0
    matches = []
    for pillar, value in bazi.items():
        if pillar == "公曆":
            continue
        gan = value[0]  # 取天干
        pillar_label = pillar[0]  # 取「年、月、日、時」
        if gan == tiande_gan:
            count += 1
            matches.append(f"{pillar_label}干 {gan} - 月支 {month_zhi}")
    
    return count, matches

def count_xing_relationships(bazi):
    zhi_list = [bazi["年柱"][1], bazi["月柱"][1], bazi["日柱"][1], bazi["時柱"][1]]
    count = 0
    matches = []
    
    for i in range(len(zhi_list)):
        for j in range(i + 1, len(zhi_list)):
            pair = (zhi_list[i], zhi_list[j])
            reverse_pair = (zhi_list[j], zhi_list[i])
            if pair in xing_relationships or reverse_pair in xing_relationships:
                count += 1
                matches.append(f"{zhi_list[i]} 刑 {zhi_list[j]}")
    
    return count, matches

def count_chong_relationships(bazi):
    zhi_list = [bazi["年柱"][1], bazi["月柱"][1], bazi["日柱"][1], bazi["時柱"][1]]
    count = 0
    matches = []
    
    for i in range(len(zhi_list)):
        for j in range(i + 1, len(zhi_list)):
            pair = (zhi_list[i], zhi_list[j])
            reverse_pair = (zhi_list[j], zhi_list[i])
            if pair in chong_relationships or reverse_pair in chong_relationships:
                count += 1
                matches.append(f"{zhi_list[i]} 沖 {zhi_list[j]}")
    
    return count, matches

def count_hai_relationships(bazi):
    zhi_list = [bazi["年柱"][1], bazi["月柱"][1], bazi["日柱"][1], bazi["時柱"][1]]
    count = 0
    matches = []
    
    for i in range(len(zhi_list)):
        for j in range(i + 1, len(zhi_list)):
            pair = (zhi_list[i], zhi_list[j])
            reverse_pair = (zhi_list[j], zhi_list[i])
            if pair in hai_relationships or reverse_pair in hai_relationships:
                count += 1
                matches.append(f"{zhi_list[i]} 害 {zhi_list[j]}")
    
    return count, matches

def count_po_relationships(bazi):
    pillars = [bazi["年柱"][1], bazi["月柱"][1], bazi["日柱"][1], bazi["時柱"][1]]
    count = 0
    matches = []
    
    for i in range(len(pillars)):
        for j in range(i + 1, len(pillars)):
            if po_relationships.get(pillars[i]) == pillars[j] or po_relationships.get(pillars[j]) == pillars[i]:
                count += 1
                matches.append(f"{pillars[i]} - {pillars[j]}")
    
    return count, matches


def count_sanhe(bazi):
    zhi_list = {bazi["年柱"][1], bazi["月柱"][1], bazi["日柱"][1], bazi["時柱"][1]}
    matches = []
    for group in sanhe_groups:
        if group.issubset(zhi_list):
            matches.append(", ".join(group))
    return len(matches), matches

def count_sanhui(bazi):
    zhi_list = {bazi["年柱"][1], bazi["月柱"][1], bazi["日柱"][1], bazi["時柱"][1]}
    matches = []
    for group in sanhui_groups:
        if group.issubset(zhi_list):
            matches.append(", ".join(group))
    return len(matches), matches

def count_hongluan_taohua(bazi):
    year_zhi = bazi["年柱"][1]  # 年支
    hongluan_zhi = hongluan_taohua.get(year_zhi, "")
    
    count = 0
    matches = []
    for pillar, value in bazi.items():
        if pillar == "公曆":
            continue
        zhi = value[1]  # 取地支
        pillar_label = pillar[0]  # 取「年、月、日、時」
        if zhi == hongluan_zhi:
            count += 1
            matches.append(f"年支 {year_zhi} - {pillar_label}支 {zhi}")
    
    return count, matches

def count_tianxi_taohua(bazi):
    year_zhi = bazi["年柱"][1]  # 年支
    tianxi_zhi = tianxi_taohua.get(year_zhi, "")
    
    count = 0
    matches = []
    for pillar, value in bazi.items():
        if pillar == "公曆":
            continue
        zhi = value[1]  # 取地支
        pillar_label = pillar[0]  # 取「年、月、日、時」
        if zhi == tianxi_zhi:
            count += 1
            matches.append(f"年支 {year_zhi} - {pillar_label}支 {zhi}")
    
    return count, matches

def count_xianchi_taohua(bazi):
    year_zhi = bazi["年柱"][1]  # 年支
    xianchi_zhi = xianchi_taohua.get(year_zhi, "")
    
    count = 0
    matches = []
    for pillar, value in bazi.items():
        if pillar == "公曆":
            continue
        zhi = value[1]  # 取地支
        pillar_label = pillar[0]  # 取「年、月、日、時」
        if zhi == xianchi_zhi:
            count += 1
            matches.append(f"年支 {year_zhi} - {pillar_label}支 {zhi}")
    
    return count, matches

def count_hongyan_taohua(bazi):
    day_gan = bazi["日柱"][0]  # 日干
    hongyan_zhi = hongyan_taohua.get(day_gan, "")
    
    count = 0
    matches = []
    for pillar, value in bazi.items():
        if pillar == "公曆":
            continue
        zhi = value[1]  # 取地支
        pillar_label = pillar[0]  # 取「年、月、日、時」
        if zhi == hongyan_zhi:
            count += 1
            matches.append(f"日干 {day_gan} - {pillar_label}支 {zhi}")
    
    return count, matches

def count_muyu_taohua(bazi):
    day_gan = bazi["日柱"][0]  # 日干
    muyu_zhi = muyu_taohua.get(day_gan, "")
    
    count = 0
    matches = []
    for pillar, value in bazi.items():
        if pillar == "公曆":
            continue
        zhi = value[1]  # 取地支
        pillar_label = pillar[0]  # 取「年、月、日、時」
        if zhi == muyu_zhi:
            count += 1
            matches.append(f"日干 {day_gan} - {pillar_label}支 {zhi}")
    
    return count, matches

def check_tonggen(bazi):
    tonggen_results = {}
    tiangan_list = {"年": bazi["年柱"][0], "月": bazi["月柱"][0], "日": bazi["日柱"][0], "時": bazi["時柱"][0]}
    dizhi_list = {"年": bazi["年柱"][1], "月": bazi["月柱"][1], "日": bazi["日柱"][1], "時": bazi["時柱"][1]}
    
    for label, tg in tiangan_list.items():
        matching_branches = []
        for dz_label, dz in dizhi_list.items():
            if tg in zang_gan_table[dz]:
                matching_branches.append(f"{dz_label}支 {dz}")
        if matching_branches:
            tonggen_results[f"{label}干 {tg}"] = matching_branches
    
    return tonggen_results

def count_tiangan_he(bazi):
    tiangan_list = [bazi["年柱"][0], bazi["月柱"][0], bazi["日柱"][0], bazi["時柱"][0]]
    he_count = 0
    he_combinations = []
    
    for i in range(len(tiangan_list)):
        for j in range(i + 1, len(tiangan_list)):
            pair = tuple(sorted([tiangan_list[i], tiangan_list[j]]))
            if pair in tiangan_he_table:
                he_count += 1
                he_combinations.append(f"{pair[0]}合{pair[1]}化{tiangan_he_table[pair]}")
    
    return he_count, he_combinations


def count_dizhi_hehua(bazi):
    dizhi = [bazi["年柱"][1], bazi["月柱"][1], bazi["日柱"][1], bazi["時柱"][1]]
    he_count = 0
    combinations = []
    for i in range(len(dizhi)):
        for j in range(i + 1, len(dizhi)):
            pair = tuple(sorted([dizhi[i], dizhi[j]]))
            if pair in dizhi_hehua_table:
                he_count += 1
                combinations.append(f"{pair[0]}合{pair[1]}化{dizhi_hehua_table[pair]}")
    return he_count, combinations


def check_de_lu(bazi):
    de_lu_results = {}
    tiangan_list = {"年": bazi["年柱"][0], "月": bazi["月柱"][0], "日": bazi["日柱"][0], "時": bazi["時柱"][0]}
    dizhi_list = {"年": bazi["年柱"][1], "月": bazi["月柱"][1], "日": bazi["日柱"][1], "時": bazi["時柱"][1]}
    
    for label, tg in tiangan_list.items():
        if tg in de_lu_table and de_lu_table[tg] in dizhi_list.values():
            de_lu_results[f"{label}干 {tg}"] = f"得祿於 {de_lu_table[tg]}"
    
    return de_lu_results


# --- Streamlit Interface ---
st.title("八字命盤分析器")

st.markdown("""
<style>
/* Prevent Streamlit columns from stacking */
.bazi-row {
    display: flex !important;
    flex-direction: row !important;
    justify-content: space-evenly;
    flex-wrap: nowrap !important;
    overflow-x: auto;
    gap: 10px;
    margin-bottom: 1rem;
}
.bazi-cell {
    text-align: center;
    min-width: 80px;
}
</style>
""", unsafe_allow_html=True)


st.markdown("請輸入您的出生時間：")

# 👇 User inputs
birth_year = st.number_input("年份", min_value=1900, max_value=2100, value=1969)
birth_month = st.number_input("月份", min_value=1, max_value=12, value=3)
birth_day = st.number_input("日期", min_value=1, max_value=31, value=1)
birth_hour = st.number_input("時辰（24小時制）", min_value=0, max_value=23, value=10)
gender = st.selectbox("請選擇性別：", ["男", "女"])


if st.button("分析八字"):
    try:
        bazi = get_bazi(birth_year, birth_month, birth_day, birth_hour)
        st.markdown("### 八字命盤")
        st.markdown(f"**公曆出生時間：** {bazi['公曆']}")

        labels = ["時柱", "日柱", "月柱", "年柱"]
        day_gan = bazi["日柱"][0]

        # Row 1: Label row
        st.markdown("<div class='bazi-row'>" + "".join([
            f"<div class='bazi-cell' style='font-weight:bold; font-size:16px'>{label[0]}</div>"
            for label in labels
        ]) + "</div>", unsafe_allow_html=True)

        # Row 2: Ten Gods (天干十神)
        st.markdown("<div class='bazi-row'>" + "".join([
            f"<div class='bazi-cell' style='font-size:18px; color:gray'>{'元' if label == '日柱' else shishen_table[day_gan][bazi[label][0]]}</div>"
            for label in labels
        ]) + "</div>", unsafe_allow_html=True)

        # Row 3: 干支 characters
        st.markdown("<div class='bazi-row'>" + "".join([
            f"<div class='bazi-cell' style='font-size:32px; font-weight:bold'>{bazi[label][0]}<br>{bazi[label][1]}</div>"
            for label in labels
        ]) + "</div>", unsafe_allow_html=True)

        # Row 4: 地支十神
        st.markdown("<div class='bazi-row'>" + "".join([
            f"<div class='bazi-cell' style='font-size:18px; color:gray'>{dizhi_shishen_table[day_gan][bazi[label][1]]}</div>"
            for label in labels
        ]) + "</div>", unsafe_allow_html=True)

        
        birth_datetime = datetime.strptime(birth_str.split()[0] + " " + birth_str.split()[1], "%Y-%m-%d %H:%M")
        ri_gan = bazi['日柱'][0]
        da_yun_list = calculate_da_yun_info(birth_datetime, gender, ri_gan)
        st.markdown("---")
        st.markdown("### 大運十柱")
        for line in da_yun_list:
            st.markdown(f"- {line}")
        
        def show_section(title, count, matches, color=None):
            if color:
                st.markdown(f"<h3 style='color:{color}'>{title} 數量: {count}</h3>", unsafe_allow_html=True)
            else:
                st.markdown(f"### {title} 數量: {count}")

            if matches:
                for m in matches:
                    if color:
                        st.markdown(f"<span style='color:{color}'>- {m}</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"- {m}")
            else:
                if color:
                    st.markdown(f"<span style='color:{color}'>無對應</span>", unsafe_allow_html=True)
                else:
                    st.markdown("無對應")

        # 🔵 Section 1: 合化、通根、得祿
        show_section("天干合化", *count_tiangan_he(bazi), color="#004488")
        show_section("地支合化", *count_dizhi_hehua(bazi), color="#004488")

        st.markdown("### <span style='color:#004488'>天干通根</span>", unsafe_allow_html=True)
        for tg, matches in check_tonggen(bazi).items():
            st.markdown(f"<span style='color:#004488'>- {tg} 通根於: {', '.join(matches)}</span>", unsafe_allow_html=True)

        st.markdown("### <span style='color:#004488'>天干得祿</span>", unsafe_allow_html=True)
        for tg, result in check_de_lu(bazi).items():
            st.markdown(f"<span style='color:#004488'>- {tg} {result}</span>", unsafe_allow_html=True)

        # 🟢 Section 2: 三合局、三會局
        show_section("三合局", *count_sanhe(bazi), color="#336600")
        show_section("三會局", *count_sanhui(bazi), color="#336600")

        # 🟠 Section 3: 貴人
        for title, func in [
            ("天乙貴人", count_tian_yi_gui_ren),
            ("太極貴人", count_taiji_gui_ren),
            ("文昌貴人", count_wenchang_gui_ren),
            ("福星貴人", count_fuxing_gui_ren),
            ("月德貴人", count_yuede_gui_ren),
            ("天德貴人", count_tiande_gui_ren),
        ]:
            show_section(title, *func(bazi), color="#cc5500")

        # 💗 Section 4: 沖、刑、害、破
        for title, func in [
            ("沖關係", count_chong_relationships),
            ("刑關係", count_xing_relationships),
            ("害關係", count_hai_relationships),
            ("破關係", count_po_relationships),
        ]:
            show_section(title, *func(bazi), color="#990066")

        # ⚪ Section 5: 桃花
        for title, func in [
            ("紅鸞桃花", count_hongluan_taohua),
            ("天喜桃花", count_tianxi_taohua),
            ("咸池桃花", count_xianchi_taohua),
            ("紅艷桃花", count_hongyan_taohua),
            ("沐浴桃花", count_muyu_taohua),
        ]:
            show_section(title, *func(bazi), color="#444444")
    
    except Exception as e:
        st.error(f"發生錯誤：{e}")
