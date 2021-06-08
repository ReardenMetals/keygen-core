from keygen.currencies.btc_crypto_coin_service import BtcCoinService
from keygen.currencies.bch_crypto_coin_service import BchCoinService
from keygen.currencies.ltc_crypto_coin_service import LtcCoinService
from keygen.currencies.eth_crypto_coin_service import EthCoinService
from keygen.currencies.doge_crypto_coin_service import DogeCoinService


class CoinFactory:
    def __init__(self):
        pass

    @staticmethod
    def get_available_currencies():
        return CoinFactory.get_default_available_currencies()

    @staticmethod
    def get_default_available_currencies():
        return ['BTC', 'BCH', 'CLUB', 'DASH', 'LTC', 'ETH', 'BSV', 'DOGE', 'XRP', 'XMR', 'BNB', 'EOS', 'POTE', 'WAVES',
                'USDT', 'ADA']

    @staticmethod
    def get_coin_service(currency):
        if currency == "BTC":
            return BtcCoinService()
        if currency == "BCH":
            return BchCoinService()
        if currency == "LTC":
            return LtcCoinService()
        if currency == "ETH":
            return EthCoinService()
        if currency == "DOGE":
            return DogeCoinService()
        raise Exception("Coin not supported")
