import argparse
import logging
import sys


def parse_args():
    parser = argparse.ArgumentParser(prog='MoneyMoneyProgram')

    parser.add_argument('--period', type=float)
    parser.add_argument('--rub', type=float)
    parser.add_argument('--eur', type=float)
    parser.add_argument('--usd', type=float)
    parser.add_argument('--debug', default='False')
    args = parser.parse_args()

    currencies = {}
    debug_mode = False
    period = None
    for arg_name, arg_value in args.__dict__.items():
        if arg_name == 'debug':
            if arg_value in ('1', 'True', 'true', 'y', 'Y'):
                debug_mode = True
            elif arg_value not in ('0', 'False', 'false', 'n', 'N'):
                raise ValueError('invalid agrument: --debug')
        elif arg_name == 'period':
            period = arg_value
        else:
            currencies[arg_name] = arg_value

    return currencies, period, debug_mode


def create_logger(debug=False):
    debug_lvl = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(encoding='utf-8', level=debug_lvl, stream=sys.stdout)
    logging.Logger.manager.getLogger('aiohttp.access').setLevel(logging.ERROR)
