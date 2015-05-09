import unittest
from sql2py.sql_parser import parse_select_query


class SimpleSelectsTestCase(unittest.TestCase):

    def test_very_basic_select(self):
        parsed = parse_select_query("select col1, col2 from tab1")

        self.assertEqual(parsed.columns[0], "col1")
        self.assertEqual(parsed.columns[1], "col2")
        self.assertEqual(len(parsed.columns), 2)
        self.assertEqual(parsed.table_name, "tab1")

    def test_underscore_in_identifiers(self):
        parsed = parse_select_query("select col_1 from tab_1")

        self.assertEqual(parsed.columns[0], "col_1")
        self.assertEqual(len(parsed.columns), 1)
        self.assertEqual(parsed.table_name, "tab_1")

        parsed = parse_select_query("select col_a from tab_a")

        self.assertEqual(parsed.columns[0], "col_a")
        self.assertEqual(len(parsed.columns), 1)
        self.assertEqual(parsed.table_name, "tab_a")


if __name__ == '__main__':
    unittest.main()
