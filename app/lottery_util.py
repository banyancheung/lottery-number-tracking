import json
import logging
from datetime import datetime
from functools import reduce
from itertools import combinations

from app import LOTTERY_DATA
from app.config import NOTIFY_CHANNEL_CONFIG
from app.juhe_api import JuheApi
from app.notify_util import notify, notify_dingtalk


def get_lottery_res(lottery_type):
    api = JuheApi()
    if lottery_type == 'ssq':
        res = api.fetch_latest_ssq()
    else:
        res = api.fetch_latest_dlt()
    # if not is_latest_res(res['result']['lottery_date']):
    #     raise DayError('result date error')
    lottery_res = format_lottery_res(lottery_type, res['result']['lottery_res'])
    return lottery_res


def is_latest_res(lottery_date):
    current = datetime.today().strftime("%Y-%m-%d")
    return current == lottery_date


def format_lottery_res(lottery_type, origin_lottery_res):
    lottery_res_list = [x.lstrip('0') for x in list(origin_lottery_res.split(','))]
    if lottery_type == 'dlt':
        lottery_res = ','.join(lottery_res_list[0:5]) + '@' + ','.join(lottery_res_list[5:])
    elif lottery_type == 'ssq':
        lottery_res = ','.join(lottery_res_list[0:6]) + '@' + ','.join(lottery_res_list[6:])
    return lottery_res


def start_check_lottery():
    try:
        date = datetime.now()
        week_day = date.isoweekday()
        if week_day == 5:
            raise DayError('not open day')
        lottery_type = 'dlt' if week_day in (1, 3, 6) else 'ssq'
        lottery_res = get_lottery_res(lottery_type)
        result = LotteryResult(lottery_type, LOTTERY_DATA[lottery_type], lottery_res)
        origin_content = result.get_bonus_with_content()
        notify(NOTIFY_CHANNEL_CONFIG, origin_content)

    except DayError:
        content = json.dumps({
            'msgtype': 'text',
            'text': {
                'content': '非开奖日或获取开奖信息有误'
            }
        })
        notify_dingtalk(NOTIFY_CHANNEL_CONFIG['dingtalk'], content)
    except Exception as error:
        content = json.dumps({
            'msgtype': 'text',
            'text': {
                'content': error.__str__()
            }
        })
        notify_dingtalk(NOTIFY_CHANNEL_CONFIG['dingtalk'], content)


