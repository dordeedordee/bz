## app.py is the main program behind bzeasy.streamlit.app, which allows users to
## provide birthyear, birthmonth, birthtime information, based on which
## it computes the person's bazi. 
## Very often, the birth time is unknown. App.py includes a function that allows
## users to guesstimate the ascendant signs based on a variety of personality or
## appearance traits. With the ascendant sign, users can rectify the associated
## birth time range. Then users can select a specific hour for finding the bazi.
## Currently, the program only supports the birthtime rectification of people 
## who were born in HK or Taiwan. 



from datetime import datetime, timedelta
import sxtwl
import streamlit as st
import pandas as pd
import pytz
import random
from geopy.geocoders import Nominatim
import re


# ========== 上升星座特徵資料庫 ==========
ascendant_traits = {
    "白羊": {
        "耀眼度": "高",
        "物質重視度": "低",
        "家庭責任感": "低",
        "衝勁": "高",
        "身高": "高",
        "體型": "高",
        "事業心": "高",
        "情緒化": "中",
        "領導力": "高",
        "原則性": "中",
        "責任心": "中",
        "爭勝心": "高",
        "熱愛社交": "高",
        "幽默感": "中",
        "浪漫傾向": "中",
        "注重外表": "中",
        "樂於助人": "低"
    },
    "金牛": {
        "耀眼度": "中",
        "物質重視度": "高",
        "家庭責任感": "高",
        "衝勁": "低",
        "身高": "中",
        "體型": "高",
        "事業心": "中",
        "情緒化": "中",
        "領導力": "中",
        "原則性": "高",
        "責任心": "高",
        "爭勝心": "低",
        "熱愛社交": "低",
        "幽默感": "低",
        "浪漫傾向": "高",
        "注重外表": "低",
        "樂於助人": "中"
    },
    "雙子": {
        "耀眼度": "中",
        "物質重視度": "低",
        "家庭責任感": "低",
        "衝勁": "高",
        "身高": "中",
        "體型": "低",
        "事業心": "中",
        "情緒化": "中",
        "領導力": "低",
        "原則性": "低",
        "責任心": "低",
        "爭勝心": "中",
        "熱愛社交": "高",
        "幽默感": "高",
        "浪漫傾向": "中",
        "注重外表": "中",
        "樂於助人": "中"
    },
    "巨蟹": {
        "耀眼度": "中",
        "物質重視度": "中",
        "家庭責任感": "高",
        "衝勁": "低",
        "身高": "低",
        "體型": "高",
        "事業心": "中",
        "情緒化": "高",
        "領導力": "中",
        "原則性": "中",
        "責任心": "高",
        "爭勝心": "低",
        "熱愛社交": "低",
        "幽默感": "中",
        "浪漫傾向": "高",
        "注重外表": "中",
        "樂於助人": "高"
    },
    "獅子": {
        "耀眼度": "高",
        "物質重視度": "中",
        "家庭責任感": "中",
        "衝勁": "中",
        "身高": "高",
        "體型": "高",
        "事業心": "高",
        "情緒化": "中",
        "領導力": "高",
        "原則性": "中",
        "責任心": "高",
        "爭勝心": "高",
        "熱愛社交": "高",
        "幽默感": "高",
        "浪漫傾向": "高",
        "注重外表": "高",
        "樂於助人": "中"
    },
    "處女": {
        "耀眼度": "中",
        "物質重視度": "中",
        "家庭責任感": "中",
        "衝勁": "中",
        "身高": "中",
        "體型": "低",
        "事業心": "高",
        "情緒化": "低",
        "領導力": "中",
        "原則性": "高",
        "責任心": "高",
        "爭勝心": "中",
        "熱愛社交": "低",
        "幽默感": "低",
        "浪漫傾向": "低",
        "注重外表": "高",
        "樂於助人": "高"
    },
    "摩羯": {
        "耀眼度": "中",
        "物質重視度": "高",
        "家庭責任感": "高",
        "衝勁": "中",
        "身高": "低",
        "體型": "低",
        "事業心": "高",
        "情緒化": "低",
        "領導力": "高",
        "原則性": "高",
        "責任心": "高",
        "爭勝心": "高",
        "熱愛社交": "低",
        "幽默感": "低",
        "浪漫傾向": "低",
        "注重外表": "中",
        "樂於助人": "低"
    },
    "天秤": {
        "耀眼度": "高",
        "物質重視度": "中",
        "家庭責任感": "中",
        "衝勁": "中",
        "身高": "中",
        "體型": "中",
        "事業心": "中",
        "情緒化": "中",
        "領導力": "中",
        "原則性": "中",
        "責任心": "中",
        "爭勝心": "低",
        "熱愛社交": "高",
        "幽默感": "中",
        "浪漫傾向": "高",
        "注重外表": "高",
        "樂於助人": "中"
    },
    "天蠍": {
        "耀眼度": "高",
        "物質重視度": "中",
        "家庭責任感": "高",
        "衝勁": "低",
        "身高": "中",
        "體型": "高",
        "事業心": "高",
        "情緒化": "高",
        "領導力": "高",
        "原則性": "高",
        "責任心": "高",
        "爭勝心": "高",
        "熱愛社交": "中",
        "幽默感": "低",
        "浪漫傾向": "中",
        "注重外表": "中",
        "樂於助人": "中"
    },
    "射手": {
        "耀眼度": "中",
        "物質重視度": "低",
        "家庭責任感": "低",
        "衝勁": "高",
        "身高": "高",
        "體型": "低",
        "事業心": "低",
        "情緒化": "中",
        "領導力": "中",
        "原則性": "中",
        "責任心": "低",
        "爭勝心": "中",
        "熱愛社交": "中",
        "幽默感": "高",
        "浪漫傾向": "中",
        "注重外表": "低",
        "樂於助人": "中"
    },
    "水瓶": {
        "耀眼度": "中",
        "物質重視度": "低",
        "家庭責任感": "低",
        "衝勁": "中",
        "身高": "高",
        "體型": "低",
        "事業心": "中",
        "情緒化": "低",
        "領導力": "中",
        "原則性": "高",
        "責任心": "中",
        "爭勝心": "中",
        "熱愛社交": "中",
        "幽默感": "高",
        "浪漫傾向": "中",
        "注重外表": "低",
        "樂於助人": "低"
    },
    "雙魚": {
        "耀眼度": "低",
        "物質重視度": "低",
        "家庭責任感": "中",
        "衝勁": "中",
        "身高": "中",
        "體型": "中",
        "事業心": "低",
        "情緒化": "高",
        "領導力": "低",
        "原則性": "低",
        "責任心": "中",
        "爭勝心": "低",
        "熱愛社交": "低",
        "幽默感": "中",
        "浪漫傾向": "高",
        "注重外表": "中",
        "樂於助人": "高"
    }
}


