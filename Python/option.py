from argparse import ArgumentParser


def Parse() -> dict:
    parser = ArgumentParser(description='重慶交通大學校園網自動登錄')
    parser.add_argument(
        '--config', '-c', type=str,
        default='./config.json',
        help='配置文件路徑',
    )
    parser.add_argument(
        '--data', '-d', type=str,
        default='./data.json',
        help='data 文件路徑',
    )
    return vars(parser.parse_args())
