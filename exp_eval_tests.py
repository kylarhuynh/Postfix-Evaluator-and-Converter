# Start of unittest - add to completely test functions in exp_eval

import unittest
from exp_eval import *


class test_expressions(unittest.TestCase):
    def test_postfix_eval_01(self):  # testing for all operators
        self.assertAlmostEqual(postfix_eval("3 5 +"), 8)
        self.assertAlmostEqual(postfix_eval("86 3 -"), 83)
        self.assertAlmostEqual(postfix_eval("9 3 /"), 3)
        self.assertAlmostEqual(postfix_eval("3 7 *"), 21)
        self.assertAlmostEqual(postfix_eval("2 3 **"), 8)
        self.assertAlmostEqual(postfix_eval("48 2 >>"), 12)
        self.assertAlmostEqual(postfix_eval("12 2 <<"), 48)
        self.assertAlmostEqual(postfix_eval("3  5    +"), 8)  # test spaces

    def test_postfix_eval_001(self):
        self.assertAlmostEqual(postfix_eval("5 1 2 + 4 ** + 3 -"), 83)  # test from doc
        self.assertAlmostEqual(postfix_eval("-9 7 +"), -2)  # test negative numbers
        self.assertEqual(postfix_eval('524287 2 1 << 2 << >>'), 7)  # test bit shifters

    def test_postfix_eval_float(self):  # test floats
        self.assertAlmostEqual(postfix_eval("1"), 1)
        self.assertAlmostEqual(postfix_eval("3.2 1.1 +"), 4.3)
        self.assertAlmostEqual(postfix_eval("6.7 3.2 -"), 3.5)
        self.assertAlmostEqual(postfix_eval("3.3 1.1 /"), 3)
        self.assertAlmostEqual(postfix_eval("10.2 3.5 *"), 35.7)
        self.assertAlmostEqual(postfix_eval("2.2 3.4 **"), 14.59611, 3)

    def test_postfix_eval_bitfloat(self):
        try:
            postfix_eval("6 2.3 >>")  # test bit shift float exception
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Illegal bit shift operand")
        try:
            postfix_eval("1 7.6 * 3.5 >>")  # test bit shift float exception
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Illegal bit shift operand")
        try:
            postfix_eval("2.7 7.0 <<")  # test bit shift float exception
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Illegal bit shift operand")

    def test_postfix_eval_02(self):
        try:
            postfix_eval("blah")  # test invalid token
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Invalid token")

    def test_postfix_eval_03(self):
        try:
            postfix_eval("+")  # test insufficient operands
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Insufficient operands")
        try:
            postfix_eval("+ 4")  # test insufficient operands
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Insufficient operands")
        try:
            postfix_eval("4 +")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Insufficient operands")
        try:
            postfix_eval("4 -")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Insufficient operands")
        try:
            postfix_eval("5 *")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Insufficient operands")
        try:
            postfix_eval("5 /")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Insufficient operands")
        try:
            postfix_eval("5 **")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Insufficient operands")
        try:
            postfix_eval("5 >>")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Insufficient operands")
        try:
            postfix_eval("1 <<")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Insufficient operands")

    def test_postfix_eval_15(self):
        try:
            postfix_eval("3 3 / 1 >>")  # should produce bit shift exception
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Illegal bit shift operand")

    def test_postfix_eval_16(self):
        try:
            postfix_eval("5 5 / 1 <<")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Illegal bit shift operand")

    def test_postfix_eval_04(self):
        try:
            postfix_eval("4 5 7 -")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Too many operands")

    def test_postfix_eval_05(self):
        try:
            postfix_eval("")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Empty input")

    def test_postfix_eval_06(self):
        try:
            postfix_eval("1 0 /")
            self.fail()
        except ValueError:
            self.assertRaises(ZeroDivisionError)

    def test_postfix_eval_07(self):  # zero division error
        with self.assertRaises(ValueError):
            postfix_eval("4 7 7 - /")

    def test_postfix_eval_08(self):
        try:
            postfix_eval("12 c")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Invalid token")

    def test_postfix_eval_09(self):
        try:
            postfix_eval("12.3 9 + -")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Insufficient operands")

    def test_postfix_eval_10(self):
        try:
            postfix_eval("3 5 5 3 b")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Invalid token")

    def test_infix_to_postfix_01(self):  # testing various infix expressions
        self.assertEqual(infix_to_postfix("6 - 3"), "6 3 -")
        self.assertEqual(infix_to_postfix("6"), "6")
        self.assertEqual(infix_to_postfix("6 - 3 * 2 / ( 1 - 5 ) ** 5 ** 2.1"), "6 3 2 * 1 5 - 5 2.1 ** ** / -")
        self.assertEqual(infix_to_postfix("( -3 + 2 ) * -3 ** 4"), "-3 2 + -3 4 ** *")  # tests negatives
        self.assertEqual(infix_to_postfix("1 * 2 ** ( 4 + 1.5 + 2.5 )"), "1 2 4 1.5 + 2.5 + ** *")  # tests
        self.assertEqual(infix_to_postfix("3 + 4 * 2 / ( 1 - 5 ) << 2 ** 3"), "3 4 2 * 1 5 - 2 << 3 ** / +")  # from doc
        self.assertEqual(infix_to_postfix("3 +   4 * 2 / ( 1  -  5 ) << 2 **   3"),
                         "3 4 2 * 1 5 - 2 << 3 ** / +")  # spaces

    def test_infix_to_postfix_02(self):
        self.assertEqual(infix_to_postfix("3 + 4 * 2 / ( 1 - 5 ) ** 2 ** 3"), "3 4 2 * 1 5 - 2 3 ** ** / +")

    def test_infix_to_postfix_03(self):
        self.assertEqual(infix_to_postfix("( 4 * 12 ) >> 2 + 4"), "4 12 * 2 >> 4 +")

    def test_prefix_to_postfix_(self):
        self.assertEqual(prefix_to_postfix("* - 7.8 / 4 5 + / 4 5 6"), "7.8 4 5 / - 4 5 / 6 + *")  # decimals
        self.assertEqual(prefix_to_postfix("* - 3 /   2   1 - / 4 5 6"), "3 2 1 / - 4 5 / 6 - *")  # with spaces

    def test_prefix_to_postfix(self):
        self.assertEqual(prefix_to_postfix("+ -1 * 3 4"), "-1 3 4 * +")  # test with negative


if __name__ == "__main__":
    unittest.main()
