from keygen.crypto_coin_factory import CoinFactory


def test_coin(currency, private_key, address):
    service = CoinFactory.get_coin_service(currency)
    gen_address = service.get_address(private_key)
    assert gen_address == address


def test(currency, private_key, address, title):
    print("Checking {}, {}...".format(title, private_key))
    test_coin(currency, private_key, address)
    print(currency + " Success")

# 1. ETH

# '0x2786dA53108E93B7e539e0284C1466b8B7b88125', wif='1fa6d1d608224ee70cef46369f8ff24d08993d25ca3290c5ae5a1a512bba74a8',

# test('ETH', '1fa6d1d608224ee70cef46369f8ff24d08993d25ca3290c5ae5a1a512bba74a8',
#      '0x2786dA53108E93B7e539e0284C1466b8B7b88125', 'ETH')

test('ETH', 'bb0d723177603b46d3ba5b4aad018b83bd3cf7afc128274948655f2036549858',
     '0xd3af1fdfae6a9871c06b90e23193b3785bd2390a', 'ETH')

test('ETH', 'c2afb46249f70cd011cf594e29af09cebd3fa2570774d80d54447f7440031921',
     '0x6f2a619733dcc8ee9c53766bd906b5985ab274e2', 'ETH (OLD)')

print("Final success")
