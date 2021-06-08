from keygen.crypto_coin import CryptoCoin
from keygen.crypto_coin_service import CoinService

from bip_utils import BitcoinConf, Bip44Coins, WifDecoder, Bip44, Base58Encoder, Bip39MnemonicGenerator, \
    Bip39SeedGenerator, Base58Decoder
from bip_utils.utils import CryptoUtils, KeyUtils

from keygen.wif_validator import is_compressed_wif
import binascii


class EthCoinService(CoinService):

    def generate(self):
        # Generate random mnemonic
        mnemonic = Bip39MnemonicGenerator.FromWordsNumber(12)

        # Generate seed from mnemonic
        seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

        # Generate BIP44 master keys
        bip_obj_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)

        address = bip_obj_mst.PublicKey().ToAddress()
        wif = bip_obj_mst.PrivateKey().Raw().ToHex()
        seed = mnemonic

        return CryptoCoin(address, wif, seed)

    def get_coin(self, private_key):
        private_key_bytes = binascii.unhexlify(private_key)
        key_pair = Bip44.FromAddressPrivKey(private_key_bytes, Bip44Coins.ETHEREUM)
        address = key_pair.PublicKey().ToAddress()
        return CryptoCoin(address, private_key)
