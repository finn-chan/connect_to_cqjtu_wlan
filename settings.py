import json
from datetime import datetime

import option


# 讀取 json 文件
def Read(path: str) -> dict:
    with open(path, 'r') as config_file:
        data = json.load(config_file)
        return data


# 讀寫 json 文件
def Write(path: str, ip: str, date: str) -> None:
    with open(path, 'r+') as file:
        data = json.load(file)
        data['ip'] = ip
        data['date'] = date
        file.seek(0)
        json.dump(data, file, indent=2)
        file.truncate()


# 判斷是否應該發送訊息
def Judge(ip: str, date: str) -> bool:
    args = option.Parse()
    data = Read(args['data'])
    # ip 改變或据上一次發送大於等於7天
    if data['ip'] != ip or (
            datetime.strptime(date, "%Y-%m-%d").date() - datetime.strptime(data['date'], "%Y-%m-%d").date()).days >= 7:
        return True
    else:
        return False
