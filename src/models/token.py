import importlib

terminals = importlib.import_module("models.terminals").terminals


class Token:

    def __init__(self, value, reserved=False, literal=False, line=None, scope=None):
        self.value = value
        self.reserved = reserved
        self.literal = literal
        self.line = line
        self.scope = scope

        if reserved:
            self.identifier = list(terminals.keys())[
                list(terminals.values()).index(value.upper())
            ]
        elif isinstance(self.value, int):
            self.identifier = list(terminals.keys())[
                list(terminals.values()).index("INTEIRO")
            ]
        elif literal:
            self.identifier = list(terminals.keys())[
                list(terminals.values()).index("LITERAL")
            ]
        else:
            self.identifier = list(terminals.keys())[
                list(terminals.values()).index("IDENTIFIER")
            ]