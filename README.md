# 製作 Facebook Messenger Bots 教學（使用ngrok）
Building Facebook Messenger Bots with Python and ngrok


## Development Environment Setup

### 需要使用的工具：
-   Python 3.6 (可在這[下載](https://www.python.org/downloads/))
-   Pip (可在這[下載](https://pypi.python.org/pypi/pip))


### 在Mac Os 安裝 Virtualenv(虛擬環境)
可以減少不同版本套件載再一起而造成程式開發混淆。

1. 建立虛擬環境（指令會建立資料夾，並在之中加入必要程式＆資料檔案）
```
//python3
$ virtualenv -p python3 FbBot
```
2. 啟用虛擬環境（切換到該資料夾中）
```
$ cd FbBot
$ source bin/activate

//如果要離開虛擬環境
//$ deactivate
```

3. Clone git repository
```
$ git clone https://github.com/monica-shiao/FBBot-Python.git

$ cd FBBot-Python

//安裝所需的依賴包
$ pip install -r requirements.txt
```

---
### 在fb上製作你的機器人
https://developers.facebook.com/

可視以下完整的教程製作。
補充：

#### Step1. 產生粉絲專頁存取權杖
在facebook for developer中新增應用程式完，主畫面側邊欄->產品->Mesenger->設定中，產生粉絲專頁存取權杖

---
### 主機 - Ngrok (簡單讓外網連到自己的api)

未有ngrok，可在[此處](https://gist.github.com/jwebcat/ecaac7bc7ee26e01cd4a)的說明進行操作下載。

#### Step2. 編寫 app.py 中的 ACCESS_TOKEN / VERIFY_TOKEN
- ACCESS_TOKEN：填入剛剛產生的粉絲專頁存取權杖
- VERIFY_TOKEN：隨意填寫

#### Step3. 執行rgrok
```
//先執行 app.py
$ python3 app.py
```

應會產生：`* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`

再來，打開一個新的terminal
```
//5000 可以依 port的不同更改
$ ngrok http 5000
```

---
#### Step4. 設定 webhooks
回到Step1的設定頁，設定 webhooks
- Callback Url: 填入剛剛ngrok 產生 https的那串網址。
- Verify Token: 填入剛剛在app.py中填寫的 VERIFY_TOKEN字串
- 選擇活動（至少要有）：
    - check the messages
    - messaging_postbacks
    - message_deliveries
    - messaging_pre_checkouts boxes.
- 訂閱粉絲專頁

---
### 測試～～～～完成～～～～

詳細操作步驟可見以下的完整教程。


### 參考資料
[完整教程](https://www.twilio.com/blog/2017/12/facebook-messenger-bot-python.html)





