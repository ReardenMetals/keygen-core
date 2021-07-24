from keygen.crypto_coin_service import CoinService
from keygen.currencies.btc_crypto_coin_service import BtcCoinService
from keygen.currencies.bch_crypto_coin_service import BchCoinService
from keygen.currencies.ltc_crypto_coin_service import LtcCoinService
from keygen.currencies.eth_crypto_coin_service import EthCoinService
from keygen.currencies.doge_crypto_coin_service import DogeCoinService

import inspect


class CoinFactory:
    def __init__(self):
        self.coin_services_classes = self.__get_coin_service_classes()

    def get_available_currencies(self):
        return self.__get_default_available_currencies()

    def __get_default_available_currencies(self):
        return ['BTC', 'BCH', 'LTC', 'DOGE', 'ETH'] + \
               [coin_services_class.get_currency_name() for coin_services_class in self.coin_services_classes]

    def get_coin_service(self, currency):
        if currency == "BTC":
            return BtcCoinService()
        elif currency == "BCH":
            return BchCoinService()
        elif currency == "LTC":
            return LtcCoinService()
        elif currency == "ETH":
            return EthCoinService()
        elif currency == "DOGE":
            return DogeCoinService()
        else:
            return self.__get_discovered_coin_service(currency)

    def __get_discovered_coin_service(self, currency):
        coin_services_dictionary = dict(
            (service.get_currency_name(), service) for service in self.coin_services_classes)
        if currency in coin_services_dictionary:
            return coin_services_dictionary.get(currency)()
        else:
            raise Exception("Coin not supported")

    @staticmethod
    def __get_coin_service_classes():
        try:
            plugins_module = __import__("plugins")
            classes_member_list = [member for member in dir(plugins_module)
                                   if inspect.isclass(getattr(plugins_module, member))]
            classes_list = [getattr(plugins_module, class_member) for class_member in classes_member_list]
            return [clazz for clazz in classes_list if issubclass(clazz, CoinService) and clazz != CoinService]
        except ModuleNotFoundError:
            return []
