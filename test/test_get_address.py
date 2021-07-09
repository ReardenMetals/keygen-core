from keygen.crypto_coin_factory import CoinFactory


def get_coin_address(currency, private_key):
    service = CoinFactory().get_coin_service(currency)
    return service.get_address(private_key)


def test_get_address_btc():
    address = get_coin_address('BTC', 'L2H1WVjswTKz8USEvyii8aSt5ZNMjMkHT6A9QVg8CTQ4NUBCQikS')
    assert '1K7u7cEfBpzvHAeZpNiJddpxeyt568z12p' == address


def test_get_address_bch():
    address = get_coin_address('BCH', 'L3XNnhynz1DZqbfvuiqy3WvJKX4HfJ7KQN1LMVqxgLefNf2zveNT')
    assert 'qrxhc3x952fms33x9r6pfva0vfhngjv9gq8paeyng9' == address


def test_get_address_ltc():
    address = get_coin_address('LTC', 'T3FkAhWcCx3sSks3hyy1w3G7YGbWKQcFCdhqVLKb4yYPFVwnCwEY')
    assert 'LMMgK6N9xCq2Mdzmg8dHfba9ZFGSPi71y1' == address


def test_get_address_doge():
    address = get_coin_address('DOGE', 'QTQujDWgQ4eDLrLcvdGNnHzNg4zTpLBups7yJRic4sKhAdhtbrDa')
    assert 'D9rjjx7r4R4RW1a8EFGAJe4inEnhbvgXnK' == address


def test_get_address_eth():
    address = get_coin_address('ETH', 'f37a1cfe9b060f705cd9c27bade415a987a780015080b753219dedccca0c8a73')
    assert '0xa6d8f1e68dd33105b2932e34df2beac9f89a3340' == address
