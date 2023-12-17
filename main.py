from time import sleep

import auth
import connectivity
import icon
import info
import notification
import option
import settings
import webhook


def main():
    args = option.Parse()
    config = settings.Read(args['config'])

    notify = True
    info.Println('程序啓動成功')

    while True:
        if connectivity.IsCQJTU(
                school_url=config['school_url'],
                timeout=config['timeout'],
        ):
            info.Println('校園網已連接')

        if connectivity.HasConnection(
                url=config['generate_204'], code=204,
                timeout=config['timeout'],
        ):
            info.Println('網絡已連接')
            sleep(10)
            continue

        # 登入前先登出
        ok = auth.Logout(
            log_out_page=config['log_out_page'],
            timeout=config['timeout']
        )
        if not ok:
            notification.Toast(
                title='重慶交通大學',
                message='登出失敗',
                icon=icon.Path('cqjtu.ico'),
            )
            info.Println('校園網登出失敗')
            sleep(10)
            continue

        # 执行登入
        ok = auth.Login(
            userid=config['userid'],
            password=config['password'],
            log_in_page=config['log_in_page'],
            timeout=config['timeout'],
        )
        if not ok:
            notification.Toast(
                title='重慶交通大學',
                message='登入失敗',
                icon=icon.Path('cqjtu.ico'),
            )
            info.Println('校園網登入失敗')
            sleep(10)
            continue

        # 触发 Webhook
        ok = webhook.Trigger(
            name=config['webhooks_name'],
            key=config['webhooks_key'],
            timeout=config['timeout'],
        )
        if not ok:
            notification.Toast(
                title='重慶交通大學',
                message='Webhook 觸發失敗',
                icon=icon.Path('cqjtu.ico'),
            )
            info.Println('Webhook 觸發失敗')
            sleep(10)
            continue

        # Windows 通知
        notification.Toast(
            title='重慶交通大學',
            message='校園網已連接',
            icon=icon.Path('cqjtu.ico'),
        )

        info.Println('校園網已連接')
        sleep(10)


if __name__ == '__main__':
    main()
