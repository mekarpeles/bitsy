#-*- coding: utf-8 -*-

"""
    bitsy
    ~~~~~
    This file tests and compares avg runtime performance of summing
    the number of set bits within 1000, 16 bit numbers.

    :authors Mek
    :license GPLv3
"""

import math
from operator import attrgetter
from random import randint
import time, timeit
import argparse

def pad(n, bits=8):
    """Consumes the string representation of a binary number and
    prepends 0's until it's length is == to the number of bits
    specified by the bits argument

    Goal: Refactor to remove padding for performance increase

    >>> pad('1001', bits=8)
    '00001001'
    """
    return ((bits - len(n)) * "0") + n

def randbin(bits=16):
    """Generates a str representation of a random binary 'bits' length
    binary number.

    >>> randbin(bits=8)
    '10010111'
    """
    return str(pad(bin(randint(0, (2**bits)-1))[2:], bits))

def chunk(s, size):
    """Yield generator of successive n-sized chunks from str s.

    >>> chunk('10010111', 2)
    ['1001', '0111']
    """
    if len(s) < size:
        return [s]
    return (s[i:i+size] for i in xrange(0, len(s), size))

def hamming_weight(n):
    """Hamming weight algorithm provided by Brian Kernighan, Peter
    Wegner, Derrick Lehmer. Takes as integer value and returns the
    number of set bits required to represent the number.
    """
    c = 0
    while n > 0:
        n &= n - 1
        c += 1
    return c

def setbits(n, dictionary, chunk_size=8):
    """Counts the number of set bits (the number of occurences of 1)
    within a n-bit binary number. Uses a dict lookup table 

    XXX Add assertion + exception to enforce n % chunksize == 0

    >>> setbits16('10010111', chunk_size=8)
    5
    """
    return sum((dictionary[part] for part in chunk(n, chunk_size)))

def create_lookup(bits):
    """dict lookup table which contains a map between all permutations
    of binary number having length n and the number's corresponding
    hamming_weight. If we knew more about the distribution of binary
    numbers we'll be looking up, we could also try building the lookup
    table at runtime and memoize the hamming weights incrementally.

    >>> create_lookpup(3)
    {"000": 0, "001": 1, "010": 1, "011": 2, "100": 1, "101": 2, "111": 6}
    """
    return dict((pad(str(b), bits), b.count('1')) for b in \
                    (str(bin(n)[2:]) for n in range(0, 2**(bits+1))))

def _benchmark(nums, samples, binary_digits, chunk_size, dictionary, attempts=1000000):
    """Enabling garbage collection for tests
    XXX in progress
    """
    flags = ['gc.enable()', 'nums', 'samples', 'binary_digits',
             'chunk_size', 'dictionary']
    t = timeit.Timer("sum(map(lambda n: setbits(pad(n, binary_digits), dictionary, "\
                         "chunk_size=chunk_size), nums))", flags)
    try:
        print "%.2f microseconds per pass" % \
            (attempts * t.timeit(number=attempts)/attempts)
    except:
        t.print_exc()

def setup():
    """Configures argparser to handle command line arguments"""
    parser = argparse.ArgumentParser(description='Calculates summed hamming weight' \
                                         '(num of bits set to 1) for x, n-bit numbers.')
    parser.add_argument("--verbose", help="increase output verbosity",
                        action="store_true")

    parser.add_argument('-s', '--samples', type=int,
                        help='The number of samples to be included ' \
                            'in the hamming weight sum [default: 1000]')

    parser.add_argument('-b', '--bits', type=int,
                        help='The number of binary digits (length) '\
                            'of each binary number [default: 16]')

    parser.add_argument('-l', '--lookup', type=int,
                        help='Pre-compute a fast lookup table {sample: hamming-weight} ' \
                            'to quickly retrieve hamming-values for samples. As an optimization, ' \
                            'a chunk size can be provided to reduce the number of entries in the ' \
                            'lookup table. A chunk size should be choosen which is a multiple of '\
                            'the --bits value as the --bit value will be divided into -l lookups. ' \
                            ' [default: -l = -b]\n' \
                            'Example: Choosing -b 16 -l 8 will create a lookup table of all ' \
                            '2^8, 8-bit numbers and then calculate the hamming weight of each ' \
                            'binary as a combination of 2 chunks of 8-bit lookups.')

    return parser.parse_args()

if __name__ == "__main__":
    """Applies command line arguments (+ defaults) and runs basic
    benchmarks for the selected example.
    """
    args = setup()
    samples = args.samples if args.samples else 1000
    binary_digits = args.bits if args.bits else 16
    chunk_size = args.lookup if args.lookup else binary_digits
    dictionary = create_lookup(chunk_size)
    nums = (randbin(binary_digits) for x in xrange(samples))

    t0 = time.clock()
    x = sum(map(lambda n: setbits(pad(n, binary_digits), dictionary, 
                                  chunk_size=chunk_size), nums))
    print "Haming Weight: {} ({} seconds)".format(x, time.clock() - t0)