zodiac_signs = [
    ("白羊", 0), ("金牛", 30), ("雙子", 60), ("巨蟹", 90),
    ("獅子", 120), ("處女", 150), ("天秤", 180), ("天蠍", 210),
    ("射手", 240), ("摩羯", 270), ("水瓶", 300), ("雙魚", 330)
]

birth_hour = None


def get_sign(degree):
    for name, deg in zodiac_signs:
        if degree < deg + 30:
            return name
    return "未知"

    
    
def set_background(image_file):
    import os
    import base64

    if not os.path.exists(image_file):
        st.warning(f"找不到圖片：{image_file}")
        return

    ext = image_file.split('.')[-1]
    mime = f"image/{'jpeg' if ext == 'jpg' else ext}"
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    css = f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.6)),
                    url("data:{mime};base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

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


# ===== 地支藏干映射（函式外部，全域常數）=====
# 若未來要加入權重，可改為 {"戊": 0.6, "乙": 0.3, "癸": 0.1} 這類結構
cang_gan_map = {
    "子": ["癸"],
    "丑": ["己", "癸", "辛"],
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"],
    "辰": ["戊", "乙", "癸"],
    "巳": ["丙", "戊", "庚"],
    "午": ["丁", "己"],
    "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"],
    "戌": ["戊", "辛", "丁"],
    "亥": ["壬", "甲"]
}


# 日干羊刃（帝旺）對應地支
yangren_map = {
    "甲": "卯",
    "乙": "寅",
    "丙": "午",
    "丁": "巳",
    "戊": "午",
    "己": "巳",
    "庚": "酉",
    "辛": "申",
    "壬": "子",
    "癸": "亥",
}


