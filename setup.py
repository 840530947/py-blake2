from blake2 import Blake2b

blake = Blake2b()

print(blake.getHash("hello world", "key"))