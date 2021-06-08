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
import os
from enum                   import IntEnum, unique
from bip_utils.bip.bip39_ex import Bip39InvalidFileError, Bip39ChecksumError
from bip_utils.utils        import AlgoUtils, ConvUtils, CryptoUtils


@unique
class Bip39WordsNum(IntEnum):
    """ Enumerative for BIP-0039 words number. """

    WORDS_NUM_12 = 12,
    WORDS_NUM_15 = 15,
    WORDS_NUM_18 = 18,
    WORDS_NUM_21 = 21,
    WORDS_NUM_24 = 24,


@unique
class Bip39EntropyBitLen(IntEnum):
    """ Enumerative for BIP-0039 entropy bit lengths. """

    BIT_LEN_128 = 128,
    BIT_LEN_160 = 160,
    BIT_LEN_192 = 192,
    BIT_LEN_224 = 224,
    BIT_LEN_256 = 256,


class Bip39Const:
    """ Class container for BIP39 constants. """

    # Accepted entropy lenghts in bit
    ENTROPY_BIT_LEN    = \
        [
            Bip39EntropyBitLen.BIT_LEN_128,
            Bip39EntropyBitLen.BIT_LEN_160,
            Bip39EntropyBitLen.BIT_LEN_192,
            Bip39EntropyBitLen.BIT_LEN_224,
            Bip39EntropyBitLen.BIT_LEN_256,
        ]
    # Accepted mnemonic word lengths
    MNEMONIC_WORD_LEN  = \
        [
            Bip39WordsNum.WORDS_NUM_12,
            Bip39WordsNum.WORDS_NUM_15,
            Bip39WordsNum.WORDS_NUM_18,
            Bip39WordsNum.WORDS_NUM_21,
            Bip39WordsNum.WORDS_NUM_24,
        ]

    # Total number of words
    WORDS_LIST_NUM     = 2048
    # Bits of a single word
    WORD_BITS          = 11

    # Salt modifier for seed generation
    SEED_SALT_MOD      = "mnemonic"
    # PBKDF2 round for seed generation
    SEED_PBKDF2_ROUNDS = 2048
    # Seed length
    SEED_LEN           = 64