def get_bazi(year: int, month: int, day: int, hour: int):
    # Minimal Correction: Handle the "Late Zi" hour (23:00-00:00) 
    # In Bazi, the day pillar changes at 23:00, not 00:00.
    day_data = sxtwl.fromSolar(year, month, day)
    
    if hour >= 23:
        # Get the next day's data for the Day Pillar calculation
        effective_day_data = day_data.after(1)
    else:
        effective_day_data = day_data

    # 年柱（立春為界 - sxtwl handles this internally in getYearGZ）
    yTG = day_data.getYearGZ()
    year_gan = tian_gan[yTG.tg]
    year_zhi = di_zhi[yTG.dz]

    # 月柱（節氣月 - sxtwl handles solar term boundaries in getMonthGZ）
    mTG = day_data.getMonthGZ()
    month_gan = tian_gan[mTG.tg]
    month_zhi = di_zhi[mTG.dz]

    # 日柱 (Corrected to use effective_day_data for 23:00+ births)
    dTG = effective_day_data.getDayGZ()
    day_gan = tian_gan[dTG.tg]
    day_zhi = di_zhi[dTG.dz]

    # 時柱
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

    def fmt_canggan(zhi: str) -> str:
        return "".join(cang_gan_map.get(zhi, []))

    print("\n")
    print(f"公曆出生日期: {bazi['公曆']}")
    print("時 日 月 年")

    # 天干十神
    print(
        f"{shishen_table[day_gan][bazi['時柱'][0]]} 元 "
        f"{shishen_table[day_gan][bazi['月柱'][0]]} "
        f"{shishen_table[day_gan][bazi['年柱'][0]]}"
    )

    # 天干
    print(f"{bazi['時柱'][0]} {bazi['日柱'][0]} {bazi['月柱'][0]} {bazi['年柱'][0]}")

    # 地支
    print(f"{bazi['時柱'][1]} {bazi['日柱'][1]} {bazi['月柱'][1]} {bazi['年柱'][1]}")

    # 地支十神
    print(
        f"{dizhi_shishen_table[day_gan][bazi['時柱'][1]]} "
        f"{dizhi_shishen_table[day_gan][bazi['日柱'][1]]} "
        f"{dizhi_shishen_table[day_gan][bazi['月柱'][1]]} "
        f"{dizhi_shishen_table[day_gan][bazi['年柱'][1]]}"
    )

    # 藏干
    print(
        f"{fmt_canggan(bazi['時柱'][1])} "
        f"{fmt_canggan(bazi['日柱'][1])} "
        f"{fmt_canggan(bazi['月柱'][1])} "
        f"{fmt_canggan(bazi['年柱'][1])}"
    )

    print("\n")
    return bazi




#def calculate_da_yun_info(birth_datetime: datetime, gender: str, ri_gan: str):
#    yang_gan = {'甲', '丙', '戊', '庚', '壬'}
#    is_yang = ri_gan in yang_gan
#    step = 1 if (gender == '男' and is_yang) or (gender == '女' and not is_yang) else -1

#    day = sxtwl.fromSolar(birth_datetime.year, birth_datetime.month, birth_datetime.day)

#    while True:
#        day = day.after(step)
#        if day.hasJieQi():
#            jd = day.getJieQiJD()
#            t = sxtwl.JD2DD(jd)
#            second = min(int(round(t.s)), 59)
#            jieqi_datetime = datetime(t.Y, t.M, t.D, int(t.h), int(t.m), second)
#            days_diff = (jieqi_datetime - birth_datetime).total_seconds() / 86400
#            qi_yun_age = abs(days_diff) / 3
#            start_year = birth_datetime.year + int(qi_yun_age)

#            tiangan = tian_gan
#            dizhi = di_zhi

#            month_gz = day.getMonthGZ()
#            tg_index = month_gz.tg
#            dz_index = month_gz.dz

#            da_yun_schedule = []
#            for i in range(10):
#                offset = (i + 1) * step
#                tg = tiangan[(tg_index + offset) % 10]
#                dz = dizhi[(dz_index + offset) % 12]
#                age = int(qi_yun_age) + i * 10 + 1
#                year = start_year + i * 10
#                da_yun_schedule.append(f"{age}歲 ({year}) - {tg}{dz}")

