class Helper:
    @staticmethod
    def rotate(number, d, size):
        return (number >> d) | (number << (64 - d)) & size

    @staticmethod
    def high(number, d):
        return number >> d

    @staticmethod
    def low(number, d):
        return number & ((1 << d) - 1)

