import unittest
from pyparsing import ParseException
from sql2py.sql_parser import parse_delete_query
from sql2py.queries import Delete

class DeleteTestCase(unittest.TestCase):

    def test_delete_given_valid_table_name(self):
        parsed_query = parse_delete_query("delete from t1")

        self.assertEqual(parsed_query.table_name, "t1")
        self.assertIsInstance(parsed_query, Delete)

if __name__ == '__main__':
    unittest.main()
