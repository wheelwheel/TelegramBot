import requests
from datetime import datetime
import json
import seaborn as sns
import matplotlib.pyplot as plt
import os
import configparser

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
    "宜蘭縣1": "03",
    "桃園市3": "05",
    "桃園市1": "07",
    "新竹縣3": "09",
    "新竹縣1": "11",
    "苗栗縣3": "13",
    "苗栗縣1": "15",
    "彰化縣3": "17",
    "彰化縣1": "19",
    "南投縣3": "21",
    "南投縣1": "23",
    "雲林縣3": "25",
    "雲林縣1": "27",
    "嘉義縣3": "29",
    "嘉義縣1": "31",
    "屏東縣3": "33",
    "屏東縣1": "35",
    "臺東縣3": "37",
    "臺東縣1": "39",
    "花蓮縣3": "41",
    "花蓮縣1": "43",
    "澎湖縣3": "45",
    "澎湖縣1": "47",
    "基隆市3": "49",
    "基隆市1": "51",
    "新竹市3": "53",
    "新竹市1": "55",
    "嘉義市3": "57",
    "嘉義市1": "59",
    "臺北市3": "61",
    "臺北市1": "63",
    "高雄市3": "65",
    "高雄市1": "67",
    "新北市3": "69",
    "新北市1": "71",
    "臺中市3": "73",
    "臺中市1": "75",
    "臺南市3": "77",
    "臺南市1": "79",
    "連江縣3": "81",
    "連江縣1": "83",
    "金門縣3": "85",
    "金門縣1": "87",
    "臺灣3": "89",
    "臺灣1": "91"
}

def get_weather(city,district):
    # 讓使用者輸入 key
    
    locationId = city + "3"

    Country_val = ""
    # 查詢並輸出對應的值
    if locationId in Country_dict:
        Country_val = Country_dict[locationId]
    else:
        print("找不到對應的值")
        exit()

    # API 端點
    url = "F-D0047-0" + Country_val

    #各縣市所對應鄉鎮名稱
    LocationName = district

#     #天氣預報天氣因子
#     ElementName = district

#     Element_dict = {
#     "A":"溫度",
#     "B":"露點溫度",
#     "C":"相對濕度",
#     "D":"體感溫度",
#     "E":"舒適度指數",
#     "F":"風速",
#     "G":"風向",
#     "H":"3小時降雨機率",
#     "I":"天氣現象",
#     "J":"天氣預報綜合描述",
# }

#     # 查詢並輸出對應的值
#     if ElementName in Element_dict:
#         ElementName = Country_dict[ElementName]
#     else:
#         ElementName = ""


    # 設定參數
    params = {
    'Authorization': API_KEY,
    'locationId'   : url,
    'LocationName' : LocationName,
    # 'ElementName'  : ElementName,
    'format'       : 'JSON',
    # 'timeFrom'     : '2025-05-14T00:00:00',
    # 'timeTo'       : '2025-05-16T00:00:00',
}

    # 發送 GET 請求
    ThreeDayWeatherResponse = requests.get(Base_url, params=params)

    result = ""
    # 檢查回應狀態
    if ThreeDayWeatherResponse.status_code == 200:
        data = ThreeDayWeatherResponse.json()
        Locations = data['records']['Locations']
        for Location in Locations:      
          result += f"{Location['DatasetDescription']}:\n"
          result += f"{Location['LocationsName']}"
          for location in Location['Location']:
            result += f"{location['LocationName']}:\n"
            WeatherElement = location['WeatherElement']
            for WeatherElement in WeatherElement:
              if WeatherElement['ElementName'] == '溫度':
                溫度時間_list = []
                溫度_list = []

                # result +='溫度:'
                for time in WeatherElement['Time']:
                #   if(int(datetime.fromisoformat(time['DataTime']).strftime("%H")) % 3 == 0):
                    # 溫度時間_list.append(datetime.fromisoformat(time['DataTime']).strftime("%d %H:%M"))
                    # 溫度_list.append(time['ElementValue'][0]['Temperature'])
                # sns.lineplot(x=溫度時間_list, y=溫度_list, marker='o')
                # plt.title(f"Temp")
                # plt.show()
                # 畫折線圖
                # plt.plot(溫度時間_list, 溫度_list, marker='o')
                # plt.title("Temperature")
                # plt.xlabel("Time")
                # plt.ylabel("Temperature")
                # plt.grid(True)
                # plt.show()
                    result +=f"    日期:{datetime.fromisoformat(time['DataTime']).strftime("%Y-%m-%d   %H:%M")},溫度:{time['ElementValue'][0]['Temperature']}°C\n"
            return result if result else "查無天氣資料"

        else:
            print(f"請求失敗，狀態碼：{ThreeDayWeatherResponse.status_code}")
    

