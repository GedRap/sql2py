from pyparsing import Keyword, Word, alphas, alphanums, nums, Group, Literal, delimitedList, Forward, Optional
from queries import Select


def parse_select_query(query):
    select_grammar = Forward()

    select_keyword_token = Keyword("select", caseless=True)
    from_keyword_token = Keyword("from", caseless=True)
    limit_keyword_token = Keyword("limit", caseless=True)

    identifier_token = Word(alphanums + "_").setName("identifier")
    column_name_tokens = Group(delimitedList(identifier_token, ","))
    table_name_token = Word(alphanums + "_").setName("table_name")

    limit_token = limit_keyword_token + Optional(Word(nums).setResultsName("offset") + Literal(",")) \
                  + Word(nums).setResultsName("rows_limit")

    select_grammar << (select_keyword_token + ('*' | column_name_tokens).setResultsName("columns")\
                     + from_keyword_token + table_name_token.setResultsName("table"))\
                     + Optional(limit_token).setResultsName("limit")

    parsed_query = select_grammar.parseString(query)

    select_query = Select()
    select_query.table_name = parsed_query.table
    select_query.columns = parsed_query.columns

    if parsed_query.limit is not "":
        if parsed_query.limit.offset is not "":
            select_query.offset = int(parsed_query.limit.offset)
        select_query.rows_limit = int(parsed_query.limit.rows_limit)

    return select_query