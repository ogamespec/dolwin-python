from random import randint

def do_command(dolwin, args):
    print ("PackBitsTest:")

    res = 0
    test = 0

    for bit in range(32):
        bitValue = randint(0, 1)
        print ("Bit %d: %d" % (bit, bitValue))
        res = __PackBits (res, bit, bit, bitValue)
        test |= bitValue << (31 - bit)
        print ("res: 0x%08X, test: 0x%08X" % (res, test))
        if res != test:
            raise Exception ("Bit PackBitsTest failed!")

    res = 0
    test = 0

    for nibble in range(8):
        nibbleValue = randint(0, 0xf)
        print ("Nibble %d: 0x%x" % (nibble, nibbleValue))
        res = __PackBits (res, nibble * 4, nibble * 4 + 3, nibbleValue)
        test |= nibbleValue << (28 - nibble * 4)
        print ("res: 0x%08X, test: 0x%08X" % (res, test))
        if res != test:
            raise Exception ("Nibble PackBitsTest failed!")

    print ("PackBitsTest success!\n")


def __PackBits(res, a, b, val):
    if a > 31 or b > 31:
        raise Exception ("Bit out of range")
    if b < a:
        raise Exception ("Wrong bit order")
    bits = b - a + 1
    maxVal = 1 << bits
    if val >= maxVal:
        raise Exception ("Value out of range")
    mask = 0
    if b >= 31:
        mask = (0xffffffff >> a) ^ 0
    else:
        mask = (0xffffffff >> a) ^ (0xffffffff >> (b + 1))
    return (res & ~mask) | (val << (31 - b));
