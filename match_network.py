import datetime

import psutil
import requests


def match_cqjtu(school_url, internet_url, timeout):
    try:
        response = requests.get(school_url, timeout=timeout)  # 檢查是否鏈接校園網

        if response.status_code == 200:  # 狀態碼200為連接校園網
            if datetime.time(6, 30) <= datetime.datetime.now().time() <= datetime.time(23, 29) or (
                    datetime.time(23, 30) <= datetime.datetime.now().time() <= datetime.time(6,
                                                                                             29) and psutil.sensors_battery().power_plugged):  # 判斷校園網是否供網
                try:
                    response = requests.get(internet_url, timeout=timeout)  # 檢查校園網是否登錄
                    if response.status_code == 204:  # 狀態碼204為登入校園網
                        return 2  # 已連接互聯網
                    else:
                        return 1  # 未連接互聯網

                except requests.exceptions.RequestException:
                    return 1  # 未連接互聯網
            else:
                return 2  # 已連接校園網，但不在供網時間内

        else:
            return 0  # 未連接校園網

    except requests.exceptions.RequestException:
        return 0  # 未連接校園網
