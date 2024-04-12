import unittest


class TestExample(unittest.TestCase):
    def test_always_fails(self) -> None:
        self.assertEqual(1, 1, "This test is designed to fail")


if __name__ == "__main__":
    unittest.main()
