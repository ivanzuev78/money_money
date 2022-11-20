import asyncio
import logging
import sys
from itertools import permutations
from typing import Dict, List, Union

import requests

from .base_class import AbstractMoneyMoneyService


class MoneyMoneyService(AbstractMoneyMoneyService):

    def __init__(self, currencies: List[str], period: int):
        self.__currencies = currencies
        self.__period = period * 60
        self.__currency_amounts: Dict[str, float] = {currency: 0 for currency in self.__currencies}
        self.__exchange_rates: Dict[str, float] = {}

        self.__cbr_url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        self._main_currency = 'rub'
        self.__exchange_rates[self._main_currency] = 1
        self.__info_is_outdated = False

        self.__currencies_pairs = []
        for cur_from, cur_to in permutations(self.currencies, 2):
            if cur_to == self._main_currency:
                continue
            if (cur_to, cur_from) not in self.__currencies_pairs:
                self.__currencies_pairs.append((cur_from, cur_to))


    @property
    def _all_rates_exists(self):
        return all(self.__exchange_rates.get(currency) for currency in self.currencies)

    @property
    def currencies(self):
        return self.__currencies

    async def update_currencies(self):
        while True:
            await asyncio.gather(
                self._update_cbr_data(),
                asyncio.sleep(self.__period),
            )

    async def print_sums(self):
        while True:
            sleep_future = asyncio.ensure_future(asyncio.sleep(60))
            if self.__info_is_outdated and self._all_rates_exists:
                sys.stdout.write(self.get_total_currency_amounts_text() + '\n')
                self.__info_is_outdated = False
            await sleep_future

    def set_exchange_rate(self, currency, value):
        if self.__exchange_rates.get(currency) != value:
            logging.debug(f'Exchange ratio "{currency}" updated to {value}')
            self.__exchange_rates[currency] = value
            self.__info_is_outdated = True

    def get_exchange_rate(self, currency_from, currency_to):
        if currency_from == self._main_currency:
            return self.__exchange_rates.get(currency_to)

        else:
            from_rub = self.__exchange_rates.get(currency_from)
            rub_to = self.__exchange_rates.get(currency_to)
            return rub_to / from_rub if from_rub and rub_to else None

    async def _update_cbr_data(self):
        try:
            logging.debug(f'requesting exchange ratio data to {self.__cbr_url}')
            cbr_response = requests.get(self.__cbr_url)
        except requests.exceptions.ConnectionError:
            logging.error(f'Failed to connect {self.__cbr_url}')
            return

        if cbr_response.status_code == 200:
            data = cbr_response.json()
            for currency in self.__currencies:
                cur_upper = currency.upper()
                if cur_upper in data['Valute']:
                    value = data['Valute'][cur_upper]['Value']
                    self.set_exchange_rate(currency, value)

                elif currency != self._main_currency:
                    logging.warning(f'requested currency "{currency}" not in CBR data')

        else:
            logging.error(f'response code not 200 while request: {self.__cbr_url}')

    def get_currency_amount(self, currency):
        if currency in self.currencies:
            return self.__currency_amounts[currency]
        logging.warning(f'Trying to get non tracked currency: {currency}')

    def set_currency_amount(self, currency: str, value: Union[int, float]):
        if currency in self.currencies and self.__currency_amounts[currency] != value:
            self.__info_is_outdated = True
            self.__currency_amounts[currency] = float(value)
            return
        logging.warning(f'Trying to set non tracked currency: {currency}')

    def modify_currency_amount(self, currency: str, value: float):
        if currency in self.currencies and self.__currency_amounts[currency] != value:
            self.__info_is_outdated = True
            self.__currency_amounts[currency] += value
            return
        logging.warning(f'Trying to set non tracked currency: {currency}')

    def init_currencies(self, currencies: Dict[str, float]):
        logging.debug(f'init currencies: {currencies}')
        for currency, value in currencies.items():
            if currency in self.__currency_amounts:
                self.set_currency_amount(currency, value)
            else:
                logging.warning(f'Trying to set non tracked currency: {currency}')

    def get_total_currency_amount(self, currency_to_convert):
        total = 0
        for currency, amounts in self.__currency_amounts.items():
            rate = self.get_exchange_rate(currency_to_convert, currency)
            if rate:
                total += amounts * rate
        return round(total, 2)

    def get_total_currency_amounts_text(self):
        text_amount = '\n'.join(f'{cur}: {val}' for cur, val in self.__currency_amounts.items())
        text_exchange_rate = ''
        for cur_1, cur_2 in self.__currencies_pairs:
            text_exchange_rate += f'\n{cur_1}-{cur_2}: {self.get_exchange_rate(cur_1, cur_2)}'

        amounts = map(self.get_total_currency_amount, self.currencies)
        text_total = '\nsum: ' + ' / '.join([f'{amount or "-"} {cur}' for amount, cur in zip(amounts, self.currencies)])
        return '\n'.join([text_amount, text_exchange_rate, text_total])