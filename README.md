# 自動登入校園網

本脚本實現了對 2024 年新系統和 2023 年舊系統校園網自動登錄，以及發送登入訊息。

**請填写校园网運營商、账户和密码，并根據自身情況修改或刪除 Webhook 部分。**

## 變數

| 變數 | 介紹 |
| :----: | :----: |
| isp | 校園網運營商 |
| userid | 校園網賬戶（學號） |
| password | 校園網密碼 |
| webhook_name | 發送登入訊息時的 Webhook 名稱 |
| webhook_key | 發送登入訊息時的 Webhook 密鑰 |

## PC

Windows、Linux、Mac 等電腦端推薦直接使用網頁登錄。

### Python

**目前無法登入新版登錄界面，需要修改 `auth.py` 檔案。**

請在 `config.json` 檔案中填寫登入信息。

再將 `main.py` 檔案打包成 exe 檔案即可運行使用：

```bash
pyinstaller -F -w .\Python\main.py
```

脚本會在後臺持續檢測網絡連接狀態。

搭配 Windows `工作排程器`可以實現連接校園網後自動登入。

參考：[如何设置计划任务或者脚本才能使电脑在连接指定 Wi-Fi 后自动运行某程序？](https://www.zhihu.com/question/50249683)

## OpenWrt

### Bash

在 OpenWrt 上使用 Bash 脚本實現路由器分享校園網。

#### 啓動項

請在 `cqjtu_waln.sh` 檔案中填寫登入信息。

將資料夾中的 `cqjtu_wlan` 檔案複製到 /etc/init.d/。

並為脚本賦予執行權限：

```bash
chmod 755 /etc/init.d/cqjtu_wlan
```

再將其它的 `.sh` `.py` 檔案複製到 /home/。

將啓動項設置開機自啓動並運行：

```bash
cd /etc/init.d/cqjtu_wlan
./cqjtu_wlan enable
./cqjtu_wlan start
```

**在 v1.2 版本后增加了宿舍斷電前關機的功能，適用於 ext4 的檔案系統，默認關閉。**

#### 防火墻

防火墻設置自定義規則在一定程度上防止校園網多設備檢測：

```bash
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
```

請將上述命令末尾的 `192.168.1.1` IP 更換為路由器的默認網關。

參考：[关于某大学校园网共享上网检测机制的研究与解决方案](https://www.sunbk201.site/posts/crack-campus-network)

## Android

### Tasker

Android 設備通過 `Tasker` 軟體完成自動化操作，**本軟體依賴 Google Play 服務**。

下載鏈接：[Tasker](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm)

**Tasker 任務中，`登出校園網` 任務目前無法正常執行。**

#### 導入文件

請將 `cqjtu_wlan.prj.xml` 檔案導入專案。

#### 變數

在 `變數` 板塊中填寫對應的訊息。

| 變數 | 介紹 |
| :----: | :----: |
| %Cqjtu_wlan_isp | 校園網運營商 |
| %Cqjtu_wlan_userid | 校園網賬戶（學號） |
| %Cqjtu_wlan_password | 校園網密碼 |

#### 配置檔

在 `配置檔` 板塊中開啟 `登入校園網` 配置檔，並點擊右上方 `✓` 符號以保存。

通常來說，設備登入後再斷開校園網，無需再次登入。

啟動配置檔後，設備每次連結 Wi-Fi 後均會檢查是否需要登入校園網，請在安裝軟體時按照提示設置保活設置。

## iOS

### 捷徑

iOS、iPadOS 設備通過 `捷徑` 軟體完成自動化操作。

下載連結：[捷徑](https://apps.apple.com/us/app/shortcuts/id915249334)

**捷徑任務中，`登出校園網` 任務目前無法正常執行。**

#### 分享

- [登入校園網 電腦端](https://www.icloud.com/shortcuts/3858d60733c341b4a7fb79a37d96e431)
- [登入校園網 移動端](https://www.icloud.com/shortcuts/2db2cbcc0e5445db9dd47216363474ed)
- ~~[登出校園網](https://www.icloud.com/shortcuts/cd749c6db4db4512a582cff1e7c455f5)~~
- [網絡測試](https://www.icloud.com/shortcuts/045fc60a81f246d7bd0fcc625b190a75)


## License

[The MIT License (MIT)](https://github.com/finn-chan/cqjtu_wlan/blob/master/LICENSE)
