#-*- coding: utf-8 -*-

"""
    test
    ~~~~
    This file tests and compares avg runtime performance of summing
    the number of set bits within 1000, 16 bit 

    :authors Mek
"""

import math
from operator import attrgetter
from random import randint

def pad(n, bits=8):
    """Consumes the string representation of a binary number and
    prepends 0's until it's length is == to the number of bits
    specified by the bits argument
    """
    return ((bits - len(n)) * "0") + n

lookup = dict((pad(str(b), 8), b.count('1')) for b in \
                  map(lambda n: str(bin(n)[2:]), range(0, 256)))

def randbin(bits=16):
    return str(pad(bin(randint(0, (2**bits)-1))[2:], bits))

def chunk(s, size):
    """Yield successive n-sized chunks from str s."""
    if len(s) < size:
        return [s]
    return [s[i:i+size] for i in xrange(0, len(s), size)]

def setbits16(n, chunk_size=8):
    """Counts the number of set bits (the number of occurences of 1)
    within a 16-bit binary number. Uses a dict lookup table 
    """
    return sum(map(lambda x: lookup[x], chunk(n, chunk_size)))
                   
if __name__ == "__main__":
    nums = map(lambda x: randbin(16), xrange(1000))
    print lookup.keys()
    print sum(map(lambda n: setbits16(pad(n, 16)), nums))
