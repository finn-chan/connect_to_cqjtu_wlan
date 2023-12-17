from datetime import datetime
from sys import exit


def Println(text: str) -> None:
    time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    print('%s %s' % (time, text))


def Fatalln(text: str) -> None:
    time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    print('%s %s' % (time, text))
    exit(1)
