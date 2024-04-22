# 判斷是否會斷電
import sys

import requests


def get_holiday_info(url: str, headers: dir):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return f'Get Date Info Error: {e}'


if __name__ == '__main__':
    date = sys.argv[1]

    url = f'http://timor.tech/api/holiday/info/{date}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'}

    # 獲取日期信息
    result = get_holiday_info(url, headers)

    # 判斷是否會斷電
    # 0、1、-1 分別表示今日 不斷電、斷電、錯誤
    if isinstance(result, dict) and 'type' in result:
        type = result['type']['type']
        if result['type']['type'] == 0:
            print(1)
        else:
            print(0)
    else:
        print(-1)

"""
API 文檔
http://timor.tech/api/holiday

    {
      "code": 0,               // 0服务正常。-1服务出错
      "holiday": {             // 传过来的日期是什么，key就是什么。传多少个就有多少个。
        "2017-10-01": {        // holiday的值都是一致的
          "holiday": true,
          "name": "国庆节",
          "wage": 2
        },
        "2017-9-12": null      // 如果不是节假日，则为null
      },
      "type": {                     // 只有明确指定参数 type=Y 时才返回类型信息
        "2017-10-01": {             // 一一对应holiday对象的key，holiday有多少个这里就有多少个
          "type": enum(0, 1, 2, 3), // 节假日类型，分别表示 工作日、周末、节日、调休。
          "name": "周六",            // 节假日类型中文名，可能值为 周一 至 周日、假期的名字、某某调休。
          "week": enum(1 - 7)       // 一周中的第几天。值为 1 - 7，分别表示 周一 至 周日。
        }
      }
    }
"""
