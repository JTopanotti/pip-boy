import importlib

terminals = importlib.import_module("src.models.terminals").terminals


class Token:

    def __init__(self, value, reserved=False):
        self.value = value
        if reserved:
            self.identifier = list(terminals.keys())[
                list(terminals.values()).index(value)
            ]
        else:
            self.identifier = list(terminals.keys())[
                list(terminals.values()).index("Identifier")
            ]