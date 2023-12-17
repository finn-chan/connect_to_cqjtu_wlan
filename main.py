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
    wait_time = 10
    info.Println('程序啓動成功')

    while True:
        # 判斷是否連接校園網
        if connectivity.IsCQJTU(
                school_url=config['school_url'],
                timeout=config['timeout'],
        ):
            info.Println('校園網已連接')

            # 判斷是否連接互聯網
            if connectivity.HasConnection(
                    url=config['generate_204'], code=204,
                    timeout=config['timeout'],
            ):
                info.Println('互聯網已連接')
                sleep(wait_time)
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
                sleep(wait_time)
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
                sleep(wait_time)
                continue

            # 触发 Webhook
            ok = webhook.Trigger(
                name=config['webhook_name'],
                key=config['webhook_key'],
                timeout=config['timeout'],
            )
            if not ok:
                notification.Toast(
                    title='重慶交通大學',
                    message='Webhook 觸發失敗',
                    icon=icon.Path('cqjtu.ico'),
                )
                info.Println('Webhook 觸發失敗')
                sleep(wait_time)
                continue

            # Windows 通知
            notification.Toast(
                title='重慶交通大學',
                message='校園網已連接',
                icon=icon.Path('cqjtu.ico'),
            )

            info.Println('校園網已連接')

        sleep(wait_time)


if __name__ == '__main__':
    main()
