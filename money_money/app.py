import asyncio
import logging

from aiohttp import web

from money_money.middlewares import middleware_logger
from money_money import MoneyMoneyService
from money_money.utils import parse_args, create_logger
from money_money.views import init_routes


def init_app() -> web.Application:
    logging.info('=========== Init app ===========')

    currencies, period, debug_mode = parse_args()
    create_logger(debug_mode)
    money_app = MoneyMoneyService(list(currencies.keys()), period)
    money_app.init_currencies(currencies)

    init_async_tasks(money_app)
    app = web.Application(
        client_max_size=10 ** 8,
        middlewares=[middleware_logger]
    )
    init_routes(app, money_app)

    return app


def start_server(port=8080):
    app = init_app()
    loop = asyncio.get_event_loop()
    web.run_app(app=app, port=port, loop=loop)


def init_async_tasks(money_app):
    loop = asyncio.get_event_loop()
    loop.create_task(money_app.update_currencies())
    loop.create_task(money_app.print_sums())
