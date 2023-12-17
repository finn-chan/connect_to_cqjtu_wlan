import requests


# 登入
def DoLogIN(userid, password, log_in_page, timeout):
    header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'DDDDD': userid,
        'upass': password,
        '0MKKey': '%B5%C7%A1%A1%C2%BC',
        'v6ip': None
    }
    try:
        response = requests.post(url=log_in_page, data=data, headers=header, timeout=timeout)
        # print(response.status_code)
        return True
    except requests.exceptions.RequestException:
        return False


# 登出
def DoLogOut(log_out_page, timeout):
    try:
        response = requests.get(url=log_out_page, timeout=timeout)
        # print(response.status_code)
        # win11toast.toast('重慶交通大學', '已連接校園網')
        return True
    except requests.exceptions.RequestException:
        return False
