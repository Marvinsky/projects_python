import unittest


def digits(x):
    digs = []
    while x != 0:
        div, mod = divmod(x, 10)
        x = div
        digs.append(mod)
    return digs


def is_palindrome(x):
    digs = digits(x)
    for a, b in zip(digs, reversed(digs)):
        if a != b:
            return False
    return True

class Tests(unittest.TestCase):

    def test_negative(self):
        self.assertFalse(is_palindrome(123))

    def test_positive(self):
        self.assertTrue(is_palindrome(123321))

if __name__ == "__main__":
    unittest.main()

