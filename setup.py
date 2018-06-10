from src.blake2 import Blake2b, Blake2s
import hashlib

blake2b = Blake2b()
blake2s = Blake2s()

bb = hashlib.blake2b(b'', key=b'').hexdigest()
print(bb)

bb = hashlib.blake2s(b'', key=b'').hexdigest()
print(bb)

res = blake2b.getHash(b'', key=b'').hex()
print(res)

res = blake2s.getHash(b'', key=b'').hex()
print(res)
