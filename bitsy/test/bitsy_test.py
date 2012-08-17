import unittest
from bitsy import bitsy

dictionary = bitsy.create_lookup(8)

class BitsyTest(unittest.TestCase):

    def test_padding(self):
        """Tests to make sure the lenght of an arbitrary binary number
        is 'bits'
        """
        self.assertTrue(len(bitsy.pad('101', 8)) == 8,
                        "bitsy.pad failed to pad the correct number of bits")
        

    def test_randbin(self):
        """Verifies that bitsy.randbin is generating a str
        representation of a random binary number and that the padded
        length is correct
        """
        randbin = bitsy.randbin(bits=8)
        self.assertTrue(len(randbin) == 8,
                        "bitsy.randbin failed to pad the correct number of bits")

        self.assertTrue(type(randbin) == str,
                        "bitsy.randbin expected return type str, " \
                            "instead is: {}".format(type(randbin)))

    def test_setbits(self):
        """Checks that the number of 1's found in the str
        representation of the binary number in calculated correctly by
        bitsy.setbits16
        """
        bnum = '1011010110100110'
        expected = 9
        actual = bitsy.setbits(bnum, dictionary)
        self.assertTrue(expected == actual, "Inconsistent results for bitsy.setbits16, " \
                            "expected {} bits set, found {}".format(expected, actual))

    def test_chunking(self):
        chunk_size = 8
        bnum = '1011010110100110'
        expected = ['10110101', '10100110']
        actual = list(bitsy.chunk(bnum, chunk_size))
        # generator 'actual' converted to list to make len() available
        self.assertTrue(len(list(actual)) == len(bnum)/chunk_size,
                        "The number of chunks is not consistent with the expected "\
                            "output for bitsy.chunk")
        self.assertTrue(actual == expected, "Incorrect output for bitsy.chunk" \
                            "expected {}, but got {}".format(expected, actual))
