from src.models.terminals import terminals

class Token:

    def __init__(self):
        self.identifier = None
        self.value = None


    def is_reserved(self):
        return self.value in terminals.values()
