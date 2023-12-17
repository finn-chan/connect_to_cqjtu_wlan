from socket import gethostname, gethostbyname
from urllib.parse import quote

import requests


def Trigger(name: str, key: str, timeout: int) -> bool:
    hostname = gethostname()
    ip = gethostbyname(hostname)

    hostname = hostname.replace('-', ' ')
    try:
        res = requests.get(
            url='https://maker.ifttt.com/trigger/%s/with/key/%s?value1=%s%%0A%s%%0A%s' %
                (name, key, hostname, quote(quote('校園網已連接')), ip), timeout=timeout,
        )
        if res.status_code == 200:
            return True
        return False
    except requests.exceptions.RequestException:
        return False
