# Copyright (c) 2020 Emanuele Bellocchia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# Imports
from bip_utils.bip.bip32_utils  import Bip32Utils
from bip_utils.bip.bip44_base   import Bip44Base, Bip44Coins
from bip_utils.conf             import *


class Bip49Const:
    """ Class container for BIP44 constants. """

    # Specification name
    SPEC_NAME = "BIP-0049"
    # Purpose
    PURPOSE   = Bip32Utils.HardenIndex(49)
    # Allowed coins
    ALLOWED_COINS = \
        [
            Bip44Coins.BITCOIN     , Bip44Coins.BITCOIN_TESTNET,
            Bip44Coins.BITCOIN_CASH, Bip44Coins.BITCOIN_CASH_TESTNET,
            Bip44Coins.BITCOIN_SV  , Bip44Coins.BITCOIN_SV_TESTNET,
            Bip44Coins.LITECOIN    , Bip44Coins.LITECOIN_TESTNET,
            Bip44Coins.DOGECOIN    , Bip44Coins.DOGECOIN_TESTNET,
            Bip44Coins.DASH        , Bip44Coins.DASH_TESTNET,
            Bip44Coins.ZCASH       , Bip44Coins.ZCASH_TESTNET,
        ]
    # Map from Bip44Coins to coin classes
    COIN_TO_CLASS = \
        {
            Bip44Coins.BITCOIN              : Bip49BitcoinMainNet,
            Bip44Coins.BITCOIN_TESTNET      : Bip49BitcoinTestNet,
            Bip44Coins.BITCOIN_CASH         : Bip49BitcoinCashMainNet,
            Bip44Coins.BITCOIN_CASH_TESTNET : Bip49BitcoinCashTestNet,
            Bip44Coins.BITCOIN_SV           : Bip49BitcoinSvMainNet,
            Bip44Coins.BITCOIN_SV_TESTNET   : Bip49BitcoinSvTestNet,
            Bip44Coins.LITECOIN             : Bip49LitecoinMainNet,
            Bip44Coins.LITECOIN_TESTNET     : Bip49LitecoinTestNet,
            Bip44Coins.DOGECOIN             : Bip49DogecoinMainNet,
            Bip44Coins.DOGECOIN_TESTNET     : Bip49DogecoinTestNet,
            Bip44Coins.DASH                 : Bip49DashMainNet,
            Bip44Coins.DASH_TESTNET         : Bip49DashTestNet,
            Bip44Coins.ZCASH                : Bip49ZcashMainNet,
            Bip44Coins.ZCASH_TESTNET        : Bip49ZcashTestNet,
        }


class Bip49(Bip44Base):
    """ BIP49 class. It allows master key generation and children keys derivation in according to BIP-0049.
    BIP-0049 specifications: https://github.com/bitcoin/bips/blob/master/bip-0049.mediawiki
    """

    #
    # Override methods
    #

    def Purpose(self):
        """ Derive a child key from the purpose and return a new Bip object (e.g. BIP44, BIP49, BIP84).
        It calls the underlying _PurposeGeneric method with the current object as parameter.

        Returns:
            Bip49 object: Bip49 object

        Raises:
            Bip44DepthError: If current depth is not suitable for deriving keys
            Bip32KeyError: If the derivation results in an invalid key
        """
        return self._PurposeGeneric(self)

    def Coin(self):
        """ Derive a child key from the coin type specified at construction and return a new Bip object (e.g. BIP44, BIP49, BIP84).
        It calls the underlying _CoinGeneric method with the current object as parameter.

        Returns:
            Bip49 object: Bip49 object

        Raises:
            Bip44DepthError: If current depth is not suitable for deriving keys
            Bip32KeyError: If the derivation results in an invalid key
        """
        return self._CoinGeneric(self)

    def Account(self, acc_idx):
        """ Derive a child key from the specified account index and return a new Bip object (e.g. BIP44, BIP49, BIP84).
        It calls the underlying _AccountGeneric method with the current object as parameter.

        Args:
            acc_idx (int): Account index

        Returns:
            Bip49 object: Bip49 object

        Raises:
            Bip44DepthError: If current depth is not suitable for deriving keys
            Bip32KeyError: If the derivation results in an invalid key
        """
        return self._AccountGeneric(self, acc_idx)

    def Change(self, change_idx):
        """ Derive a child key from the specified account index and return a new Bip object (e.g. BIP44, BIP49, BIP84).
        It calls the underlying _ChangeGeneric method with the current object as parameter.

        Args:
            change_idx (Bip44Changes): Change index, must a Bip44Changes enum

        Returns:
            Bip49 object: Bip49 object

        Raises:
            TypeError: If chain index is not a Bip44Changes enum
            Bip44DepthError: If current depth is not suitable for deriving keys
            Bip32KeyError: If the derivation results in an invalid key
        """
        return self._ChangeGeneric(self, change_idx)

    def AddressIndex(self, addr_idx):
        """ Derive a child key from the specified account index and return a new Bip object (e.g. BIP44, BIP49, BIP84).
        It calls the underlying _AddressIndexGeneric method with the current object as parameter.

        Args:
            addr_idx (int): Address index

        Returns:
            Bip49 object: Bip49 object

        Raises:
            Bip44DepthError: If current depth is not suitable for deriving keys
            Bip32KeyError: If the derivation results in an invalid key
        """
        return self._AddressIndexGeneric(self, addr_idx)

    @staticmethod
    def SpecName():
        """ Get specification name.

        Returns:
            str: Specification name
        """
        return Bip49Const.SPEC_NAME

    @staticmethod
    def IsCoinAllowed(coin_type):
        """ Get if the specified coin is allowed.

        Args:
            coin_type (Bip44Coins): Coin type, must be a Bip44Coins enum

        Returns :
            bool: True if allowed, false otherwise

        Raises:
            TypeError: If coin_type is not of Bip44Coins enum
        """
        if not isinstance(coin_type, Bip44Coins):
            raise TypeError("Coin is not an enumerative of Bip44Coins")

        return coin_type in Bip49Const.ALLOWED_COINS

    @staticmethod
    def _GetPurpose():
        """ Get purpose.

        Returns:
            int: Purpose index
        """
        return Bip49Const.PURPOSE

    @staticmethod
    def _GetCoinClass(coin_type):
        """ Get coin class.

        Args:
            coin_type (Bip44Coins): Coin type, must be a Bip44Coins enum

        Returns:
            BipCoinBase child object: BipCoinBase child object
        """
        return Bip49Const.COIN_TO_CLASS[coin_type]
