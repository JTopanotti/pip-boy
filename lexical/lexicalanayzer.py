from src.models.terminals import terminals
from src.lexical.statemachine import StateMachine

class LexicalAnalyze:

    def __init__(self, source_code):
        self.source = source_code
        self.current_char = ''
        self.next_char = ''
        self.ident_buffer = []
        self.literal_buffer = []
        self.tokens = []

    def expression_end_handler(self):
        return None

    def char_handler(self):
        return None

    def white_space_handler(self):
        return None

    def numerical_handler(self):
        return None

    def start_handler(self):
        return None

    def end_handler(self):
        return None

    def run(self):
        state_machine = StateMachine()
        state_machine.set_start("start_state")
        state_machine.add_state("start_state", self.start_handler)
        state_machine.add_state("char_state", self.char_handler)
        state_machine.add_state("expression_end_state", self.expression_end_handler)
        state_machine.add_state("white_space_state", self.white_space_handler)
        state_machine.add_state("numerical_state", self.numerical_handler)
        state_machine.add_state("end_state", self.end_handler, True)



