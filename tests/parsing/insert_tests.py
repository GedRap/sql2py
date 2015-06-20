import unittest
from pyparsing import ParseException
from sql2py.sql_parser import parse_insert_query

class InsertTestCase(unittest.TestCase):

    def test_insert_given_table_name_and_single_column(self):
        parsed_query = parse_insert_query("insert into t (a) values (1)")

        self.assertEqual(parsed_query.table_name, "t")
        self.assertEqual(parsed_query.columns[0], "a")
        self.assertEqual(len(parsed_query.columns), 1)
        self.assertEqual(parsed_query.values[0], "1")
        self.assertEqual(len(parsed_query.values), 1)

    def test_insert_given_table_name_and_multiple_values(self):
        parsed_query = parse_insert_query("insert into t (a, b) values (1, 2)")

        self.assertEqual(parsed_query.table_name, "t")
        self.assertEqual(parsed_query.columns[0], "a")
        self.assertEqual(parsed_query.columns[1], "b")
        self.assertEqual(len(parsed_query.columns), 2)
        self.assertEqual(parsed_query.values[0], "1")
        self.assertEqual(parsed_query.values[1], "2")
        self.assertEqual(len(parsed_query.values), 2)

    def test_insert_given_table_name_and_mismatching_values(self):
        # lambda function used so that refactoring and other tools can recognize the invocation
        self.assertRaises(ParseException, lambda: parse_insert_query("insert into t (a) values (1, 2)"))


if __name__ == '__main__':
    unittest.main()
