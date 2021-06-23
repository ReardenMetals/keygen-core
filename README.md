# Keygen Core module for generating crypto wallets

## Install keygen-core module:

Required Python version 3.8 (preferred Python 3.8.6)

Download archive with the latest release of "Source Code (zip)" for Windows based system or "Source Code (tar.gz)" for Unix based system
https://github.com/ReardenMetals/keygen-core/releases

Run the python scipt to test the the keypair generation:
python main.py

## Keygen code structure

### CryptoCoin class
This data-class is located in keygen/crypto_coin.py, which has three fields
- address (Public address of coin)
- wif (Wallet import format of private key)
- seed (Mnemonic security phrase)

### CoinService class
This an abstract class is located in keygen/crypto_coin_service.py and needed as an abstraction for accessing to methods of keygen.
- generate: Generate new coin.
- generate_asset_id: Generate asset ID from Coin
- get_address_and_id: Get address and asset ID from private key
- get_address: Get address from private key (wif)
- get_coin: get coin structure from private key (wif)
- format: Preparing textual representation of coin
- get_csv_header: return header for csv

### Coin services implementation
Located in "keygen/currencies". Supported crypto currencies (services):
- BchCoinService
- BtcCoinService
- DogeCoinService
- EthCoinService
- LtcCoinService

### CoinFactory class
This class is located in keygen/crypto_coin_factory.py and needed to register (initiate) new crypto service:
Typical example of creating a service:


    service = CoinFactory.get_coin_service("BTC")
    coin = service.generate()

## Third party libraries integrated into Keygen-core.

### BIP utility library:
https://pypi.org/project/bip-utils/

This package contains an implementation of some BIP (Bitcoin Improvement Proposal) specifications, allowing to:

Generate a mnemonic string from a random entropy
Generate a secure seed from the mnemonic string
Use the seed to generate the master key of the wallet and derive the children keys, including address encoding
The implemented BIP specifications are the following:

* BIP-0039 for mnemonic and seed generation
* BIP-0032 for master key generation (from the secure seed) and children keys derivation
* BIP-0044, BIP-0049 and BIP-0084 for the hierarchy of deterministic wallets, based on BIP-0032 specification

### ECDSA Library:
https://pypi.org/project/ecdsa/

This is an easy-to-use implementation of ECC (Elliptic Curve Cryptography) with support for ECDSA (Elliptic Curve Digital Signature Algorithm) and ECDH (Elliptic Curve Diffie-Hellman), implemented purely in Python, released under the MIT license. With this library, you can quickly create keypairs (signing key and verifying key), sign messages, and verify the signatures. You can also agree on a shared secret key based on exchanged public keys. The keys and signatures are very short, making them easy to handle and incorporate into other protocols.

### SHA-3 wrapper (keccak) for Python
https://pypi.org/project/pysha3/

SHA-3 wrapper (keccak) for Python. The package is a wrapper around the optimized Keccak Code Package, https://github.com/gvanas/KeccakCodePackage .

The module is a standalone version of my SHA-3 module from Python 3.6 (currently under development). The code in sha3module.c has been modified to be compatible with Python 2.7 to 3.5. Python 2.6 and earlier are not supported.

### Six is a Python 2 and 3 compatibility library. 
https://pypi.org/project/six/

Six is a Python 2 and 3 compatibility library. It provides utility functions for smoothing over the differences between the Python versions with the goal of writing Python code that is compatible on both Python versions. See the documentation for more information on what is provided.
