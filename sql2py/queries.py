class Select:
    def __init__(self):
        self.table_name = None
        self.columns = []

        self.offset = None
        self.rows_limit = None

        self.conditions = []

        self.order_columns = []
        self.order_type = None


class Insert:
    def __init__(self):
        self.table_name = None
        self.columns = []

        self.values = []


class Delete:
    def __init__(self):
        self.table_name = None


class Condition:
    def __init__(self, operand_left, operator, operand_right):
        self.operand_left = operand_left
        self.operator = operator
        self.operand_right = operand_right