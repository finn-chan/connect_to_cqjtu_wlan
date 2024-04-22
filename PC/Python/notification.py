from win11toast import toast


def Toast(title: str, message: str, icon: str) -> None:
    toast(title, message, icon=icon)
