from .budget_record import FixedRecord, VariableRecord


class BudgetStatus:

    def __init__(self):
        self.variable_records = []
        self.fixed_records = []

        self.total_amount = 0
        self.total_remaining = 0
        self.variable_amount = 0
        self.variable_remaining = 0
        self.fixed_amount = 0
        self.fixed_remaining = 0

    def __str__(self):
        return str(self.__dict__)

    def is_variable(self, record):
        return isinstance(record, VariableRecord)

    def is_fixed(self, record):
        return isinstance(record, FixedRecord)

    def add(self, record):
        if self.is_variable(record):
            self.variable_records.append(record)
        elif self.is_fixed(record):
            self.fixed_records.append(record)
        else:
            raise TypeError('Invalid record type.')

        self.set_summary()

    def set_summary(self):
        self.variable_amount = sum([r.amount for r in self.variable_records])
        self.variable_remaining = sum([r.remaining for r in self.variable_records])
        self.fixed_amount = sum([r.amount for r in self.fixed_records])
        self.fixed_remaining = sum([r.remaining for r in self.fixed_records])

        self.total_amount = self.variable_amount + self.fixed_amount
        self.total_remaining = self.variable_remaining + self.fixed_remaining
