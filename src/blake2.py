from src.helper import Helper
from functools import reduce


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

        self.sigma = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            [14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3],
            [11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6, 7, 1, 9, 4],
            [7, 9, 3, 1, 13, 12, 11, 14, 2, 6, 5, 10, 4, 0, 15, 8],
            [9, 0, 5, 7, 2, 4, 10, 15, 14, 1, 11, 12, 6, 8, 3, 13],
            [2, 12, 6, 10, 0, 11, 8, 3, 4, 13, 7, 5, 15, 14, 1, 9],
            [12, 5, 1, 15, 14, 13, 4, 10, 0, 7, 6, 3, 9, 2, 8, 11],
            [13, 11, 7, 14, 12, 1, 3, 9, 5, 0, 15, 4, 8, 6, 2, 10],
            [6, 15, 14, 9, 11, 3, 0, 8, 12, 2, 13, 7, 1, 4, 10, 5],
            [10, 2, 8, 4, 7, 6, 1, 5, 15, 11, 9, 14, 3, 12, 13, 0],
        ]

        self.blocksize = 128
        self.intsize = (1 << 64) - 1

    def getHash(self, message, key=None, hashlen=64):
        state = self.initvector[:]

        message = bytearray(message)

        keylen = 0
        if key is not None:
            key = bytearray(key[:64])
            keylen = len(key)

        state[0] ^= 0x01010000 | (keylen << 8) | hashlen

        compressed = 0
        remaining = len(message)

        if keylen > 0:
            message = key + bytearray([0 for _ in range(self.blocksize - keylen)]) + message
            remaining += self.blocksize

        i = 0
        while remaining > self.blocksize:
            block = message[(i * self.blocksize):((i + 1) * self.blocksize)]
            compressed += self.blocksize
            remaining -= self.blocksize
            state = self.compress(state, block, compressed)
            i += 1

        block = message[(i * self.blocksize):]
        compressed += remaining
        block = block + bytearray([0 for _ in range(self.blocksize - len(block))])

        state = reduce(
            lambda x, y: x + y.to_bytes(8, byteorder='little'),
            self.compress(state, block, compressed, True),
            bytearray()
        )

        return state[:hashlen]

    def compress(self, statevector, block, count, last=False):
        workvec = statevector[:] + self.initvector[:]

        workvec[12] ^= Helper.low(count, int(self.blocksize / 2))
        workvec[13] ^= Helper.high(count, int(self.blocksize / 2))

        if last:
            workvec[14] ^= self.intsize

        messages = [int.from_bytes(block[i:i + 8], byteorder='little') for i in range(0, len(block), 8)]

        for i in range(12):
            schedule = self.sigma[i % 10]

            workvec = self.mix(workvec, [0, 4, 8, 12], [messages[schedule[0]], messages[schedule[1]]])
            workvec = self.mix(workvec, [1, 5, 9, 13], [messages[schedule[2]], messages[schedule[3]]])
            workvec = self.mix(workvec, [2, 6, 10, 14], [messages[schedule[4]], messages[schedule[5]]])
            workvec = self.mix(workvec, [3, 7, 11, 15], [messages[schedule[6]], messages[schedule[7]]])

            workvec = self.mix(workvec, [0, 5, 10, 15], [messages[schedule[8]], messages[schedule[9]]])
            workvec = self.mix(workvec, [1, 6, 11, 12], [messages[schedule[10]], messages[schedule[11]]])
            workvec = self.mix(workvec, [2, 7, 8, 13], [messages[schedule[12]], messages[schedule[13]]])
            workvec = self.mix(workvec, [3, 4, 9, 14], [messages[schedule[14]], messages[schedule[15]]])

        return [statevector[i] ^ workvec[i + 8] ^ workvec[i] for i in range(8)]

    def mix(self, v, i, m):
        r = v[:]
        t = self.intsize

        r[i[0]] = (r[i[0]] + r[i[1]] + m[0]) & t
        r[i[3]] = Helper.rotate(r[i[3]] ^ r[i[0]], 32, t) & t
        r[i[2]] = (r[i[2]] + r[i[3]]) & t
        r[i[1]] = Helper.rotate(r[i[1]] ^ r[i[2]], 24, t) & t

        r[i[0]] = (r[i[0]] + r[i[1]] + m[1]) & t
        r[i[3]] = Helper.rotate(r[i[3]] ^ r[i[0]], 16, t) & t
        r[i[2]] = (r[i[2]] + r[i[3]]) & t
        r[i[1]] = Helper.rotate(r[i[1]] ^ r[i[2]], 63, t) & t
        return r