class Bip39EntropyGenerator:
    """ Entropy generator class. It generates random entropy bytes with the specified length. """

    def __init__(self, bits_len):
        """ Construct class by specifying the bits length.

        Args:
            bits_len (int or Bip39EntropyBitLen): Entropy length in bits

        Raises:
            ValueError: If the bit length is not valid
        """
        if bits_len % 8 != 0:
            raise ValueError("Bit length not multiple of 8")

        self.m_bits_len = bits_len

    def Generate(self):
        """ Generate random entropy bytes with the length specified during construction.

        Returns:
            bytes: Generated entropy bytes
        """
        return os.urandom(self.m_bits_len // 8)


class MnemonicFileReader:
    """ Mnemonic file reader class. It reads the English BIP39 words list from a file """

    # File name constant
    FILE_NAME = "bip39_wordslist_en.txt"

    def __init__(self):
        """ Construct class by reading the words list from file.

        Raises:
            Bip39InvalidFileError: If loaded words list length is not 2048
        """

        # Read file
        file_path = os.path.join(os.path.dirname(__file__), self.FILE_NAME)
        with open(file_path, "r", encoding = "utf-8") as fin:
            self.m_words_list = [word.strip() for word in fin.readlines() if word.strip() != ""]

        # Check words list length
        if len(self.m_words_list) != Bip39Const.WORDS_LIST_NUM:
            raise Bip39InvalidFileError("Number of loaded words list (%d) is not valid" % len(self.m_words_list))

    def GetWordIdx(self, word):
        """ Get the index of the specified word, by searching it in the list.

        Args:
            word (str): Word to be searched

        Returns:
            int: Word index

        Raises:
            ValueError: If the word is not found
        """
        idx = AlgoUtils.BinarySearch(self.m_words_list, word)
        if idx == -1:
            raise ValueError("Word %s is not existent in word list" % word)

        return idx

    def GetWordAtIdx(self, word_idx):
        """ Get the word at the specified index.

        Args:
            word_idx (int): Word index

        Returns:
            str: Word at the specified index
        """
        return self.m_words_list[word_idx]


class Bip39MnemonicGenerator:
    """ BIP39 mnemonic generator class. It generates the mnemonic in according to BIP39.
    Mnemonic can be generated randomly or from a specified entropy.
    BIP-0039 specifications: https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
     """

    @staticmethod
    def FromWordsNumber(words_num):
        """ Generate mnemonic with the specified words number from random entropy.

        Args:
            words_num (int or Bip39WordsNum): Number of words (12, 15, 18, 21, 24)

        Returns:
            str: Generated mnemonic from random entropy

        Raises:
            ValueError: If words number is not valid
        """

        # Check words number
        if words_num not in Bip39Const.MNEMONIC_WORD_LEN:
            raise ValueError("Words number for mnemonic (%d) is not valid" % words_num)

        # Get entropy length in bit from words number
        entropy_bit_len = Bip39MnemonicGenerator.__EntropyBitLenFromWordsNum(words_num)
        # Generate entropy
        entropy_bytes = Bip39EntropyGenerator(entropy_bit_len).Generate()

        return Bip39MnemonicGenerator.FromEntropy(entropy_bytes)

    @staticmethod
    def FromEntropy(entropy_bytes):
        """ Generate mnemonic from the specified entropy bytes.

        Args:
            entropy_bytes (bytes): Entropy bytes (accepted lengths in bits: 128, 160, 192, 224, 256)

        Returns:
            str: Generated mnemonic from specified entropy

        Raises:
            ValueError: If entropy length is not valid
        """

        # Check entropy lenght in bits
        entropy_bit_len = len(entropy_bytes) * 8
        if entropy_bit_len not in Bip39Const.ENTROPY_BIT_LEN:
            raise ValueError("Entropy length in bits (%d) is not valid" % entropy_bit_len)

        # Compute entropy hash
        entropy_hash_bytes = CryptoUtils.Sha256(entropy_bytes)

        # Convert entropy to binary string
        entropy_bin = ConvUtils.BytesToBinaryStr(entropy_bytes, len(entropy_bytes) * 8)
        # Convert entropy hash to binary string
        entropy_hash_bin = ConvUtils.BytesToBinaryStr(entropy_hash_bytes, CryptoUtils.Sha256DigestSize() * 8)
        # Get checksum binary string
        checksum_bin = entropy_hash_bin[: len(entropy_bytes) // 4]

        # Create mnemonic entropy binary string by concatenating entropy and checksum, as specified in BIP39
        mnemonic_entropy_bin = entropy_bin + checksum_bin

        # Create mnemonic reader
        mnemonic_reader = MnemonicFileReader()

        # Empty mnemonic
        mnemonic = []

        # Get mnemonic from entropy
        for i in range(len(mnemonic_entropy_bin) // Bip39Const.WORD_BITS):
            # Get current word index
            word_idx = int(mnemonic_entropy_bin[i * Bip39Const.WORD_BITS : (i + 1) * Bip39Const.WORD_BITS], 2)
            # Get word at given index
            mnemonic.append(mnemonic_reader.GetWordAtIdx(word_idx))

        # Join to string
        return " ".join(mnemonic)

    @staticmethod
    def __EntropyBitLenFromWordsNum(words_num):
        """ Get entropy length from words number.

        Args:
            words_num (int): Words numer

        Returns:
            int: Correspondent entropy length
        """
        return (words_num * Bip39Const.WORD_BITS) - (words_num // 3)


class Bip39MnemonicValidator:
    """ BIP39 mnemonic validator class. It validates a mnemonic string or list. """

    #
    # Public methods
    #

    def __init__(self, mnemonic):
        """ Construct the class from mnemonic.

        Args:
            mnemonic (str or list): Mnemonic
        """
        self.m_mnemonic = mnemonic

    def Validate(self):
        """ Validate the mnemonic specified at construction.

        Returns:
            bool: True if valid, False otherwise
        """

        # Get back mnemonic binary string
        try:
            mnemonic_bin = self.__GetMnemonicBinaryStr()
        except ValueError:
            return False

        # The computed checksum shall be equal to the existent one
        return self.__ComputeChecksum(mnemonic_bin) == self.__GetChecksum(mnemonic_bin)

    def GetEntropy(self):
        """Get entropy bytes from mnemonic.

        Returns:
            bytes: Entropy bytes corresponding to the mnemonic

        Raises:
            ValueError: If mnemonic is not valid
            Bip39ChecksumError: If checksum is not valid
        """

        # Get back mnemonic binary string
        mnemonic_bin = self.__GetMnemonicBinaryStr()

        checksum      = self.__GetChecksum(mnemonic_bin)
        comp_checksum = self.__ComputeChecksum(mnemonic_bin)

        # Verify checksum
        if checksum != comp_checksum:
            raise Bip39ChecksumError("Invalid checksum when getting entropy (expected %s, got %s" % (comp_checksum, checksum))

        # Get entropy bytes from binary string
        return self.__GetEntropyBytes(mnemonic_bin)

    #
    # Private methods
    #

    def __GetMnemonicBinaryStr(self):
        """ Get mnemonic binary string from mnemonic string or list.

        Returns:
           str: Mnemonic binary string

        Raises:
            ValueError: If mnemonic is not valid
        """

        # Split mnemonic string if needed
        mnemonic = self.m_mnemonic.split(" ") if not isinstance(self.m_mnemonic, list) else self.m_mnemonic

        # Check mnemonic length
        if len(mnemonic) not in Bip39Const.MNEMONIC_WORD_LEN:
            raise ValueError("Mnemonic length (%d) is not valid" % len(mnemonic))

        # Create reader
        mnemonic_reader = MnemonicFileReader()
        # Convert each word to its index in binary format
        mnemonic_bin = map(lambda word : ConvUtils.IntToBinaryStr(mnemonic_reader.GetWordIdx(word), Bip39Const.WORD_BITS), mnemonic)

        # Join the elements to get the complete binary string
        return "".join(mnemonic_bin)

    def __GetEntropyBytes(self, mnemonic_bin_str):
        """ Get entropy from mnemonic binary string.

        Args:
            mnemonic_bin_str (str): Mnemonic binary string

        Returns:
           bytes: Entropy bytes
        """

        # Get checksum length
        checksum_len = self.__GetChecksumLen(mnemonic_bin_str)
        # Get back entropy binary string
        entropy_bin = mnemonic_bin_str[:-checksum_len]

        # Get entropy bytes from binary string
        return ConvUtils.BytesFromBinaryStr(entropy_bin, checksum_len * 8)

    def __GetChecksum(self, mnemonic_bin_str):
        """ Get checksum from mnemonic binary string.

        Args:
            mnemonic_bin_str (str): Mnemonic binary string

        Returns:
           str: Checksum binary string
        """

        return mnemonic_bin_str[-self.__GetChecksumLen(mnemonic_bin_str):]

    def __ComputeChecksum(self, mnemonic_bin_str):
        """ Compute checksum from mnemonic binary string.

        Args:
            mnemonic_bin_str (str): Mnemonic binary string

        Returns:
           bytes: Computed checksum binary string
        """

        # Get entropy bytes
        entropy_bytes = self.__GetEntropyBytes(mnemonic_bin_str)
        # Convert entropy hash to binary string
        entropy_hash_bin = ConvUtils.BytesToBinaryStr(CryptoUtils.Sha256(entropy_bytes), CryptoUtils.Sha256DigestSize() * 8)

        # Compute checksum
        checksum_bin = entropy_hash_bin[:self.__GetChecksumLen(mnemonic_bin_str)]

        return checksum_bin

    @staticmethod
    def __GetChecksumLen(mnemonic_bin_str):
        """ Get checksum length from mnemonic binary string.

        Args:
            mnemonic_bin_str (str): Mnemonic binary string

        Returns:
           int: Checksum length
        """
        return len(mnemonic_bin_str) // 33


class Bip39SeedGenerator:
    """ BIP39 seed generator class. It generates the seed from a mnemonic in according to BIP39. """

    def __init__(self, mnemonic):
        """ Construct the class from a specified mnemonic.

        Args:
            mnemonic (str or list): Mnemonic

        Raises:
            ValueError: If the mnemonic is not valid
        """

        # Make sure that the given mnemonic is valid
        if not Bip39MnemonicValidator(mnemonic).Validate():
            raise ValueError("Invalid mnemonic (%s)" % mnemonic)

        self.m_mnemonic = mnemonic

    def Generate(self, passphrase = ""):
        """ Generate the seed using the specified passphrase.

        Args:
            passphrase (str, optional): Passphrase, empty if not specified

        Returns:
            bytes: Generated seed
        """

        # Get salt
        salt = Bip39Const.SEED_SALT_MOD + passphrase
        # Compute key
        key = CryptoUtils.Pbkdf2HmacSha512(AlgoUtils.StringEncode(self.m_mnemonic), AlgoUtils.StringEncode(salt), Bip39Const.SEED_PBKDF2_ROUNDS)

        return key[:Bip39Const.SEED_LEN]
