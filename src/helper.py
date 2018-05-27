class Helper:
    @staticmethod
    def rotate(number, d):
        return (number >> d) | (number << (64 - d)) & 0xFFFFFFFF

    @staticmethod
    def high(number, d):
        return number >> d

    @staticmethod
    def low(number, d):
        return number & ((1 << d) - 1)

