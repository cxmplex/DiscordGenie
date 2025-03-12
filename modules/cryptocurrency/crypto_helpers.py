
import json
import time

from modules.aws_lambda import aws


def get_message(info):
    message = '```{}\n{}:\nUSD: {}\nBTC: {}\n1 Hour Change: {}%\n24 Hour Change: {}%\n7 Day Change: {}%\n```'.format(
        time.ctime(),
        info['message'][0]['name'],
        info['message'][0]['price_usd'],
        info['message'][0]['price_btc'],
        info['message'][0]['percent_change_1h'],
        info['message'][0]['percent_change_24h'],
        info['message'][0]['percent_change_7d'])
    return message


def get_info(request):
    info = json.loads(aws.process("crypto", request))
    if 'error' in info['message']:
        return 0
    return info


def get_coin_list():
    info = json.loads(aws.process("coin", "coin"))
    return info
