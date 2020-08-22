# 监控数据
LOTTERY_DATA = {
    # 双色球
    'ssq': [
        {'num': "4,9,10,14,18,20,21,22,23@9,11", 'multiple': 2},
    ],
    # 大乐透
    'dlt': [
        {'num': "7,10,17,25,30,31,32@1,7,9", 'multiple': 1, 'append': True},
    ]
}

# 通知渠道
NOTIFY_CHANNEL_CONFIG = {
    # 替换为自己的
    'dingtalk': {
        'access_token': '',
        'sign': '',
    },
    'smtp': {
        'sender': '',
        'code': '',
        'receive': [''],
    }
}
