import main
import unittest


class Test_TestIsPrime(unittest.TestCase):
    def test_is_prime(self):
        self.assertEqual(main.is_prime(1, 1), False)
        self.assertEqual(main.is_prime(2, 1), True)
        self.assertEqual(main.is_prime(7, 6), True)
        self.assertEqual(main.is_prime(15, 14), False)
        self.assertEqual(main.is_prime(2999, 1500), True)


class Test_TestGetPrimes(unittest.TestCase):
    def test_get_primes(self):
        self.assertEqual(main.get_primes(
            0,
            10
        ), [
            2,
            3,
            5,
            7
        ])