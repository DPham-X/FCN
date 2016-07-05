import unittest
import sys
sys.path.append("..")
from fcn import FCN


class FCNCheckTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_convert_hex_2byte_low(self):
        x = 0
        out = FCN.convert_to_hex(x, 2)
        self.assertEqual(out, '0000')

    def test_convert_hex_4byte_low(self):
        x = 0
        out = FCN.convert_to_hex(x, 4)
        self.assertEqual(out, '00000000')

    def test_convert_hex_8byte_low(self):
        x = 0
        out = FCN.convert_to_hex(x, 8)
        self.assertEqual(out, '0000000000000000')

    def test_convert_hex_16byte_low(self):
        x = 0
        out = FCN.convert_to_hex(x, 16)
        self.assertEqual(out, '00000000000000000000000000000000')

    def test_convert_hex_2byte_mid(self):
        x = 0
        for i in range(2*2):
            x += 16**i
        out = FCN.convert_to_hex(x, 2)
        self.assertEqual(out, '1111')

    def test_convert_hex_4byte_mid(self):
        x = 0
        for i in range(4 * 2):
            x += 16 ** i
        out = FCN.convert_to_hex(x, 4)
        self.assertEqual(out, '11111111')

    def test_convert_hex_8byte_mid(self):
        x = 0
        for i in range(8 * 2):
            x += 16 ** i
        out = FCN.convert_to_hex(x, 8)
        self.assertEqual(out, '1111111111111111')

    def test_convert_hex_16byte_mid(self):
        x = 0
        for i in range(16 * 2):
            x += 16 ** i
        out = FCN.convert_to_hex(x, 16)
        self.assertEqual(out, '11111111111111111111111111111111')
