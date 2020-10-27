class Condition:
    """
        Condition to be evaluated on a decision node to partition a dataset
    """

    def __init__(self, column, value, header):
        self.column = column
        self.value = value
        self.header = header

    def match(self, example):
        """
            Evaluate the condition to see if it is true
        """

        val = example[self.column]
        if self.__is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __repr__(self):
        """
            Converting current object to string will print the following
        """

        condition = "=="
        if self.__is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (
            self.header[self.column], condition, str(self.value))

    def __is_numeric(self, value):
        """
            Check if a value is numeric
        """
        return isinstance(value, int) or isinstance(value, float)
