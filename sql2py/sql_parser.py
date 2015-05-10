from pyparsing import Keyword, Word, alphas, alphanums, nums, Group, Literal, delimitedList, Forward, Optional, oneOf
from queries import Select, Condition


def parse_select_query(query):
    select_grammar = Forward()

    select_keyword_token = Keyword("select", caseless=True)
    from_keyword_token = Keyword("from", caseless=True)
    limit_keyword_token = Keyword("limit", caseless=True)
    order_by_keyword_token = Keyword("order by", caseless=True)
    where_keyword_token = Keyword("where", caseless=True)
    operators_tokens = oneOf("= != < > >= <=")

    identifier_token = Word(alphanums + "_").setName("identifier")
    column_name_tokens = Group(delimitedList(identifier_token, ","))
    table_name_token = Word(alphanums + "_").setName("table_name")
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