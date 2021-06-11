# keygen-core

## BIP utility library:
https://pypi.org/project/bip-utils/

This package contains an implementation of some BIP (Bitcoin Improvement Proposal) specifications, allowing to:

Generate a mnemonic string from a random entropy
Generate a secure seed from the mnemonic string
Use the seed to generate the master key of the wallet and derive the children keys, including address encoding
The implemented BIP specifications are the following:

* BIP-0039 for mnemonic and seed generation
* BIP-0032 for master key generation (from the secure seed) and children keys derivation
* BIP-0044, BIP-0049 and BIP-0084 for the hierarchy of deterministic wallets, based on BIP-0032 specification

## ECDSA Library:
https://pypi.org/project/ecdsa/

This is an easy-to-use implementation of ECC (Elliptic Curve Cryptography) with support for ECDSA (Elliptic Curve Digital Signature Algorithm) and ECDH (Elliptic Curve Diffie-Hellman), implemented purely in Python, released under the MIT license. With this library, you can quickly create keypairs (signing key and verifying key), sign messages, and verify the signatures. You can also agree on a shared secret key based on exchanged public keys. The keys and signatures are very short, making them easy to handle and incorporate into other protocols.

## SHA-3 wrapper (keccak) for Python
https://pypi.org/project/pysha3/

SHA-3 wrapper (keccak) for Python. The package is a wrapper around the optimized Keccak Code Package, https://github.com/gvanas/KeccakCodePackage .

The module is a standalone version of my SHA-3 module from Python 3.6 (currently under development). The code in sha3module.c has been modified to be compatible with Python 2.7 to 3.5. Python 2.6 and earlier are not supported.
