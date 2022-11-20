import logging

from aiohttp import web

from money_money.base_class import AbstractMoneyMoneyService
from money_money.validations import validate_data


def init_routes(app: web.Application, money_service: AbstractMoneyMoneyService):
    routes = web.RouteTableDef()

    @routes.get('/amount/get')
    async def get_amount(request):
        return web.Response(text=money_service.get_total_currency_amounts_text(),
                            headers={'content-type': 'text/plain'})

    @routes.post('/amount/set')
    async def set_amounts(request):
        data = await request.json()
        validate_successful, msg = validate_data(data)
        if validate_successful:
            # TODO Добавить проверку на совпадение поданных и отслеживаемых валют
            money_service.set_currency_amounts(data)
            return web.Response(text="Successful", headers={'content-type': 'text/plain'})

        logging.warning(msg)
        return web.Response(text=msg, headers={'content-type': 'text/plain'}, status=400)

    @routes.post('/modify')
    async def modify_amounts(request):
        data = await request.json()
        validate_successful, msg = validate_data(data)
        if validate_successful:
            # TODO Добавить проверку на совпадение поданных и отслеживаемых валют
            money_service.modify_currency_amounts(data)
            return web.Response(text="Successful", headers={'content-type': 'text/plain'})

        logging.warning(msg)
        return web.Response(text=msg, headers={'content-type': 'text/plain'}, status=400)

    @routes.get('/{currency}/get')
    async def variable_handler(request):
        currency = request.match_info['currency']
        amount = money_service.get_currency_amount(currency)
        if amount is not None:
            return web.Response(
                text="{}: {}".format(currency, amount), headers={'content-type': 'text/plain'})

        return web.Response(
            text="{} is not tracked".format(currency), headers={'content-type': 'text/plain'}, status=400)

    app.add_routes(routes)
