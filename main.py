# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from keygen.crypto_coin import CryptoCoin
from keygen.crypto_coin_service import CoinService

from keygen.crypto_coin_factory import CoinFactory

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def test_coin(currency):
    service = CoinFactory.get_coin_service(currency)
    coin = service.generate()
    print(currency)
    print(coin)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test_coin("BTC")
    test_coin("BCH")
    test_coin("LTC")
    test_coin("DOGE")
    test_coin("ETH")
