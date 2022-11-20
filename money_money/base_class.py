from abc import ABC, abstractmethod
from typing import Dict


class AbstractMoneyMoneyService(ABC):

    @abstractmethod
    async def update_currencies(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def currencies(self):
        raise NotImplementedError

    @abstractmethod
    async def _update_cbr_data(self):
        raise NotImplementedError

    @abstractmethod
    def get_currency_amount(self, currency: str):
        raise NotImplementedError

    @abstractmethod
    def set_currency_amount(self, currency: str, value: float):
        raise NotImplementedError

    def set_currency_amounts(self, currency_amounts: Dict[str, float]):
        for currency, amount in currency_amounts.items():
            self.set_currency_amount(currency, amount)

    @abstractmethod
    def modify_currency_amount(self, currency: str, value: float):
        raise NotImplementedError

    def modify_currency_amounts(self, currency_amounts: Dict[str, float]):
        for currency, amount in currency_amounts.items():
            self.modify_currency_amount(currency, amount)

    @abstractmethod
    def get_total_currency_amount(self, currency_to_convert: str):
        raise NotImplementedError

    @abstractmethod
    def get_total_currency_amounts_text(self):
        raise NotImplementedError
