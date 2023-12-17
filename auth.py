from time import sleep

import requests


def Login(userid: str, password: str, log_in_page: str, timeout: int) -> bool:
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'DDDDD': userid,
        'upass': password,
        '0MKKey': '%B5%C7%A1%A1%C2%BC',
        'v6ip': None,
    }

    try:
        res = requests.post(
            timeout=timeout, headers=headers, data=data,
            url=log_in_page,
        )

        if res.status_code != 200:
            return False

        sleep(5)
        return True
    except requests.exceptions.RequestException:
        return False


def Logout(log_out_page: str, timeout: int) -> bool:
    try:
        res = requests.get(
            timeout=timeout,
            url=log_out_page,
        )

        if res.status_code != 200:
            return False

        sleep(5)
        return True
    except requests.exceptions.RequestException:
        return False
