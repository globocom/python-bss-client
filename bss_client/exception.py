class BSSError(Exception):
    def __init__(self, code, value):
        self.code = code
        self.value = value

    def __str__(self):
        return "{0} - {1}".format(self.code, self.value)