class LotteryResult(object):

    def __init__(self, lottery_type, lottery_config, lottery_res):
        self.result = []
        self.__lottery_type = lottery_type
        self.__lottery_config = lottery_config
        self.__lottery_res = lottery_res

    def get_bonus(self):
        if self.__lottery_type == 'ssq':
            self.result = self.__get_bonus_by_ssq()
        elif self.__lottery_type == 'dlt':
            self.result = self.__get_bonus_by_dlt()
        return self.result

    def get_default_content_title(self):
        date = datetime.today().strftime("%Y-%m-%d")
        lottery_type = '双色球' if self.__get_is_ssq() else '大乐透'
        return f"{date} - {lottery_type}开奖：本期没有中奖,请继续努力"

    def get_prize_content_title(self):
        date = datetime.today().strftime("%Y-%m-%d")
        lottery_type = '双色球' if self.__get_is_ssq() else '大乐透'
        return f"{date} - {lottery_type}：恭喜您中奖了！！"

    def get_bonus_with_content(self):
        content = {
            'is_prize': 0,
            'lottery_res': self.__lottery_res,
            'prize_msg': self.get_default_content_title(),
            'lottery_num': "\n".join([x['num'] for x in self.__lottery_config]),
            'lottery_prize': [],
        }
        result = self.result if self.result else self.get_bonus()
        count = 0
        for prize, num in result.items():
            if num > 0:
                count += num
                content['lottery_prize'].append({
                    'prize_name': self.get_prize_name_by_prize(prize),
                    'prize_require': self.__get_prize_require(prize),
                    'prize_num': num,
                    'prize_money': self.__get_prize_money(prize, num)
                })
        if count > 0:
            content['is_prize'] = 1
            content['prize_msg'] = self.get_prize_content_title()
        return content

    def __get_prize_require(self, prize):
        if self.__get_is_ssq():
            prize_require_map = {
                'first': '6+1',
                'second': '6+0',
                'third': '5+1',
                'fourth': '5+0,4+1',
                'fifth': '4+0,3+1',
                'sixth': '0+1',
            }
        else:
            prize_require_map = {
                'first': '5+2',
                'second': '5+1',
                'third': '5+0',
                'fourth': '4+2',
                'fifth': '4+1',
                'sixth': '3+2',
                'seventh': '4+0,',
                'eighth': '3+1,2+2',
                'ninth': '3+0,1+2,2+1,0+2',
            }
        return prize_require_map[prize] if prize in prize_require_map else ''

    def __get_prize_money(self, prize, num):
        if self.__get_is_ssq():
            prize_money_map = {
                'first': '恭喜中了特特特特大奖！',
                'second': '恭喜中了大奖！',
                'third': 3000 * num,
                'fourth': 200 * num,
                'fifth': 10 * num,
                'sixth': 5 * num,
            }
        else:
            prize_money_map = {
                'first': '恭喜中了特特特特大奖！',
                'second': '恭喜中了大奖！',
                'third': 100 * num,
                'fourth': 3000 * num,
                'fifth': 300 * num,
                'sixth': 200 * num,
                'seventh': 100 * num,
                'eighth': 15 * num,
                'ninth': 5 * num,
            }
        return prize_money_map[prize] if prize in prize_money_map else ''

    def __get_is_ssq(self):
        return self.__lottery_type == 'ssq'

    def __get_is_dlt(self):
        return self.__lottery_type == 'dlt'

    def __get_bonus_by_ssq(self):
        result = []
        for config in self.__lottery_config:
            bonus = self.__get_bonus_by_ssq_config(config)
            result.append(bonus)
        result = reduce(self.sum_dict, result)
        return result

    @staticmethod
    def sum_dict(a, b):
        temp = dict()
        for key in a.keys() | b.keys():
            temp[key] = sum([d.get(key, 0) for d in (a, b)])
        return temp

    def __get_bonus_by_dlt(self):
        result = []
        for config in self.__lottery_config:
            bonus = self.__get_bonus_by_dlt_config(config)
            result.append(bonus)
        result = reduce(self.sum_dict, result)
        return result

    def __get_bonus_by_ssq_config(self, config):
        real_red_tuple, real_blue_tuple = self.get_tuple_by_str(self.__lottery_res)
        red_tuple, blue_tuple = self.get_tuple_by_str(config['num'])
        is_compound = len(red_tuple) > 6
        result = {
            'first': 0,
            'second': 0,
            'third': 0,
            'fourth': 0,
            'fifth': 0,
            'sixth': 0,
        }
        if is_compound:
            combinations_arr = combinations(red_tuple, 6)
        else:
            combinations_arr = [red_tuple]

        for combination in combinations_arr:
            hit_red_count = len(set(combination) & set(real_red_tuple))

            for blue in blue_tuple:
                hit_blue_count = len(set(blue) & set(real_blue_tuple))
                # print('num', combination.__str__(), 'hit_red_count', hit_red_count, 'hit_blue_count', hit_blue_count)
                if hit_red_count == 6 and hit_blue_count == 1:
                    result['first'] += config['multiple']
                elif hit_red_count == 6:
                    result['second'] += config['multiple']
                elif hit_red_count == 5 and hit_blue_count == 1:
                    result['third'] += config['multiple']
                elif hit_red_count == 5 or (hit_red_count == 4 and hit_blue_count == 1):
                    result['fourth'] += config['multiple']
                elif hit_red_count == 4 or (hit_red_count == 3 and hit_blue_count == 1):
                    result['fifth'] += config['multiple']
                elif hit_red_count == 0 and hit_blue_count == 1:
                    result['sixth'] += config['multiple']
        return result

    def __get_bonus_by_dlt_config(self, config):
        real_red_tuple, real_blue_tuple = self.get_tuple_by_str(self.__lottery_res)
        red_tuple, blue_tuple = self.get_tuple_by_str(config['num'])
        is_front_compound = len(red_tuple) > 5
        is_backend_compound = len(blue_tuple) > 2
        result = {
            'first': 0,
            'second': 0,
            'third': 0,
            'fourth': 0,
            'fifth': 0,
            'sixth': 0,
            'seventh': 0,
            'eighth': 0,
            'ninth': 0,
        }

        if is_front_compound:
            red_combinations_arr = combinations(red_tuple, 5)
        else:
            red_combinations_arr = [red_tuple]

        if is_backend_compound:
            blue_combinations = list(combinations(blue_tuple, 2))
        else:
            blue_combinations = [blue_tuple]
        for red_combination in red_combinations_arr:
            hit_red_count = len(set(red_combination) & set(real_red_tuple))

            for blue in blue_combinations:
                hit_blue_count = len(set(blue) & set(real_blue_tuple))
                if hit_red_count == 5 and hit_blue_count == 2:
                    result['first'] += config['multiple']
                elif hit_red_count == 5 and hit_blue_count == 1:
                    result['second'] += config['multiple']
                elif hit_red_count == 5 and hit_blue_count == 0:
                    result['third'] += config['multiple']
                elif hit_red_count == 4 and hit_blue_count == 2:
                    result['fourth'] += config['multiple']
                elif hit_red_count == 4 and hit_blue_count == 1:
                    result['fifth'] += config['multiple']
                elif hit_red_count == 3 and hit_blue_count == 2:
                    result['sixth'] += config['multiple']
                elif hit_red_count == 4 and hit_blue_count == 0:
                    result['seventh'] += config['multiple']
                elif (hit_red_count == 3 and hit_blue_count == 1) or (hit_red_count == 2 and hit_blue_count == 2):
                    result['eighth'] += config['multiple']
                elif hit_red_count == 3 or (hit_red_count == 1 and hit_blue_count == 2) or (
                        hit_red_count == 2 and hit_blue_count == 1):
                    result['ninth'] += config['multiple']
        return result

    @staticmethod
    def get_tuple_by_str(num):
        """
        将配置里的字符串转换为tuple并返回，方便程序进行下一步处理
        :param num: 原始字符串
        :return:
        """
        red_str, blue_str = num.split('@')
        red_tuple = tuple(red_str.split(','))
        blue_tuple = tuple(blue_str.split(','))
        return red_tuple, blue_tuple

    @staticmethod
    def get_prize_name_by_prize(prize):
        """
        返回英文对应的中文奖项
        :param prize:
        :return:
        """
        prize_name_map = {
            'first': '一等奖',
            'second': '二等奖',
            'third': '三等奖',
            'fourth': '四等奖',
            'fifth': '五等奖',
            'sixth': '六等奖',
            'seventh': '七等奖',
            'eighth': '八等奖',
            'ninth': '九等奖',
        }
        return prize_name_map[prize] if prize in prize_name_map else ''


class DayError(ValueError):
    pass
