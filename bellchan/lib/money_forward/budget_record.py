class BaseBudgetRecord(object):

    def __init__(self, name, amount, remaining):
        self.name = name
        self.amount = self.extract_yen(amount)
        self.remaining = self.extract_yen(remaining)

    def __str__(self):
        return str(self.__dict__)

    def extract_yen(self, yen):
        return int(yen.strip().replace(',', '').strip('円'))


class FixedRecord(BaseBudgetRecord):
    pass


class VariableRecord(BaseBudgetRecord):
    pass
