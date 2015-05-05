from pyparsing import Keyword, Word, alphas, alphanums, Group, delimitedList, Forward
from queries import Select


def parse_select_query(query):
    select_grammar = Forward()

    select_keyword_token = Keyword("select", caseless=True)
    from_keyword_token = Keyword("from", caseless=True)

    identifier_token = Word(alphas, alphanums).setName("identifier")
    column_name_tokens = Group(delimitedList(identifier_token, ","))
    table_name_token = Word(alphas, alphanums).setName("table_name")

    select_grammar << (select_keyword_token + ('*' | column_name_tokens).setResultsName("columns")\
                     + from_keyword_token + table_name_token.setResultsName("table"))

    parsed_query = select_grammar.parseString(query)

    select_query = Select()
    select_query.table_name = parsed_query.table
    select_query.columns = parsed_query.columns

    return select_query