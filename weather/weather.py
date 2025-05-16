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
    "宜縣3": "01",
    "宜縣1": "03",
    "桃市3": "05",
    "桃市1": "07",
    "竹縣3": "09",
    "竹縣1": "11",
    "苗縣3": "13",
    "苗縣1": "15",
    "彰縣3": "17",
    "彰縣1": "19",
    "投縣3": "21",
    "投縣1": "23",
    "雲縣3": "25",
    "雲縣1": "27",
    "嘉縣3": "29",
    "嘉縣1": "31",
    "屏縣3": "33",
    "屏縣1": "35",
    "東縣3": "37",
    "東縣1": "39",
    "花縣3": "41",
    "花縣1": "43",
    "澎縣3": "45",
    "澎縣1": "47",
    "基市3": "49",
    "基市1": "51",
    "竹市3": "53",
    "竹市1": "55",
    "嘉市3": "57",
    "嘉市1": "59",
    "北市3": "61",
    "北市1": "63",
    "高市3": "65",
    "高市1": "67",
    "新市3": "69",
    "新市1": "71",
    "中市3": "73",
    "中市1": "75",
    "南市3": "77",
    "南市1": "79",
    "連縣3": "81",
    "連縣1": "83",
    "金縣3": "85",
    "金縣1": "87",
    "臺3": "89",
    "臺1": "91"
}

# 讓使用者輸入 key
locationId = input("縣市天氣:")

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
LocationName = input("縣市:")

#天氣預報天氣因子
ElementName = input("""\n
A:溫度\n
B:露點溫度\n
C:相對濕度\n
D:體感溫度\n
E:舒適度指數\n
F:風速\n
G:風向\n
H:3小時降雨機率\n
I:天氣現象\n
J:天氣預報綜合描述\n
""")

Element_dict = {
    "A":"溫度",
    "B":"露點溫度",
    "C":"相對濕度",
    "D":"體感溫度",
    "E":"舒適度指數",
    "F":"風速",
    "G":"風向",
    "H":"3小時降雨機率",
    "I":"天氣現象",
    "J":"天氣預報綜合描述",
}

# 查詢並輸出對應的值
if ElementName in Element_dict:
    ElementName = Country_dict[ElementName]
else:
    ElementName = ""


# 設定參數
params = {
    'Authorization': API_KEY,
    'locationId'   : url,
    'LocationName' : LocationName,
    'ElementName'  : ElementName,
    'format'       : 'JSON',
    # 'timeFrom'     : '2025-05-14T00:00:00',
    # 'timeTo'       : '2025-05-16T00:00:00',
}

# 發送 GET 請求
ThreeDayWeatherResponse = requests.get(Base_url, params=params)

# 檢查回應狀態
if ThreeDayWeatherResponse.status_code == 200:
    data = ThreeDayWeatherResponse.json()
    Locations = data['records']['Locations']
    for Location in Locations:      
      print(f"{Location['DatasetDescription']}:")
      print(f"{Location['LocationsName']}:") 
      for location in Location['Location']:
        print(f"{location['LocationName']}:")
        WeatherElement = location['WeatherElement']
        for WeatherElement in WeatherElement:
          
          
          if WeatherElement['ElementName'] == '溫度':
            溫度時間_list = []
            溫度_list = []
            
            print('溫度:')
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
                print(f"    日期:{datetime.fromisoformat(time['DataTime']).strftime("%Y-%m-%d %H:%M")},溫度:{time['ElementValue'][0]['Temperature']}°C")
          
          # if WeatherElement['ElementName'] == '露點溫度':
          #   print('露點溫度:')
          #   for time in WeatherElement['Time']:
          #     if(int(datetime.fromisoformat(time['DataTime']).strftime("%H")) % 3 == 0):
          #       print(f"    日期:{datetime.fromisoformat(time['DataTime']).strftime("%Y-%m-%d %H:%M")},溫度:{time['ElementValue'][0]['DewPoint']}°C")
          
          
          # if WeatherElement['ElementName'] == '相對濕度':
          #   print('相對濕度:')
          #   for time in WeatherElement['Time']:
          #     if(int(datetime.fromisoformat(time['DataTime']).strftime("%H")) % 3 == 0):
          #       print(f"    日期:{datetime.fromisoformat(time['DataTime']).strftime("%Y-%m-%d %H:%M")},比率:{time['ElementValue'][0]['RelativeHumidity']}%")
                
          
          # if WeatherElement['ElementName'] == '體感溫度':
          #   print('體感溫度:')
          #   for time in WeatherElement['Time']:
          #     print(f"    日期:{datetime.fromisoformat(time['DataTime']).strftime("%Y-%m-%d %H:%M")},體感溫度:{time['ElementValue'][0]['ApparentTemperature']}°C")
          

          # if WeatherElement['ElementName'] == '舒適度指數':
          #   print('舒適度指數:')
          #   for time in WeatherElement['Time']:
          #     print(f"    日期:{datetime.fromisoformat(time['DataTime']).strftime("%Y-%m-%d %H:%M")},舒適度:{time['ElementValue'][0]['ComfortIndexDescription']}")
          
          
          # if WeatherElement['ElementName'] == '風速':
          #   print('風速:')
          #   for time in WeatherElement['Time']:
          #     print(f"    日期:{datetime.fromisoformat(time['DataTime']).strftime("%Y-%m-%d %H:%M")},風速:{time['ElementValue'][0]['WindSpeed']},風力:{time['ElementValue'][0]['BeaufortScale']}")
              
              
          # if WeatherElement['ElementName'] == '風向':
          #   print('風向:')
          #   for time in WeatherElement['Time']:
          #     print(f"    日期:{datetime.fromisoformat(time['DataTime']).strftime("%Y-%m-%d %H:%M")},風向:{time['ElementValue'][0]['WindDirection']}")

          
          # if WeatherElement['ElementName'] == '3小時降雨機率':
          #   print('3小時降雨機率:')
          #   for time in WeatherElement['Time']:
          #     print(f"    {datetime.fromisoformat(time['StartTime']).strftime("%Y-%m-%d %H:%M")}~{datetime.fromisoformat(time['EndTime']).strftime("%Y-%m-%d %H:%M")},機率:{time['ElementValue'][0]['ProbabilityOfPrecipitation']}%")
          
          
          # if WeatherElement['ElementName'] == '天氣現象':
          #   print('天氣現象:')
          #   for time in WeatherElement['Time']:
          #     print(f"    {datetime.fromisoformat(time['StartTime']).strftime("%Y-%m-%d %H:%M")}~{datetime.fromisoformat(time['EndTime']).strftime("%Y-%m-%d %H:%M")},現象:{time['ElementValue'][0]['Weather']}")
          

          # if WeatherElement['ElementName'] == '天氣預報綜合描述':
          #   print('天氣預報綜合描述:')
          #   for time in WeatherElement['Time']:
          #     print(f"    {datetime.fromisoformat(time['StartTime']).strftime("%Y-%m-%d %H:%M")}~{datetime.fromisoformat(time['EndTime']).strftime("%Y-%m-%d %H:%M")},描述:{time['ElementValue'][0]['WeatherDescription']}")
          

else:
    print(f"請求失敗，狀態碼：{ThreeDayWeatherResponse.status_code}")
