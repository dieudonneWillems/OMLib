from omlib.thing import Thing


class Measure(Thing):

    def __init__(self,numerical_value, unit):
        super.__init__()
        self.numerical_value = numerical_value
        self.unit = unit

    def __init__(self, uri, numerical_value, unit):
        super().__init__(uri)
        self.numerical_value = numerical_value
        self.unit = unit
