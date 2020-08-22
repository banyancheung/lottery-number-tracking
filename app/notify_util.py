import base64
import hashlib
import hmac
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
import urllib

import requests


def notify(config, origin_content):
    for channel, setting in config.items():
        content = format_content(channel, origin_content)
        if channel == 'smtp':
            notify_email(setting, origin_content['prize_msg'], content)
        if channel == 'dingtalk':
            notify_dingtalk(setting, content)


def format_content(channel, origin_content):
    text = f"""
{origin_content['prize_msg']}\n
开奖号码：{origin_content['lottery_res']}\n
你的号码: \n
{origin_content['lottery_num']}
\n
    """
    if origin_content['is_prize']:
        text += "中奖信息：\n"
        for prize in origin_content['lottery_prize']:
            text += f"{prize['prize_name']}:[{prize['prize_require']}],{prize['prize_num']}注,估算奖金：{prize['prize_money']}\n"

    if channel == 'dingtalk':
        content = json.dumps({
            'msgtype': 'text',
            'text': {
                'content': text
            }
        })
    elif channel == 'smtp':
        content = text
    return content


def notify_email(config, subject, content):
    from_addr = config['sender']  # 邮件发送账号
    to_addrs = config['receive']  # 接收邮件账号
    qq_code = config['code']  # 授权码（这个要填自己获取到的）
    smtp_server = 'smtp.qq.com'  # 固定写死
    smtp_port = 465  # 固定端口
    # 配置服务器
    stmp = smtplib.SMTP_SSL(smtp_server, smtp_port)
    stmp.login(from_addr, qq_code)
    # 组装发送内容
    message = MIMEText(content, 'plain', 'utf-8')  # 发送的内容
    message['From'] = Header("开奖通知", 'utf-8')  # 发件人
    message['To'] = Header("订阅者", 'utf-8')  # 收件人
    message['Subject'] = Header(subject, 'utf-8')  # 邮件标题
    try:
        stmp.sendmail(from_addr, to_addrs, message.as_string())
    except Exception as e:
        print('邮件发送失败--' + str(e))


def notify_dingtalk(config, content):
    timestamp = str(round(time.time() * 1000))
    secret_enc = config['sign'].encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, config['sign'])
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    query_param = {'access_token': config['access_token'], 'timestamp': timestamp, 'sign': sign}
    url = 'https://oapi.dingtalk.com/robot/send'
    headers = {
        "content-type": "application/json"
    }
    requests.post(url, headers=headers, params=query_param, data=content)
