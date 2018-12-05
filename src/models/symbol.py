class Symbol:
    def __init__(self, name = None, type = None, scope = None, category=None):
        self.name = name
        self.type = type
        self.scope = scope
        self.category = category

    def reset(self):
        self.name = None
        self.type = None
        self.scope = None
        self.category = None

    def __eq__(self, other):
        return self.name == other.name and self.type == other.type and self.scope == other.scope \
            and self.category == other.category