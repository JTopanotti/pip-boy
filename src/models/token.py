import importlib

terminals = importlib.import_module("src.models.terminals").terminals


class Token:

    def __init__(self, value, reserved=False, literal=False):
        self.value = value
        if reserved:
            self.identifier = list(terminals.keys())[
                list(terminals.values()).index(value.upper())
            ]
        elif isinstance(self.value, int):
            self.identifier = list(terminals.keys())[
                list(terminals.values()).index("INTEGER")
            ]
        elif literal:
            self.identifier = list(terminals.keys())[
                list(terminals.values()).index("LITERAL")
            ]
        else:
            self.identifier = list(terminals.keys())[
                list(terminals.values()).index("IDENTIFIER")
            ]