import json
import time
import socket
import requests
from datetime import datetime
from urllib.parse import quote


def ifttt(webhooks_name, webhooks_key, timeout):
    # 讀取已有的 JSON 數據
    with open('data.json') as json_file:
        data = json.load(json_file)

    # 獲取主機名
    hostname = socket.gethostname()

    # 獲取本機 IP 地址
    ip_address = socket.gethostbyname(hostname)
    hostname = hostname.replace('-', ' ')

    # print("主機名:", hostname)
    # print("IPv4 地址:", ip_address)

    # 獲取當前時間
    current_date = datetime.now().date()

    # IPv4 地址發生變化或上次發送距今超過一周發送訊息
    if data['cqjtu_ipv4_address'] != ip_address or (
            current_date - datetime.strptime(data['send_date'], "%Y-%m-%d").date()).days >= 7:
        # 發送信息給 IFTTT
        while True:
            try:
                response = requests.get(
                    url='https://maker.ifttt.com/trigger/' + webhooks_name + '/with/key/' + webhooks_key + '?value1=' + hostname + '%0A' + quote(
                        quote(
                            '已連接校園網')) + '%0A' +
                        ip_address, timeout=timeout)
                if response.status_code == 200:
                    break

            except requests.exceptions.RequestException:
                pass

            time.sleep(timeout)

        # 更新 IPv4 地址
        data['cqjtu_ipv4_address'] = ip_address
        data['send_date'] = current_date.strftime('%Y-%m-%d')  # 將 datetime 對象轉換為字符串

        # 寫入更新後的數據到 JSON 文件
        with open('data.json', 'w') as json_file:
            json.dump(data, json_file)
