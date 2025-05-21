import requests
from datetime import datetime,timedelta
import json
import seaborn as sns
import matplotlib.pyplot as plt
import os
import configparser
from collections import defaultdict

# 取得目前檔案所在的資料夾
current_dir = os.path.dirname(os.path.abspath(__file__))

# 找到 env.ini 的完整路徑
ini_path = os.path.join(current_dir, '..', 'env.ini')

# 建立 configparser 實例
config = configparser.ConfigParser()

# 讀取 env.ini
config.read(ini_path, encoding="utf-8")

Authorization = config['Key']['Authorization']

# 替換為您的 API 金鑰
API_KEY = Authorization

Base_url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-093'

# 建立字典
Country_dict = {
    "宜蘭縣3": "01",
    # "宜蘭縣1": "03",
    "桃園市3": "05",
    # "桃園市1": "07",
    "新竹縣3": "09",
    # "新竹縣1": "11",
    "苗栗縣3": "13",
    # "苗栗縣1": "15",
    "彰化縣3": "17",
    # "彰化縣1": "19",
    "南投縣3": "21",
    # "南投縣1": "23",
    "雲林縣3": "25",
    # "雲林縣1": "27",
    "嘉義縣3": "29",
    # "嘉義縣1": "31",
    "屏東縣3": "33",
    # "屏東縣1": "35",
    "臺東縣3": "37",
    # "臺東縣1": "39",
    "花蓮縣3": "41",
    # "花蓮縣1": "43",
    "澎湖縣3": "45",
    # "澎湖縣1": "47",
    "基隆市3": "49",
    # "基隆市1": "51",
    "新竹市3": "53",
    # "新竹市1": "55",
    "嘉義市3": "57",
    # "嘉義市1": "59",
    "臺北市3": "61",
    # "臺北市1": "63",
    "高雄市3": "65",
    # "高雄市1": "67",
    "新北市3": "69",
    # "新北市1": "71",
    "臺中市3": "73",
    # "臺中市1": "75",
    "臺南市3": "77",
    # "臺南市1": "79",
    "連江縣3": "81",
    # "連江縣1": "83", 
    "金門縣3": "85",
    # "金門縣1": "87",
    "臺灣3": "89",
    # "臺灣1": "91"
}

