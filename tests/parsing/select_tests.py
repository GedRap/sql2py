import unittest
from sql2py.sql_parser import parse_select_query


class SimpleSelectsTestCase(unittest.TestCase):

    def test_very_basic_select(self):
        parsed = parse_select_query("select col1, col2 from tab1")

        self.assertEqual(parsed.columns[0], "col1")
        self.assertEqual(parsed.columns[1], "col2")
        self.assertEqual(len(parsed.columns), 2)
        self.assertEqual(parsed.table_name, "tab1")


if __name__ == '__main__':
    unittest.main()
