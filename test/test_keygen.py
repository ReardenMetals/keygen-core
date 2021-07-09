from keygen.crypto_coin_factory import CoinFactory


def generate(currency):
    coin = CoinFactory().get_coin_service(currency).generate()
    print('Coin currency: ', currency)
    print("Coin address: ", coin.address)
    print("Coin wif: ", coin.wif)
    return coin


def test_gen_btc():
    coin = generate('BTC')
    assert coin.address is not None
    assert coin.wif is not None


def test_gen_bch():
    coin = generate('BCH')
    assert coin.address is not None
    assert coin.wif is not None


def test_gen_ltc():
    coin = generate('LTC')
    assert coin.address is not None
    assert coin.wif is not None


def test_gen_doge():
    coin = generate('DOGE')
    assert coin.address is not None
    assert coin.wif is not None


def test_gen_eth():
    coin = generate('ETH')
    assert coin.address is not None
    assert coin.wif is not None
