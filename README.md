# Lottery number tracking hepler

## 背景

本人有追号习惯（小买怡情，诸君就不要吐槽买彩票这个事了），迫于每期的结果需要自己去看并且兑奖，刚好最近在学习Python(PHP全栈背景)，突发奇想
写一个小脚本解决当前需求，用正在学习的东西解决实际问题是提升的最好方式，写完这个感觉也的确学到不少。分享给大家学习交流之用。

PS：鉴于项目背景，就不写英文版了。

## 功能

**每一期晚上开奖（程序固定为晚上10点）的时候会通过接口获取最新的开奖信息并和你的号码进行比对，中奖与否都会发送开奖信息。**

**目前仅支持大乐透，双色球的单注或复式，并能算出中了多少注和金额。支持的通知发送方式有钉钉机器人和邮件。**


## 必要配置

**追号配置：**

在 `config.py` 里按照格式，修改你自己的号码，多注的话就直接加dict就行了。

复式的话只需要把号码都列出来，程序会自动识别。@之前是红区，之后是蓝区。multuple是倍数的意思。

![config-1](http://mrzfiles.oss-cn-shenzhen.aliyuncs.com/lottery-tracking/config-1.png)


**邮箱配置：**

以QQ邮箱为例，在顶部->设置->账户中，找到**POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务**一项，生成一个授权码

![qqmail-setting](http://mrzfiles.oss-cn-shenzhen.aliyuncs.com/lottery-tracking/qqmail-setting.png)

![qqmail-setting2](http://mrzfiles.oss-cn-shenzhen.aliyuncs.com/lottery-tracking/qqmail-setting2.png)

在配置项中，`sender`为qq邮箱的地址，`code`是刚刚获取的code,`receive`是要发送的邮箱地址

**钉钉配置:**

1， 发起群聊

![dingtalk](http://mrzfiles.oss-cn-shenzhen.aliyuncs.com/lottery-tracking/dingtalk-1.png)

2， 选择分类创建

![dingtalk](http://mrzfiles.oss-cn-shenzhen.aliyuncs.com/lottery-tracking/dingtalk-2.png)

3， 随便选一个，我选值班群

![dingtalk](http://mrzfiles.oss-cn-shenzhen.aliyuncs.com/lottery-tracking/dingtalk-3.png)

4， 随便选一个，我选值班群

![dingtalk](http://mrzfiles.oss-cn-shenzhen.aliyuncs.com/lottery-tracking/dingtalk-4.png)

5， 在智能群助手里选择添加机器人

![dingtalk](http://mrzfiles.oss-cn-shenzhen.aliyuncs.com/lottery-tracking/dingtalk-5.png)

![dingtalk](http://mrzfiles.oss-cn-shenzhen.aliyuncs.com/lottery-tracking/dingtalk-6.png)

6， 选择自定义

![dingtalk](http://mrzfiles.oss-cn-shenzhen.aliyuncs.com/lottery-tracking/dingtalk-7.png)

7， 安全设置选择“加签”，获取到`sign`

![dingtalk](http://mrzfiles.oss-cn-shenzhen.aliyuncs.com/lottery-tracking/dingtalk-8.png)

8， 点击完成，获取到 `access_token`

![dingtalk](http://mrzfiles.oss-cn-shenzhen.aliyuncs.com/lottery-tracking/dingtalk-9.png)

将以上的配置获取的信息填入相应的配置项就可以了，。

![config-2](http://mrzfiles.oss-cn-shenzhen.aliyuncs.com/lottery-tracking/config-2.png)


**接口配置**

在[聚合API](https://www.juhe.cn/docs/api/id/300 "聚合API") 申请一个，免费的就够用了。
动手能力强的大佬也可以自己爬彩票网站。这个就不展开了，这一步主要是获取到一个 `API_KEY`

填入到 `app/juhe_api.py` 的 `API_KEY` 一栏即可。

![apiconfig](http://mrzfiles.oss-cn-shenzhen.aliyuncs.com/lottery-tracking/apiconfig.png)


## 截图

钉钉效果

![dingtalk](http://mrzfiles.oss-cn-shenzhen.aliyuncs.com/lottery-tracking/dingtalk.png)

邮箱效果

![mail](http://mrzfiles.oss-cn-shenzhen.aliyuncs.com/lottery-tracking/qqmail.png)


## 运行

### 本地运行

**安装venv(Windows版)**

管理员身份运行`powershell` 并进入当前目录

`py -3 -m venv venv`

稍等片刻后，运行：

`.\venv\Scripts\activate`

**安装依赖**

`pip install -r requirements.txt`

然后 `python run.py即可`

### 服务器运行

推荐使用docker部署，简单快捷

**docker环境部署**

`docker build -t lottery-tracking-image .`

`docker run -d --name lottery-tracking lottery-tracking-image`

---

要更多DIY的话就自己改吧。希望大家中大奖，哈哈！THANKS
    
