#!/bin/sh
# Automatically Log In To The Campus Network With Mobile Login
# 自動登入校園網，以移動端登入
# Copyright (c) 2023-2024 Finn Chan <life4aran@gmail.com>
# v1.5


NAME=cqjtu_wlan
LOG_FILE=/var/log/$NAME.log

# 日志輸出模式
# 0 - 不輸出日志
# 1 - 輸出關鍵日志
# 2 - 輸出全部日志
LOG_LEVEL=1

# 檢查網路狀態
check_network_status() {
    http_status=$(curl -o /dev/null -s -w '%{http_code}' "http://connect.rom.miui.com/generate_204")
    # 直接 return 狀態碼會判斷錯誤
    echo $http_status
}

# 檢查應是否關機
check_shutdown(){
    # 獲取當前時間的小時和分鐘
    current_hour=$(date +%H)
    current_minute=$(date +%M)

    # 將當前時間轉換爲分鐘數
    current_time_in_minutes=$((current_hour * 60 + current_minute))

    # 將 22:58 和 23:00 轉換為分鐘數
    start_time_in_minutes=$((22 * 60 + 58))
    end_time_in_minutes=$((23 * 60))

    # 判斷當前時間是否在 22:58 至 23:00 之間
    if [ "$current_time_in_minutes" -ge "$start_time_in_minutes" ] && [ "$current_time_in_minutes" -le "$end_time_in_minutes" ]; then
        # 獲取明日信息
        tomorrow_date=$(date +%Y-%m-%d -d @$(( $(date +%s) + 86400 )))
        response=$(python3 power_outage.py "$tomorrow_date")

        if [ $response = 1 ]; then
            poweroff
        fi
fi
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
        return 0
    else
        return 1
    fi
}

# 輸出日志
log_message(){
	# 日志類型
	# 0 - 非關鍵日志
	# 1 - 關鍵日志
	local log_level=$1

	shift
    local message=$*

	# 輸出關鍵日志
	if [ "$LOG_LEVEL" -eq 1 ]; then
		if [ "$log_level" -eq 1 ]; then
			echo "$(date '+%Y-%m-%d %H:%M:%S') - $message" | tee -a $LOG_FILE
		fi

	# 輸出全部日志
	elif [ "$LOG_LEVEL" -eq 2 ]; then
		echo "$(date '+%Y-%m-%d %H:%M:%S') - $message" | tee -a $LOG_FILE
	fi
}

# 發送 Webhook 訊息
send_webhook_notification() {
    local webhook_domain=$1
    local webhook_name=$2
    local webhook_key=$3

    # 獲取並列印主機名稱
    hostname="Finn $(cat /proc/sys/kernel/hostname)"
    device_name=$(python -c "import urllib.parse; print(urllib.parse.quote('''$hostname'''))")

    # 提示詞
    clue=校園網已連接

    # 獲取 IPv4 地址
    ip_address=$(ip addr show dev 'eth1' | grep 'inet ' | awk '{print $2}' | cut -d/ -f1)
    
    # 前置轉義 .
    escaped_ip_address=${ip_address//./\\.}

    # 為 IPv4 地址添加鏈接
    encode_words=$(python -c "import urllib.parse; print(urllib.parse.quote('''$clue\n[$escaped_ip_address](http://$escaped_ip_address)'''))")

    # 發送 Webhook
    response=$(curl -w "%{http_code}" -o /dev/null -s "https://$webhook_domain/trigger/$webhook_name/with/key/$webhook_key?value1=$device_name&value2=$encode_words&value3=MarkdownV2")

    # 檢查返回的狀態碼
    if [ "$response" -eq 200 ]; then
        return 0
    else
        return 1
    fi
}


main() {
    # 校園網帳戶
    local userid=教工號或學號

    # 校園網密碼
    local password=初始密碼為身份證后六位

    # 校園網運營商
    # 空值 - 教師
    # @cmcc - 移動
    # @telecom - 電信
    # @unicom - 聯通
    local isp=

    # Webhook 網域
    local webhook_domain=

    # Webhook 名稱
    local webhook_name=

    # Webhook 金鑰
    local webhook_key=


    # 登錄次數
    local login_count=0

    # 上一次 IPV4 地址
    local previous_ip_address=0

    while true; do
        # 檢測網路狀態
        http_status=$(check_network_status)

        # 獲取當前 IPv4 地址
        current_ip_address=$(ip addr show dev 'eth1' | grep 'inet ' | awk '{print $2}' | cut -d/ -f1)

        # 已登入
        if [ "${http_status}" = "204" ]; then

            login_count=$((login_count + 1))

            if [ "$current_ip_address" != "$previous_ip_address" ]; then
				message="Login Detected"
				log_message 1 $message

                # 發送成功
                if send_webhook_notification $webhook_domain $webhook_name $webhook_key; then
					message=".... Send Sucessful"
					log_message 1 $message
                    previous_ip_address=$current_ip_address

                # 發送失敗
                else
					message=".... Send Failure"
					log_message 1 $message
                fi

			else
				message="Login Detected"
				log_message 0 $message
            fi

        # 未登入
        elif [ "${http_status}" = "200" ]; then
            # 登入成功
            if login $userid $password $isp; then
				message="Login Successful"
				log_message 1 $message
                login_count=$((login_count + 1))

                if [ "$current_ip_address" != "$previous_ip_address" ]; then
                    # 發送成功
                    if send_webhook_notification $webhook_domain $webhook_name $webhook_key; then
						message=".... Send Sucessful"
						log_message 1 $message
                        previous_ip_address=$current_ip_address

                    # 發送失敗
                    else
						message=".... Send Failure"
						log_message 1 $message
                    fi

                else
					message=".... No Send"
					log_message 1 $message
            fi

            # 登入失敗
            else
				message="Login Failure"
				log_message 1 $message
            fi

        # 網絡錯誤
        else
			message="Network Abnormal"
			log_message 1 $message
        fi

        # 檢查應是否關機
        # check_shutdown

        sleep 60

    done
}

main
