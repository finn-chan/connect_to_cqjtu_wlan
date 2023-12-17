import requests


def HasConnection(url: str, code: int, timeout: int) -> bool:
    try:
        res = requests.get(timeout=timeout, url=url)
        if res.status_code != code:
            return False
        return True
    except requests.exceptions.ConnectionError:
        return False


def IsCQJTU(school_url: str, timeout: int) -> bool:
    return HasConnection(
        url=school_url,
        timeout=timeout,
        code=200,
    )
