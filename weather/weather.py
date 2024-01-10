import requests
import configparser

from datetime import datetime

now = datetime.now()

config = configparser.ConfigParser()
config.read('env.ini', encoding='utf-8')
Authorization = config['Key']['Authorization']

locationId = [
  "F-D0047-001",
  "F-D0047-005",
  "F-D0047-009",
  "F-D0047-013",
  "F-D0047-017",
  "F-D0047-021",
  "F-D0047-025",
  "F-D0047-029",
  "F-D0047-033",
  "F-D0047-037",
  "F-D0047-041",
  "F-D0047-045",
  "F-D0047-049",
  "F-D0047-053",
  "F-D0047-057",
  "F-D0047-061",
  "F-D0047-065",
  "F-D0047-069",
  "F-D0047-073",
  "F-D0047-077",
  "F-D0047-081",
  "F-D0047-085",
  "F-D0047-089",
  "F-D0047-057"
]

url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-093?Authorization=' + Authorization + '&locationId=F-D0047-029'
data = requests.get(url)
data_json = data.json()

locations = data_json['records']['locations']
for i in locations:
  city = i['locationsName']  # 城市
  location = i['location']  
  for j in location :
    locationName = j['locationName'] # 鄉鎮
    if(locationName == '大林鎮'):
      weatherElement = j['weatherElement'] #天氣
        # 12小時降雨機率
        # 天氣現象
        # 體感溫度
        # 溫度
        # 相對濕度
        # 舒適度指數
        # 天氣預報綜合描述
        # 6小時降雨機率
        # 風速
        # 風向
        # 露點溫度
      print(weatherElement[6]['description'])
      for k in weatherElement[6]['time']:
        startTime = datetime.strptime(k['startTime'], '%Y-%m-%d %H:%M:%S')
        endTime = datetime.strptime(k['endTime'], '%Y-%m-%d %H:%M:%S')
        if(now > startTime and now < endTime ):
          result = k['elementValue'][0]['value']
          print(result)
        
        
        
        
        
