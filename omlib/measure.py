from .thing import Thing


class Measure(Thing):

    def __init__(self,numericalValue, unit):
        super.__init__()
        self.numericalValue = numericalValue
        self.unit = unit

    def __init__(self, uri, numericalValue, unit):
        super().__init__(uri)
        self.numericalValue = numericalValue
        self.unit = unit
