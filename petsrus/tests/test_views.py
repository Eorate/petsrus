import unittest

from petsrus.petsrus import app


class PetsRUsTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_index(self):
        result = self.app.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(bytes("Login Page", "utf-8"), result.data)


if __name__ == "__main__":
    unittest.main()
