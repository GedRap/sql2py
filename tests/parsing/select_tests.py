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

    def test_limit_condition_only_limit_given(self):
        parsed = parse_select_query("select col1 from tab1 limit 15")

        self.assertEqual(parsed.rows_limit, 15)

    def test_limit_condition_both_offset_and_limit_given(self):
        parsed = parse_select_query("select col1 from tab1 limit 1, 5")

        self.assertEqual(parsed.rows_limit, 5)
        self.assertEqual(parsed.offset, 1)

if __name__ == '__main__':
    unittest.main()
