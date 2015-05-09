import unittest
from sql2py.sql_parser import parse_select_query


class SimpleSelectsTestCase(unittest.TestCase):

    def test_very_basic_select(self):
        parsed = parse_select_query("select col1, col2 from tab1")

        self.assertEqual(parsed.columns[0], "col1")
        self.assertEqual(parsed.columns[1], "col2")
        self.assertEqual(len(parsed.columns), 2)
        self.assertEqual(parsed.table_name, "tab1")
        self.assertIsNone(parsed.offset)
        self.assertIsNone(parsed.order_type)
        self.assertEqual(len(parsed.order_columns), 0)

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
        self.assertIsNone(parsed.offset)

    def test_limit_condition_both_offset_and_limit_given(self):
        parsed = parse_select_query("select col1 from tab1 limit 1, 5")

        self.assertEqual(parsed.rows_limit, 5)
        self.assertEqual(parsed.offset, 1)

    def test_order_clause_implicit(self):
        parsed = parse_select_query("select col1 from tab1 order by col1")

        self.assertEqual(len(parsed.order_columns), 1)
        self.assertEqual(parsed.order_columns[0], "col1")
        self.assertEqual(parsed.order_type, "asc")

    def test_order_clause_asc(self):
        parsed = parse_select_query("select col1 from tab1 order by col1 asc")

        self.assertEqual(len(parsed.order_columns), 1)
        self.assertEqual(parsed.order_columns[0], "col1")
        self.assertEqual(parsed.order_type, "asc")

    def test_order_clause_desc(self):
        parsed = parse_select_query("select col1 from tab1 order by col1 desc")

        self.assertEqual(len(parsed.order_columns), 1)
        self.assertEqual(parsed.order_columns[0], "col1")
        self.assertEqual(parsed.order_type, "desc")

    def test_order_clause_multi_column(self):
        parsed = parse_select_query("select col1, col2 from tab1 order by col2, col1 asc")

        self.assertEqual(len(parsed.order_columns), 2)
        self.assertEqual(parsed.order_columns[0], "col2")
        self.assertEqual(parsed.order_columns[1], "col1")
        self.assertEqual(parsed.order_type, "asc")
if __name__ == '__main__':
    unittest.main()
