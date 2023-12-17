from datetime import datetime
from socket import gethostname, gethostbyname
from urllib.parse import quote

import requests

import option
import settings


# 發送訊息至 IFTTT
def Trigger(name: str, key: str, timeout: int) -> bool:
    hostname = gethostname()
    ip = gethostbyname(hostname)
    date = datetime.now().date().strftime("%Y-%m-%d")

    if settings.Judge(ip, date):
        hostname = hostname.replace('-', ' ')
        try:
            res = requests.get(
                url='https://maker.ifttt.com/trigger/%s/with/key/%s?value1=%s%%0A%s%%0A%s' %
                    (name, key, hostname, quote(quote('校園網已連接')), ip), timeout=timeout,
            )

            # 更新數據
            args = option.Parse()
            settings.Write(args['data'], ip, date)

            if res.status_code == 200:
                return True
            print('1')
            return False

        except requests.exceptions.RequestException:
            print('2')
            return False

    else:
        return True
