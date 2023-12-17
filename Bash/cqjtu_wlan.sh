#!/bin/sh
# 自動登入校園網，以移動端登入
# Created by Yuifun

# 檢測網路狀態
check_network_status() {
    http_status=$(curl -o /dev/null -s -w '%{http_code}' "http://connect.rom.miui.com/generate_204")
    # 直接 return 狀態碼會判斷錯誤
    echo $http_status
}

# 登入
login() {
    local userid=$1
    local password=$2
    local isp=$3

    # 執行登入操作
    login_response=$(curl "http://172.19.7.17/drcom/login?callback=dr1009&DDDDD=${userid}${isp}&upass=${password}&0MKKey=123456&R1=0&R2=&R3=0&R6=1&para=00&v6ip=&terminal_type=2&lang=zh-tw&jsVersion=4.2.1&v=6769")

    # 檢查是否登入成功
    if echo ${login_response} | grep -q "result\":1"; then
        echo "登入成功"
        return 0
    else
        echo "登入失敗"
        return 1
    fi
}

# 發送 Webhook 通知
send_webhook_notification() {
    local webhook_name=$1
    local webhook_key=$2

    # 獲取並列印主機名稱
    hostname="YUIs $(cat /proc/sys/kernel/hostname)"
    device_name=$(python -c "import urllib.parse; print(urllib.parse.quote('''$hostname'''))")

    # 對字符串進行兩次 URL 編碼
    clue=$(python -c "import urllib.parse; print(urllib.parse.quote('''校園網已連接'''))")

    # 使用 ip 命令獲取 IPv4 地址
    ip_address=$(ip addr show dev 'eth1' | grep 'inet ' | awk '{print $2}' | cut -d/ -f1)
    
    # 為 IPv4 地址添加鏈接
    encode_words=$(python -c "import urllib.parse; print(urllib.parse.quote('''$device_name%0A$clue%0A[$ip_address](http://$ip_address)&parse_mode=Markdown'''))")

    # 發送 Webhook
    curl "https://maker.ifttt.com/trigger/$webhook_name/with/key/$webhook_key?value1=$encode_words"
}

main() {
    # sleep 30
    
    # 校園網帳戶
    local userid= "請在這裏輸入學號"
    
    # 校園網密碼
    local password= "請在這裏輸入密碼"
    
    # 校園網運營商
    # 教師：空
    # 移動：@cmcc
    # 電信：@telecom
    # 聯通：@unicon
    local isp= "選擇上方的運營商"

    # # Webhook 名稱
    # local webhook_name=
    #
    # # Webhook 金鑰
    # local webhook_key=

    # 檢測網路狀態
    http_status=$(check_network_status)
    
    # 判斷是否登入
    if [ "${http_status}" = "204" ]; then
        echo "檢測到已登入"
        send_webhook_notification $webhook_name $webhook_key
    elif [ "${http_status}" = "200" ]; then
        echo "檢測到未登入，嘗試登入"
        if login $userid $password $isp; then
            echo "登入成功"
            # sleep 10
            # send_webhook_notification $webhook_name $webhook_key
        else
            echo "登入失敗"
        fi
    else
        echo "網路狀態異常"
    fi
}

main
