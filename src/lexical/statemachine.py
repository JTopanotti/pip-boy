class StateMachine:

    def __init__(self):
        self.handlers = {}
        self.start_state = None
        self.end_states = []
        self.set_new_char = None

    def add_state(self, name, handler, end_state=False):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.end_states.append(name)

    def set_start(self, name):
        self.start_state = name.upper()

    def set_new_char_handler(self, handler):
        self.set_new_char = handler

    def run(self, cargo):
        if cargo:
            self.cargo = cargo
        else:
            raise Exception("Precisa passar um cargo para processar")
        try:
            handler = self.handlers[self.start_state]
        except:
            raise Exception("Precisa chamar .set_start() antes de .run()")
        if not self.end_states:
            raise Exception("Pelo menos um estado final deve existir")
        if not self.set_new_char:
            raise Exception("Precisa setar um handler para chars novos")

        while True:
            if self.set_new_char:
                self.set_new_char()
            new_state = handler()
            print(new_state)
            if new_state.upper() in self.end_states:
                handler = self.handlers[new_state.upper()]
                handler()
                print("chegou ao estado", new_state)
                break
            else:
                handler = self.handlers[new_state.upper()]
        
