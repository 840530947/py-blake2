class Helper:
    @staticmethod
    def rotate(number, d, size, bytes):
        return (number >> d) | (number << int(bytes - d)) & size

    @staticmethod
    def high(number, d):
        return number >> d

    @staticmethod
    def low(number, d):
        return number & ((1 << d) - 1)

