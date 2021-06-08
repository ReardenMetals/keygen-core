
import sha3

k = sha3.keccak_256()
k.update('age'.encode("UTF-8"))
print(k.hexdigest())