import pytest

from money_money.money_class import MoneyMoneyService


@pytest.fixture
def money_service():
    currencies = ['rub', 'eur', 'usd']
    service = MoneyMoneyService(currencies, 10)

    yield service


def test_init_currencies(money_service):
    currencies = {'rub': 100, 'eur': 200, 'usd': 300}

    for currency, value in currencies.items():
        money_service.set_currency_amount(currency, value)
        assert money_service.get_currency_amount(currency) == value


def test_modify_currencies(money_service):
    money_service.set_currency_amount('rub', 100)
    money_service.modify_currency_amount('rub', 50)
    assert money_service.get_currency_amount('rub') == 150


def test_exchange_rate(money_service):
    money_service.set_exchange_rate('usd', 60)
    money_service.set_exchange_rate('eur', 70)

    assert money_service.get_exchange_rate('usd', 'eur') == 70 / 60
    assert money_service.get_exchange_rate('rub', 'rub') == 1


def test_get_total_currency_amount(money_service):
    currencies = {'rub': 100, 'eur': 200, 'usd': 300}

    for currency, value in currencies.items():
        money_service.set_currency_amount(currency, value)

    money_service.set_exchange_rate('usd', 60)
    money_service.set_exchange_rate('eur', 70)

    assert money_service.get_total_currency_amount('rub') == round(100 + 200 * 70 + 300 * 60, 2)
    assert money_service.get_total_currency_amount('eur') == round(100 / 70 + 200 + 300 * 60 / 70, 2)