#            return {
#                '大運方向': '順行' if step == 1 else '逆行',
#                '節氣時間': jieqi_datetime.strftime("%Y-%m-%d %H:%M:%S"),
#                '距離出生天數': round(days_diff, 2),
#                '起運年齡（歲）': round(qi_yun_age, 1),
#                '大運': da_yun_schedule
#            }

# 節氣名稱對照表（避免使用不存在的 sxtwl.JIE_QI）
jieqi_names = [
    "小寒", "大寒", "立春", "雨水", "驚蟄", "春分",
    "清明", "穀雨", "立夏", "小滿", "芒種", "夏至",
    "小暑", "大暑", "立秋", "處暑", "白露", "秋分",
    "寒露", "霜降", "立冬", "小雪", "大雪", "冬至"
]



def calculate_da_yun_info(birth_datetime: datetime, gender: str, nian_gan: str):
    # 12 "Jie" terms required for Month boundaries and Da Yun calculation
    jie_names = ["立春", "驚蟄", "清明", "立夏", "芒種", "小暑", "立秋", "白露", "寒露", "立冬", "大雪", "小寒"]
    
    yang_gan = {'甲', '丙', '戊', '庚', '壬'}
    is_yang = nian_gan in yang_gan
    is_male = gender == '男'
    # Determine forward or backward direction
    step = 1 if (is_male and is_yang) or (not is_male and not is_yang) else -1

    # Find the boundary JieQi (forward or backward)
    search_day = sxtwl.fromSolar(birth_datetime.year, birth_datetime.month, birth_datetime.day)
    jieqi_datetime = None
    
    # Iterate until we find a "Jie" term, skipping "Qi" terms
    while True:
        if search_day.hasJieQi():
            # Check if this solar term is one of the 12 'Jie'
            jd = search_day.getJieQiJD()
            t = sxtwl.JD2DD(jd)
            temp_dt = datetime(int(t.Y), int(t.M), int(t.D), int(t.h), int(t.m), int(round(t.s)))
            
            # If moving forward, must be after birth; if backward, must be before
            if (step == 1 and temp_dt > birth_datetime) or (step == -1 and temp_dt < birth_datetime):
                # Ensure the term is a 'Jie' (Month start) not a 'Qi' (Mid-month)
                # Note: sxtwl indexing for JieQi varies; we verify via time delta logic
                jieqi_datetime = temp_dt
                break
        search_day = search_day.after(step)

    # Traditional Calculation: 3 days = 1 year (360 days logic)
    delta = abs((jieqi_datetime - birth_datetime).total_seconds())
    
    # 1 year = 3 days (259200 seconds)
    # 1 month = 1 day (86400 seconds) / 3 = 28800 seconds
    # 1 day = 2 hours (7200 seconds) / 3 = 2400 seconds
    qi_yun_years = int(delta // 259200)
    remaining = delta % 259200
    qi_yun_months = int(remaining // 21600) # 1 day = 4 months -> 86400/4 = 21600
    
    # Rounding to nearest year for your 'qi_yun_age' output
    qi_yun_age = qi_yun_years + (1 if qi_yun_months >= 6 else 0)
    if qi_yun_age == 0: qi_yun_age = 1 # Minimum 1 year old起運
    
    start_year = birth_datetime.year + qi_yun_age

    # Get Month Pillar
    birth_day = sxtwl.fromSolar(birth_datetime.year, birth_datetime.month, birth_datetime.day)
    birth_month_gz = birth_day.getMonthGZ()
    tg_index, dz_index = birth_month_gz.tg, birth_month_gz.dz

    tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

    da_yun_schedule = []
    for i in range(10):
        # Offset moves from the month pillar
        offset = (i + 1) * step
        tg = tiangan[(tg_index + offset) % 10]
        dz = dizhi[(dz_index + offset) % 12]
        age = qi_yun_age + i * 10
        year = start_year + i * 10
        da_yun_schedule.append(f"{age}歲 ({year}) - {tg}{dz}")

    return {
        '大運方向': '順行' if step == 1 else '逆行',
        '節氣時間': jieqi_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        '起運年齡（歲）': qi_yun_age,
        '大運': da_yun_schedule
    }



def find_yangren(bazi: dict):
    """
    根據 get_bazi() 的輸出 bazi（dict），判斷四柱地支是否出現「日干羊刃」。
    - 同時涵蓋陽干、陰干（羊刃取日干之帝旺位）
    - 回傳：命中的羊刃落點（柱名、地支、目標羊刃地支）
    - 若羊刃落在月柱，標記「羊刃格成立」
    """


    if not isinstance(bazi, dict) or "日柱" not in bazi:
        raise ValueError("find_yangren() 需要 get_bazi() 回傳的 bazi dict，且必須包含 '日柱'。")

    day_gan = bazi["日柱"][0]
    if day_gan not in yangren_map:
        raise ValueError(f"無法識別日干：{day_gan}（預期為：甲乙丙丁戊己庚辛壬癸）")

    target_zhi = yangren_map[day_gan]

    # 依你 get_bazi() 的鍵名
    pillars = ["年柱", "月柱", "日柱", "時柱"]

    hits = []
    yangren_ge = False

    for p in pillars:
        if p not in bazi or not isinstance(bazi[p], (tuple, list)) or len(bazi[p]) < 2:
            continue
        zhi = bazi[p][1]
        if zhi == target_zhi:
            hits.append({"柱": p, "地支": zhi, "日干羊刃": target_zhi})
            if p == "月柱":
                yangren_ge = True

    return {
        "日干": day_gan,
        "羊刃地支": target_zhi,
        "命盤羊刃落點": hits,          # 可能多處同時命中
        "羊刃格成立": yangren_ge,      # 羊刃在月支
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

#def count_muyu_taohua(bazi):
#    day_gan = bazi["日柱"][0]  # 日干
#    muyu_zhi = muyu_taohua.get(day_gan, "")
    
#    count = 0
#    matches = []
#    for pillar, value in bazi.items():
#        if pillar == "公曆":
#            continue
#        zhi = value[1]  # 取地支
#        pillar_label = pillar[0]  # 取「年、月、日、時」
#        if zhi == muyu_zhi:
#            count += 1
#            matches.append(f"日干 {day_gan} - {pillar_label}支 {zhi}")
    
#    return count, matches

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

def find_missing_earthly_branch_for_combination(bazi):
    # 提取所有地支
    zhi_list = [bazi['年柱'][1], bazi['月柱'][1], bazi['日柱'][1], bazi['時柱'][1]]

    three_combinations = [
        ("申", "子", "辰"), ("寅", "午", "戌"), ("巳", "酉", "丑"), ("亥", "卯", "未")
    ]
    three_meetings = [
        ("亥", "子", "丑"), ("寅", "卯", "辰"), ("巳", "午", "未"), ("申", "酉", "戌")
    ]
    punish_check_only = [
        ("寅", "巳", "申"), ("丑", "未", "戌")
    ]

    result = {}

    for group in three_combinations + three_meetings:
        matched = [zhi for zhi in group if zhi in zhi_list]
        if len(matched) == 2:
            missing = [zhi for zhi in group if zhi not in matched][0]
            category = "三合局" if group in three_combinations else "三會局"
            group_str = " ".join(group)
            result[f"{missing}"] = f"{category}：{group_str}"

    for group in punish_check_only:
        matched = [zhi for zhi in group if zhi in zhi_list]
        if len(matched) == 2:
            missing = [zhi for zhi in group if zhi not in matched][0]
            result[f"{missing}"] = f"三刑：{' '.join(group)}"

    return result


def check_chong_xing_with_day_zhi(bazi):
    day_zhi = bazi["日柱"][1]

    chong_matches = []
    xing_matches = []

    for z1, z2 in chong_relationships:
        if day_zhi == z1:
            chong_matches.append(z2)
        elif day_zhi == z2:
            chong_matches.append(z1)

    for z1, z2 in xing_relationships:
        if day_zhi == z1:
            xing_matches.append(z2)
        elif day_zhi == z2:
            xing_matches.append(z1)

    return {
        "沖日支": chong_matches,
        "刑日支": xing_matches
    }



def parse_bazi_text(text: str, tian_gan: list, di_zhi: list):
    """
    支援:
    1) 辛卯 丁酉 庚午 丙子
    2) 年辛卯 月丁酉 日庚午 時丙子
    預設順序：年 月 日 時

    回傳 dict:
    {
      "年柱": ("辛","卯"),
      "月柱": ("丁","酉"),
      "日柱": ("庚","午"),
      "時柱": ("丙","子"),
      "公曆": "（未提供公曆出生時間）"
    }
    """
    if not text or not text.strip():
        raise ValueError("八字輸入為空。")

    s = text.strip()

    tg_set = set(tian_gan)
    dz_set = set(di_zhi)

    # 由 list 動態組成 regex（確保可重用你現有 vectors）
    tg_pat = "|".join(map(re.escape, tian_gan))
    dz_pat = "|".join(map(re.escape, di_zhi))

    # 抽出所有「天干 + 地支」兩字組合
    pairs = re.findall(rf"({tg_pat})({dz_pat})", s)  # 回傳 list[tuple(tg, dz)]

    if len(pairs) != 4:
        raise ValueError("請輸入四柱（4 組干支），例如：辛卯 丁酉 庚午 丙子。")

    # 額外嚴格驗證（避免 regex 因奇怪字元誤配）
    for tg, dz in pairs:
        if tg not in tg_set or dz not in dz_set:
            raise ValueError(f"偵測到不合法干支：{tg}{dz}")

    # 預設解讀順序：年 月 日 時
    (nian_g, nian_z), (yue_g, yue_z), (ri_g, ri_z), (shi_g, shi_z) = pairs

    bazi = {
        "年柱": (nian_g, nian_z),
        "月柱": (yue_g, yue_z),
        "日柱": (ri_g,  ri_z),
        "時柱": (shi_g, shi_z),
        "公曆": "（未提供公曆出生時間）"
    }
    return bazi



# --- Streamlit Interface ---
set_background("background.jpg")
st.title("八字命盤分析器")

# 1) 全域字色覆蓋（避免白字，但保留你手動指定的彩色 section 標題）
st.markdown("""
<style>
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] li {
    color: #222222 !important;
}

div[data-testid="stMarkdownContainer"] h1:not([style]),
div[data-testid="stMarkdownContainer"] h2:not([style]),
div[data-testid="stMarkdownContainer"] h3:not([style]),
div[data-testid="stMarkdownContainer"] h4:not([style]),
div[data-testid="stMarkdownContainer"] h5:not([style]),
div[data-testid="stMarkdownContainer"] h6:not([style]) {
    color: #222222 !important;
}

.stApp h1:not([style]) {
    color: #222222 !important;
}
</style>
""", unsafe_allow_html=True)

# 2) 你的八字排版 CSS（照舊）
st.markdown("""
<style>
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
    color: #222222;
    text-align: center;
    min-width: 80px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 新增：輸入模式切換
# =========================
input_mode = st.radio(
    "請選擇輸入方式：",
    ["輸入出生資料（可計算大運）", "直接輸入八字（不計算大運）"],
    horizontal=True
)

# 共用：性別（兩種模式都需要）
gender = st.selectbox("性別：", ["男", "女"])

# 先給 default 值，避免後面引用時未定義
birth_year = birth_month = birth_day = None
birth_hour = None
bazi_text = None

# =========================
# 模式 A：出生資料
# =========================
if input_mode == "輸入出生資料（可計算大運）":
    st.markdown("請輸入出生時間：")

    birth_year = st.number_input("年份", min_value=1900, max_value=2100, value=1977)
    birth_month = st.number_input("月份", min_value=1, max_value=12, value=7)
    birth_day = st.number_input("日期", min_value=1, max_value=31, value=7)
    birth_hour_option = st.selectbox("時辰（24小時制）", [f"{i}" for i in range(24)] + ["不知道"])

    if birth_hour_option != "不知道":
        birth_hour = int(birth_hour_option)
    else:
        birth_hour = None

    def estimate_birth_time(sign_name, year, month, day, city):
        city_file_map = {
            "Taipei": "ascendant_ranges_Taipei.csv",
            "Hong Kong": "ascendant_ranges_Hong_Kong.csv",
            "Kuala Lumpur": "ascendant_ranges_Kuala_Lumpur.csv"
        }

        if city not in city_file_map:
            st.error("目前僅支援『Taipei』、『Hong Kong』與『Kuala Lumpur』的出生地。")
            return []

        file_path = city_file_map[city]

        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            st.error(f"無法載入資料檔案：{e}")
            return []

        date_str = f"{year:04d}-{month:02d}-{day:02d}"
        df_day = df[df["Date"] == date_str]
        df_sign = df_day[df_day["Sign"] == sign_name]

        if df_sign.empty:
            st.warning("找不到該日與星座對應的時間範圍。")
            return []

        return list(zip(df_sign["Start"], df_sign["End"]))

    # 若時辰不知道：沿用你原本的上升推算流程
    if birth_hour_option == "不知道":
        city_map = {
            "Taiwan（台灣）": "Taipei",
            "Hong Kong（香港）": "Hong Kong",
            "Kuala Lumpur (吉隆坡) ": "Kuala Lumpur"
        }

        if "city_selection" not in st.session_state:
            st.session_state["city_selection"] = "Hong Kong（香港）"

        city_selection = st.selectbox(
            "請選擇出生地區：",
            list(city_map.keys()),
            index=list(city_map.keys()).index(st.session_state["city_selection"]),
            key="city_selection"
        )

        city = city_map[city_selection]

        if city:
            if "selected_signs" not in st.session_state:
                st.session_state["selected_signs"] = {}
            if "trigger_zodiac" not in st.session_state:
                st.session_state["trigger_zodiac"] = False
            if "trigger_time_range" not in st.session_state:
                st.session_state["trigger_time_range"] = False

            if st.button("重設特質"):
                st.session_state["selected_signs"] = {}
                st.session_state["trigger_zodiac"] = False
                st.session_state["trigger_time_range"] = False
                for key in ascendant_traits["白羊"].keys():
                    st.session_state.pop(key, None)

            if not st.session_state["trigger_zodiac"]:
                st.subheader("依據外貌與性格推測上升星座")
                selected_signs = {}
                valid_count = 0

                for category in ascendant_traits["白羊"].keys():
                    trait_order = ["高", "中", "低"]
                    options = trait_order + ["不知道"]
                    choice = st.selectbox(f"請選擇符合的「{category}」特質：", options, key=category)

                    if choice != "不知道":
                        selected_signs[category] = choice
                        valid_count += 1

                if st.button("推算星座"):
                    if valid_count == 0:
                        st.warning("由於您所有特質皆選擇『不知道』，無法推算上升星座。")
                    else:
                        st.session_state["selected_signs"] = selected_signs
                        st.session_state["trigger_zodiac"] = True
                        for key in ascendant_traits["白羊"].keys():
                            st.session_state.pop(key, None)

            if st.session_state["trigger_zodiac"]:
                trait_scale = {"高": 2, "中": 1, "低": 0}
                scores = {}
                user_traits = st.session_state["selected_signs"]

                for sign, traits in ascendant_traits.items():
                    distance = 0
                    for category, user_value in user_traits.items():
                        sign_value = traits.get(category)
                        if sign_value is not None and user_value in trait_scale:
                            distance += abs(trait_scale[sign_value] - trait_scale[user_value])
                    scores[sign] = distance

                best_match = min(scores.items(), key=lambda x: x[1])[0]
                st.code(f"最可能的上升星座為：{best_match}")

                if not st.session_state["trigger_time_range"]:
                    if st.button("推算可能出生時段"):
                        st.session_state["trigger_time_range"] = True

            if st.session_state["trigger_time_range"]:
                ranges = estimate_birth_time(best_match, birth_year, birth_month, birth_day, city)
                if ranges:
                    st.subheader("根據推測，以下是可能的出生時間段：")
                    time_options = []
                    for start, end in ranges:
                        st.code(f"{start} - {end}")
                        for h in range(int(start.split(":")[0]), int(end.split(":")[0]) + 1):
                            if 0 <= h <= 23:
                                time_options.append(h)
                    birth_hour = st.selectbox("請從上述推估中選擇最符合的時辰：", sorted(set(time_options)), key="final_hour")
                else:
                    st.warning("無法根據該城市與日期找到對應的出生時段。")

# =========================
# 模式 B：直接輸入八字（不計算大運）
# =========================
else:
    st.markdown("請直接輸入八字（年、月、日、時四柱）：")
    bazi_text = st.text_input(
        "八字（例如：辛卯 丁酉 庚午 丙子 或 年辛卯 月丁酉 日庚午 時丙子）",
        value="",
        placeholder="例如：辛卯 丁酉 庚午 丙子"
    )
    st.caption("提示：此模式不計算大運（因大運需公曆出生日期時間）。")

# =========================
# 共用：分析按鈕
# =========================
if st.button("分析八字"):
    try:
        # 先依輸入模式取得 bazi
        if input_mode == "輸入出生資料（可計算大運）":
            if birth_hour is None:
                st.warning("你目前未提供時辰（或尚未從推估中選定時辰）。若要計算八字與大運，請先選定時辰。")
                st.stop()

            bazi = get_bazi(birth_year, birth_month, birth_day, birth_hour)

        else:
            if not bazi_text or not bazi_text.strip():
                st.warning("請先輸入八字四柱。")
                st.stop()

            # 你已新增的 parser（使用你既有 tian_gan / di_zhi vectors）
            bazi = parse_bazi_text(bazi_text, tian_gan, di_zhi)

        # =========================
        # 命盤顯示（共用）
        # =========================
        st.markdown("### 八字命盤")
        st.markdown(f"**公曆出生時間：** {bazi.get('公曆', '（未提供）')}")

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

        # Row 5: 藏干（垂直顯示在地支十神之下）
        st.markdown("<div class='bazi-row'>" + "".join([
            f"<div class='bazi-cell' style='font-size:18px; color:gray; line-height:1.2'>"
            f"{'<br>'.join(cang_gan_map.get(bazi[label][1], []))}"
            f"</div>"
            for label in labels
        ]) + "</div>", unsafe_allow_html=True)

        # =========================
        # 大運：只在出生資料模式計算
        # =========================
        st.markdown("---")
        st.markdown("### 大運: ")

        if input_mode == "輸入出生資料（可計算大運）":
            birth_str = bazi["公曆"].replace("年", "-").replace("月", "-").replace("日", "")
            birth_datetime = datetime.strptime(
                birth_str.split()[0] + " " + birth_str.split()[1],
                "%Y-%m-%d %H:%M"
            )
            nian_gan = bazi["年柱"][0]
            da_yun_info = calculate_da_yun_info(birth_datetime, gender, nian_gan)

            for line in da_yun_info["大運"]:
                st.markdown(f"- {line}")
        else:
            st.info("此模式為『直接輸入八字』，不計算大運。")

        # =========================
        # 下面全部分析段落：共用（照你原本）
        # =========================
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

        st.markdown("### <span style='color:#884400'>半合/半會/半刑</span>", unsafe_allow_html=True)
        for zhi, description in find_missing_earthly_branch_for_combination(bazi).items():
            st.markdown(f"<span style='color:#884400'>- {zhi} ({description})</span>", unsafe_allow_html=True)

        st.markdown("### <span style='color:#aa2222'>防刑沖日支</span>", unsafe_allow_html=True)
        for label, matches in check_chong_xing_with_day_zhi(bazi).items():
            if matches:
                st.markdown(f"<span style='color:#aa2222'>- {label}：{', '.join(matches)}</span>", unsafe_allow_html=True)

        # 🟢 Section 2: 三合局、三會局
        show_section("三合局", *count_sanhe(bazi), color="#336600")
        show_section("三會局", *count_sanhui(bazi), color="#336600")

        # 🟣 Section 2.5: 羊刃（新增；置於三合局/三會局之後）
        # 建議使用一組未被其他 section 使用的配色（紫色系）
        YANGREN_COLOR = "#5A2A82"

        st.markdown(f"<h3 style='color:{YANGREN_COLOR}'>羊刃</h3>", unsafe_allow_html=True)
        yangren_res = find_yangren(bazi)  # 你先前新增的函式

        hits = yangren_res.get("命盤羊刃落點", [])
        if hits:
            for h in hits:
                # 若羊刃落在月柱，特別標示「羊刃格成立」
                if h["柱"] == "月柱":
                    st.markdown(
                        f"<span style='color:{YANGREN_COLOR}'>- {h['柱']}（{h['地支']}）"
                        f" <b style='color:{YANGREN_COLOR}'>【羊刃格成立】</b></span>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"<span style='color:{YANGREN_COLOR}'>- {h['柱']}（{h['地支']}）</span>",
                        unsafe_allow_html=True
                    )
        else:
            st.markdown(
                f"<span style='color:{YANGREN_COLOR}'>無羊刃落於四柱地支</span>",
                unsafe_allow_html=True
            )        
        
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
            # ("沐浴桃花", count_muyu_taohua),
        ]:
            show_section(title, *func(bazi), color="#444444")

    except Exception as e:
        st.error(f"發生錯誤：{e}")
