class StateMachine:

    def __init__(self):
        self.handlers = {}
        self.start_state = None
        self.end_states = []

    def add_state(self, name, handler, end_state=False):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.end_states.append(name)

    def set_start(self, name):
        self.start_state = name.upper()

    def run(self, cargo):
        try:
            handler = self.handlers[self.start_state]
        except:
            raise Exception("Precisa chamar .set_start() antes de .run()")
        if not self.end_states:
            raise Exception("Pelo menos um estado final deve existir")

        while True:
            #(new_state, cargo) = handler(cargo)
            new_state = handler()
            print(new_state)
            if new_state.upper() in self.end_states:
                handler = self.handlers[new_state.upper()]
                handler()
                print("chegou ao estado", new_state)
                break
            else:
                handler = self.handlers[new_state.upper()]
        
