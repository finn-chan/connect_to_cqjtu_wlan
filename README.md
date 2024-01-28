# 自動登入校園網

本脚本實現了對 2024 年新系統和 2023 年舊系統校園網自動登錄功能，以及發送通知訊息

**請根據自身情況修改或刪除 IFTTT 部分 Webhook**

## Windows

將 Python 文件打包成 exe 文件即可運行使用

    pyinstaller -F -w .\Python\main.py

脚本會在後臺持續檢測網絡連接狀態

搭配 Windows `工作排程器`可以實現連接校園網後自動登入

參考：[如何设置计划任务或者脚本才能使电脑在连接指定wifi后自动运行某程序？](https://www.zhihu.com/question/50249683)

## OpenWrt

### 啓動項

將 `Bash` 文件夾中的 cqjtu_wlan 文件複製到 /etc/init.d/，其它的 .sh .py 文件複製到 /home/

將啓動項設置開機自啓動並運行

    cd /etc/init.d/cqjtu_wlan
    ./cqjtu_wlan enable
    ./cqjtu_wlan start

**在 v1.2 版本中增加了宿舍斷電前關機的功能，適用於 ext4 的檔案系統**

### 防火墻

防火墻設置自定義規則在一定程度上防止校園網多設備檢測

    # UDP 端口 443 流量拦截规则
    iptables -t mangle -I PREROUTING -p udp -m multiport --dport 443 -j DROP
    ip6tables -t mangle -I PREROUTING -p udp -m multiport --dport 443 -j DROP
    
    # 为传入数据包设置 TTL
    iptables -t mangle -A PREROUTING -i eth0.2 -j TTL --ttl-set 64
    iptables -t mangle -A PREROUTING -i br-lan -j TTL --ttl-set 64
    
    # 重定向 NTP 流量
    iptables -t nat -N ntp_force_local
    iptables -t nat -I PREROUTING -p udp --dport 123 -j ntp_force_local
    iptables -t nat -A ntp_force_local -d 0.0.0.0/8 -j RETURN
    iptables -t nat -A ntp_force_local -d 127.0.0.0/8 -j RETURN
    iptables -t nat -A ntp_force_local -d 192.168.0.0/16 -j RETURN
    iptables -t nat -A ntp_force_local -s 192.168.0.0/16 -j DNAT --to-destination 192.168.1.1

請將 192.168.1.1 更換成路由器的默認網關

參考：[关于某大学校园网共享上网检测机制的研究与解决方案](https://www.sunbk201.site/posts/crack-campus-network)

## Android

## iOS

## License

[The MIT License (MIT)](https://github.com/finn-chan/cqjtu_wlan/blob/master/LICENSE)
