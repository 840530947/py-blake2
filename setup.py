from src.blake2 import Blake2b
import hashlib

blake = Blake2b()

bb = hashlib.blake2b(b'input').hexdigest()
print(bb)

res = blake.getHash(b'input')
print(res)
