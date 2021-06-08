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
import binascii
from bip_utils.base58 import Base58Encoder
from bip_utils.bech32 import BchBech32Encoder
from bip_utils.conf   import BitcoinConf
from bip_utils.utils  import CryptoUtils, KeyUtils


class P2SHConst:
    """ Class container for P2SH constants. """

    # Script bytes
    SCRIPT_BYTES = b"0014"


class P2SHUtils:
    """ Class container for P2SH utility functions. """

    @staticmethod
    def AddScriptSig(pub_key_bytes):
        """ Add script signature to public key and get address bytes.

        Args:
            pub_key_bytes (bytes) : Public key bytes

        Returns:
            bytes: Address bytes
        """
        # Key hash: Hash160(public_key)
        key_hash = CryptoUtils.Hash160(pub_key_bytes)
        # Script signature: 0x0014 | Hash160(public_key)
        script_sig = binascii.unhexlify(P2SHConst.SCRIPT_BYTES) + key_hash
        # Address bytes = Hash160(script_signature)
        return CryptoUtils.Hash160(script_sig)


class P2SH:
    """ P2SH class. It allows the Pay-to-Script-Hash address generation. """

    @staticmethod
    def ToAddress(pub_key_bytes, net_addr_ver = BitcoinConf.P2SH_NET_VER.Main()):
        """ Get address in P2SH format.

        Args:
            pub_key_bytes (bytes)         : Public key bytes
            net_addr_ver (bytes, optional): Net address version, default is Bitcoin main network

        Returns:
            str: Address string

        Raises:
            ValueError: If the key is not a public compressed key
        """
        if not KeyUtils.IsPublicCompressed(pub_key_bytes):
            raise ValueError("Public compressed key is required for P2SH")

        # Final address: Base58Check(addr_prefix | address_bytes)
        return Base58Encoder.CheckEncode(net_addr_ver + P2SHUtils.AddScriptSig(pub_key_bytes))


class BchP2SH:
    """ Bitcoin Cash P2SH class. It allows the Bitcoin Cash P2SH generation. """

    @staticmethod
    def ToAddress(pub_key_bytes, hrp, net_addr_ver):
        """ Get address in Bitcoin Cash P2SH format.

        Args:
            pub_key_bytes (bytes): Public key bytes
            hrp (str)            : HRP
            net_addr_ver (int)   : Net address version

        Returns:
            str: Address string

        Raises:
            ValueError: If key is not a public compressed key
        """
        if not KeyUtils.IsPublicCompressed(pub_key_bytes):
            raise ValueError("Public compressed key is required for Bitcoin Cash")

        return BchBech32Encoder.Encode(hrp, net_addr_ver, P2SHUtils.AddScriptSig(pub_key_bytes))