def get_weather(city,district):
    locationId = city + "3" 

    Country_val = ""
    # 查詢並輸出對應的值
    if locationId in Country_dict:
        Country_val = Country_dict[locationId]
    else:
        print("找不到對應的值")

    # API 端點
    url = "F-D0047-0" + Country_val

    #各縣市所對應鄉鎮名稱
    LocationName = district
    
    ComfortIndex_To_Emoji = {   
        "A": "🥶",   #非常寒冷：須注意保暖
        "B": "❄️",   #寒冷：穿著冬季衣物才舒適
        "C": "🌬️",  #涼爽：需穿著長袖衣物
        "D": "😊",   #舒適：人體感受最為宜人
        "E": "😓",   #稍感悶熱：適合穿著輕便衣物
        "F": "🔥",   #炎熱：容易出汗，應注意補水
        "G": "🥵",   #非常悶熱：戶外活動應謹慎
        "H": "☀️🚫", #極度酷熱：易中暑，須避免外出
    }
    
    WindDirection_To_Emoji = {  
        "北風":"⬇️",
        "南風":"⬆️",
        "東風":"⬅️",
        "西風":"➡️",
        "東北風":"↙️",
        "西北風":"↘️",
        "東南風":"↖️",
        "西南風":"↗️",
        "旋轉風":"🌀",
    }
    
    WeatherCode_To_Emoji = {
        "01": "☀️",          #晴天
        "02": "🌤️",         #晴時多雲
        "03": "🌤️🌥️",      #多雲時晴
        "04": "☁️",          #多雲
        "05": "🌥️",         #多雲時陰
        "06": "🌥️",         #陰時多雲
        "07": "☁️",          #陰天
        "08": "🌦️",         #多雲陣雨
        "09": "🌦️⏱",        #多雲短暫雨
        "10": "🌦️⏱",        #多雲短暫陣雨
        "11": "⛈️",          #多雲有雷陣雨
        "12": "🌧️",         #多雲有雨
        "13": "🌧️⏱",        #多雲有陣雨
        "14": "⛈️",          #多雲有雷雨
        "15": "⛈️⏱",         #多雲有雷陣雨
        "16": "🌫️",         #多雲有霧
        "17": "🌫️🌧️",      #多雲有霧有雨
        "18": "🌫️🌧️⏱",     #多雲有霧有陣雨
        "19": "🌫️⛈️",       #多雲有霧有雷陣雨
        "20": "☁️",          #陰天
        "21": "☁️🌧️",       #陰天有雨
        "22": "☁️🌧️⏱",      #陰天有陣雨
        "23": "☁️⛈️",        #陰天有雷雨
        "24": "☁️⛈️⏱",       #陰天有雷陣雨
        "25": "☁️🌫️",       #陰天有霧
        "26": "☁️🌫️🌧️",    #陰天有霧有雨
        "27": "☁️🌫️🌧️⏱",   #陰天有霧有陣雨
        "28": "☁️🌫️⛈️",     #陰天有霧有雷陣雨
        "29": "☁️🌧️📍",     #多雲局部雨
        "30": "☁️🌧️⏱📍",    #多雲局部陣雨
        "31": "☁️🌫️🌧️📍",  #多雲有霧有局部雨
        "32": "☁️🌫️🌧️⏱📍", #多雲有霧有局部陣雨
        "33": "☁️",          #陰天（重複定義）
        "34": "☁️🌧️",       #陰天有雨
        "35": "☁️🌧️⏱",      #陰天有陣雨
        "36": "☁️⛈️",        #陰天有雷雨
        "37": "☁️🌫️",       #陰天有霧
        "38": "🌧️🌫️",      #有雨有霧
        "39": "🌧️⏱🌫️🌅",   #短暫雨晨霧
        "41": "🌧️⏱⛈️⏱🌫️",  #短暫雨雷雨霧
        "42": "❄️",          #雪
    }


    # 設定參數
    params = {
    'Authorization': API_KEY,
    'locationId'   : url,
    'LocationName' : LocationName,
    'format'       : 'JSON',
    'timeFrom'     : datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    'timeTo'       : (datetime.now()+ timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%S"),
    }

    # 發送 GET 請求
    ThreeDayWeatherResponse = requests.get(Base_url, params=params)

    result = ""
    # 檢查回應狀態
    if ThreeDayWeatherResponse.status_code == 200:
        data = ThreeDayWeatherResponse.json()
        Locations = data['records']['Locations']
        for Location in Locations:      
            # result += f"{Location['DatasetDescription']}:\n"
            # result += f"{Location['LocationsName']}"
            for location in Location['Location']:
                # result += f"{location['LocationName']}:\n"
                
                # 整理資料：以日期為主分類
                grouped_data = defaultdict(lambda: {"instant": defaultdict(list), "range": defaultdict(list)})

                for element in location["WeatherElement"]:
                    name = element["ElementName"]
                    for t in element["Time"]:
                        if "DataTime" in t:
                            dt = datetime.fromisoformat(t["DataTime"])
                            date = dt.strftime("%Y-%m-%d")
                            time = dt.strftime("%H")
                            
                            value = t["ElementValue"][0]
                            if name == "溫度":
                                grouped_data[date]["instant"][time].append(f"{value['Temperature']}°C /")
                            # elif name == "露點溫度":
                            #     grouped_data[date]["instant"][time].append(f"露點溫度{value['DewPoint']}")
                            # elif name == "相對濕度":
                            #     grouped_data[date]["instant"][time].append(f"相對濕度{value['RelativeHumidity']}")
                            elif name == "體感溫度":
                                grouped_data[date]["instant"][time].append(f"{value['ApparentTemperature']}°C /")
                            elif name == "舒適度指數":
                                ComfortIndex = ''
                                if(int(value['ComfortIndex']) < 11 ):
                                    ComfortIndex = ComfortIndex_To_Emoji.get("A")
                                elif(int(value['ComfortIndex']) < 16):
                                    ComfortIndex = ComfortIndex_To_Emoji.get("B")
                                elif(int(value['ComfortIndex']) < 21):
                                    ComfortIndex = ComfortIndex_To_Emoji.get("C")
                                elif(int(value['ComfortIndex']) < 26):
                                    ComfortIndex = ComfortIndex_To_Emoji.get("D")
                                elif(int(value['ComfortIndex']) < 31):
                                    ComfortIndex = ComfortIndex_To_Emoji.get("E")
                                elif(int(value['ComfortIndex']) < 36):
                                    ComfortIndex = ComfortIndex_To_Emoji.get("F")
                                elif(int(value['ComfortIndex']) < 41):
                                    ComfortIndex = ComfortIndex_To_Emoji.get("G")
                                else:
                                    ComfortIndex = ComfortIndex_To_Emoji.get("H")
                                grouped_data[date]["instant"][time].append(f"    {ComfortIndex}    /")
                            # elif name == "風速":
                            #     grouped_data[date]["instant"][time].append(f"風速{value['WindSpeed']}{value['BeaufortScale']}")
                            elif name == "風向":
                                grouped_data[date]["instant"][time].append(f"  {WindDirection_To_Emoji.get(value['WindDirection'].replace("偏",""))}")
                        else:
                            start    = datetime.fromisoformat(t["StartTime"]).strftime("%H")
                            end      = datetime.fromisoformat(t["EndTime"]).strftime("%H")
                            date     = datetime.fromisoformat(t["StartTime"]).strftime("%Y-%m-%d")
                            time_key = f"{start}~{end}"

                            value = t["ElementValue"][0]
                            if name == "天氣現象":
                                 grouped_data[date]["range"][time_key].append(f"{WeatherCode_To_Emoji.get(value['WeatherCode'])}")
                            elif name == "3小時降雨機率":
                                 grouped_data[date]["range"][time_key].append(f"{value['ProbabilityOfPrecipitation']}%")
                            # elif name == "天氣預報綜合描述":
                            #      grouped_data[date]["range"][time_key].append(f"天氣預報綜合描述 {value['WeatherDescription']}") 
                result += f"      🕗    氣溫  / 體感  / 舒適度 / 風向\n"      
                for date, data in grouped_data.items():  
                    result += f"{date}:\n"   
                    for time, values in data["instant"].items():
                        result += f"     {time}時: {' '.join(values)}\n"
                                                
                result += f"\n\n"
                        
                result += f"🌧️ 降雨機率與天氣\n"           
                for date, data in grouped_data.items():  
                    result += f"{date}:\n"
                    for time, values in data["range"].items():
                        result += f"    {time}時: {' '.join(values)}\n"
                    
                return result if result else "查無天氣資料"

    else:
        print(f"請求失敗，狀態碼：{ThreeDayWeatherResponse.status_code}")