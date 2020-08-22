import json

import requests


class JuheApi(object):

    API_KEY = ''

    def fetch_latest_ssq(self):
        config = {
            'query_param': {
                'key': self.API_KEY,
                'lottery_id': 'ssq',
            },
            'method': 'get',
            'url': 'http://apis.juhe.cn/lottery/query'
        }
        return self.request(config)

    def fetch_latest_dlt(self):
        config = {
            'query_param': {
                'key': self.API_KEY,
                'lottery_id': 'dlt',
            },
            'method': 'get',
            'url': 'http://apis.juhe.cn/lottery/query'
        }
        return self.request(config)

    @staticmethod
    def request(config):
        if config['method'] == 'get':
            response = requests.get(config['url'], params=config['query_param'])
        elif config['method'] == 'post':
            response = requests.post(config['url'], params=config['query_param'], data=config['data'])
        result = json.loads(response.text)
        if result["error_code"] == 0:
            return result
        else:
            return {}
