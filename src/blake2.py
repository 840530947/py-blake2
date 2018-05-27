class Blake2b:

    def __init__(self):

        self.initvector = [
            0x6A09E667F3BCC908,
            0xBB67AE8584CAA73B,
            0x3C6EF372FE94F82B,
            0xA54FF53A5F1D36F1,
            0x510E527FADE682D1,
            0x9B05688C2B3E6C1F,
            0x1F83D9ABFB41BD6B,
            0x5BE0CD19137E2179
        ]

        self.blocksize = 128

    def getHash(self, input, key = None, hashlen = 64):
        state = self.initvector[:]
        keylen = len(key.encode()) if key is not None else 0

        state[0] ^= 0x01010000 | (keylen << 8) | hashlen

        compressed = 0
        remaining = len(input)

        if keylen > 0:
            input = key.ljust(self.blocksize, '\0') + input
            remaining += self.blocksize

        while remaining > self.blocksize:
            return

        return keylen

    def compress(self, statevector, block, count):
        workvec = statevector[:].extend(self.initvector[:])

        workvec[12] ^= self.low(count, self.blocksize / 2)
        workvec[13] ^= self.high(count, self.blocksize / 2)


        pass

    def mix(self, v, m):
        pass

    def r_rotate(self, number, d):
        return (number >> d) | (number << (64 - d)) & 0xFFFFFFFF

    def high(self, number, d):
        return number >> d

    def low(self, number, d):
        return number & ((1 << d) - 1)

