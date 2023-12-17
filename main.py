import json
import os
import sys
import time

import win11toast

import auth
import match_network
import send_to

# 讀取配置文件
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)
    # print(config_data['userid'])

cycles = 0
while True:
    state = match_network.match_cqjtu(config_data['school_url'], config_data['internet_url'], config_data['timeout'])
    if state == 1:
        if auth.DoLogOut(config_data['log_out_page'], config_data['timeout']):  # 登入前先登出
            time.sleep(config_data['timeout'])
            if auth.DoLogIN(config_data['userid'], config_data['password'], config_data['log_in_page'],
                            config_data['timeout']):  # 登入
                time.sleep(2)
                if config_data['ifttt']:  # 發送訊息給 IFTTT
                    time.sleep(2)
                    send_to.ifttt(config_data['webhooks_name'], config_data['webhooks_key'], config_data['timeout'])
                win11toast.toast('重慶交通大學', '已連接校園網',
                                 icon=os.path.dirname(os.path.abspath(sys.argv[0])) + '\\cqjtu.ico')

    elif state == 2:  # 已連接校園網
        if cycles:
            pass
        else:  # 初次彈窗提醒
            win11toast.toast('重慶交通大學', '已連接校園網',
                             icon=os.path.dirname(os.path.abspath(sys.argv[0])) + '\\cqjtu.ico')

    elif state == 0:  # 未連接校園網，程序終止
        # print('Over!')
        break

    cycles += 1
    time.sleep(30)

# auth.DoLogOut(config_data['log_out_page'],config_data['timeout'])
# send_to.ifttt(config_data['webhooks_name'], config_data['webhooks_key'], config_data['timeout'])
