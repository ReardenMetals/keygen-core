from keygen.crypto_coin_factory import CoinFactory


def default_input(message, default_val):
    if default_val:
        return input("%s [%s] : " % (message, default_val)) or default_val
    else:
        return input("%s " % message)


def main():
    currency = default_input("What crypto you making (BTC, ETH, ...)? ", "BTC").upper()
    service = CoinFactory().get_coin_service(currency)
    coin = service.generate()
    print("Currency: {}".format(currency))
    print("Address: {}".format(coin.address))
    print("Wif: {}".format(coin.wif))
    print("Seed: {}".format(coin.seed))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
