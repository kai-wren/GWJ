import unittest
from test_bot import search, format_output

class Test_GWJ_Bot(unittest.TestCase):

	def setUp(self):
		self.res = search("bunny")
		self.form_res = format_output(self.res)

	def test_search(self):
		self.assertEqual(search("addfbdsfczvbfgsfc"), [],
			"incorrect return when no articles found.")
		self.assertEqual(len(self.res), 10, "incorrect size")
		self.assertIsInstance(self.res, list, "incorrect return type")
		self.assertIsInstance(self.res[0], dict, "incorrect type")
		self.assertIsInstance(self.res[0]["title"], str, "incorrect type")
		self.assertIsInstance(self.res[0]["biorxiv_url"], str, "incorrect type")

	def test_format(self):
		self.assertIsInstance(self.form_res, str, "incorrect type")
		self.assertTrue(i in self.form_res for i in ['1','2','3','4','5','6','7','8','9','10'])
		self.assertEqual(format_output(search("addfbdsfczvbfgsfc")), "",
			"incorrect return when no articles found.")
		self.assertTrue(len(self.form_res.split(",")) >= 10)



if __name__ == '__main__':
    unittest.main()