from pyparsing import Keyword, Word, alphas, alphanums, nums, Group, Literal, delimitedList, \
    Forward, Optional, oneOf, printables, ParseException
from queries import Select, Insert, Condition, Delete

identifier_token = Word(alphanums + "_").setName("identifier")
table_name_token = Word(alphanums + "_").setName("table_name")

def build_select_grammar():
    select_grammar = Forward()

    select_keyword_token = Keyword("select", caseless=True)
    from_keyword_token = Keyword("from", caseless=True)
    limit_keyword_token = Keyword("limit", caseless=True)
    order_by_keyword_token = Keyword("order by", caseless=True)
    where_keyword_token = Keyword("where", caseless=True)
    operators_tokens = oneOf("= != < > >= <=")

    column_name_tokens = Group(delimitedList(identifier_token, ","))
    order_by_token = order_by_keyword_token + column_name_tokens.setResultsName("order_by_cols")\
                     + Optional(
                        (Keyword("asc", caseless=True).setResultsName("order_by_type") |
                         Keyword("desc", caseless=True).setResultsName("order_by_type"))
                    )

    limit_token = limit_keyword_token + Optional(Word(nums).setResultsName("offset") + Literal(",")) \
                  + Word(nums).setResultsName("rows_limit")

    where_expression = where_keyword_token + identifier_token.setResultsName("operand_left") \
                       + operators_tokens.setResultsName("operator") + Word(alphanums).setResultsName("operand_right")

    select_grammar << select_keyword_token + ('*' | column_name_tokens).setResultsName("columns")\
                     + from_keyword_token + table_name_token.setResultsName("table")\
                     + Optional(where_expression).setResultsName("where")\
                     + Optional(order_by_token).setResultsName("order")\
                     + Optional(limit_token).setResultsName("limit")

    return select_grammar

def build_insert_grammar():
    insert_grammar = Forward()

    insert_into_keyword_token = Keyword("insert into", caseless=True)
    values_token = Keyword("values", caseless=True)

    columns = Optional(Group(delimitedList(identifier_token, ",")))
    values_list_token = Group(delimitedList(Word(alphanums + " "), ","))

    insert_grammar << insert_into_keyword_token + table_name_token.setResultsName("table_name") \
                      + Literal("(") + columns.setResultsName("columns") + Literal(")") + \
                      values_token + Literal("(") + values_list_token.setResultsName("values_list") + Literal(")")

    return insert_grammar

def build_delete_grammar():
    delete_grammar = Forward()

    delete_from_keyword_token = Keyword("delete from", caseless=True)

    delete_grammar << delete_from_keyword_token + table_name_token.setResultsName("table_name")

    return delete_grammar

def parse_select_query(query):
    select_grammar = build_select_grammar()

    parsed_query = select_grammar.parseString(query)

    select_query = Select()
    select_query.table_name = parsed_query.table
    select_query.columns = parsed_query.columns

    if parsed_query.where is not "":
        condition = Condition(
            parsed_query.where.operand_left,
            parsed_query.where.operator,
            parsed_query.where.operand_right
        )
        select_query.conditions.append(condition)

    if parsed_query.limit is not "":
        if parsed_query.limit.offset is not "":
            select_query.offset = int(parsed_query.limit.offset)
        select_query.rows_limit = int(parsed_query.limit.rows_limit)
        
    if parsed_query.order is not "":
        select_query.order_columns = parsed_query.order.order_by_cols
        if parsed_query.order.order_by_type is not "":
            select_query.order_type = parsed_query.order.order_by_type
        else:
            select_query.order_type = "asc"

    return select_query

def parse_insert_query(query):
    insert_grammar = build_insert_grammar()

    parsed_query = insert_grammar.parseString(query)

    insert_query = Insert()
    insert_query.table_name = parsed_query.table_name
    insert_query.columns = parsed_query.columns[0]
    insert_query.values = parsed_query.values_list

    if len(insert_query.columns) != len(insert_query.values):
        raise ParseException("Number of columns should match the number of values")

    return insert_query

def parse_delete_query(query):
    delete_grammar = build_delete_grammar()

    parsed_query = delete_grammar.parseString(query)

    delete_query = Delete()
    delete_query.table_name = parsed_query.table_name

    return delete_query