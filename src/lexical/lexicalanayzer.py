from builtins import Exception
from models.terminals import terminals
from models.token import Token


class LexicalAnalyzer:

    def __init__(self):
        self.text = None
        self.current_char = None
        self.ident_buffer = ""
        self.value_buffer = ""
        self.tokens = []
        self.handlers = {
            "CHAR_STATE": self.char_handler,
            "SPECIAL_CHAR_STATE": self.special_char_handler,
            "WHITE_SPACE_STATE": self.white_space_handler,
            "DIGIT_STATE": self.digit_handler,
            "END_STATE": self.end_handler
        }
        self.start_state = "WHITE_SPACE_STATE"
        self.end_states = ["ERROR_STATE", "END_STATE"]

        self.specials = [":", ";", ",", ".", "(", ")", "[", "]", "\'", "=", "<", ">", "+", "-", "/", "*"]

    def set_current_char(self):
        if self.text:
            if len(self.text) > 1:
                self.current_char, self.text, = \
                    self.text[0], self.text[1:]
            else:
                self.current_char, self.text = \
                    self.text[0], ''
        else:
            self.current_char = None

    def char_handler(self):
        if self.current_char:
            while self.current_char.isalnum():
                self.ident_buffer += self.current_char
                return "char_state"

            if self.current_char in self.specials:
                self.register_identifier()
                self.register_number()
                self.special_helper()
                return "special_char_state"
            elif self.current_char.isspace():
                self.register_identifier()
                return "white_space_state"
        else:
            return "end_state"

    def white_space_handler(self):
        if self.current_char:
            while self.current_char.isspace():
                return "white_space_state"
            else:
                if self.current_char.isalpha():
                    self.ident_buffer += self.current_char
                    return "char_state"
                elif self.current_char in self.specials:
                    self.special_helper()
                    return "special_char_state"
                elif self.current_char.isdigit():
                    self.value_buffer += self.current_char
                    return "digit_state"
        else:
            return "end_state"

    def skip_comment_char(self):
        self.current_char, self.text = \
            self.text[1], self.text[2:]

    def special_helper(self):
        if self.current_char in ['<', '>'] and \
                self.text[0] in ['=', '>']:
            operator = self.current_char
            self.set_current_char()
            operator = operator + self.current_char
            self.tokens.append(Token(operator, reserved=True))
        elif self.current_char == ':' and \
                self.text[0] == '=':
            operator = self.current_char
            self.set_current_char()
            operator = operator + self.current_char
            self.tokens.append(Token(operator, reserved=True))
        elif self.current_char == '\'':
            self.set_current_char()
            buffer = ''
            while not self.current_char == '\'':
                buffer += self.current_char
                self.set_current_char()
            self.tokens.append(Token(buffer, literal=True))
        elif self.current_char == '/' and \
                self.text[0] == '*':
            self.skip_comment_char()
            while self.current_char != '*' and \
                    self.current_char != '/':
                self.set_current_char()
            self.skip_comment_char()
        else:
            self.tokens.append(Token(self.current_char, reserved=True))

    def special_char_handler(self):
        if self.current_char:
            if self.current_char.isalpha():
                self.ident_buffer += self.current_char
                return "char_state"
            elif self.current_char.isdigit():
                self.value_buffer += self.current_char
                return "digit_state"
            elif self.current_char.isspace():
                return "white_space_state"
            elif self.current_char in self.specials:
                self.special_helper()
                return "special_char_state"
            else:
                return "error_state"
        else:
            return "end_state"

    def digit_handler(self):
        if self.current_char:
            while self.current_char.isdigit():
                self.value_buffer += self.current_char
                return "digit_state"

            if self.current_char.isspace():
                self.register_number()
                return "white_space_state"
            elif self.current_char.isalpha():
                self.register_number()
                return "char_state"
            elif self.current_char in self.specials:
                self.register_number()
                self.special_helper()
                return "special_char_state"
        else:
            return "end_state"

    def end_handler(self):
        if self.ident_buffer:
            self.register_identifier()
        for token in self.tokens:
            print(token.value, " : ", token.identifier, " : ", terminals[token.identifier])

    def register_number(self):
        value = self.value_buffer
        if value:
            value = int(value)
            self.tokens.append(Token(value))
            self.value_buffer = ""

    def register_identifier(self):
        value = self.ident_buffer
        if value:
            if self.is_reserved(value):
                token = Token(value, reserved=True)
            else:
                token = Token(value)
            self.tokens.append(token)
            self.ident_buffer = ""

    def is_reserved(self, identifier):
        return identifier.upper() in terminals.values()

    def run(self, text):
        if self.tokens:
            self.tokens = []
        self.text = text.replace('\n', '')

        try:
            handler = self.handlers[self.start_state]
        except:
            raise Exception("Precisa chamar .set_start() antes de .run()")
        if not self.end_states:
            raise Exception("Pelo menos um estado final deve existir")

        while True:
            self.set_current_char()
            new_state = handler()
            print(new_state)
            if new_state.upper() in self.end_states:
                handler = self.handlers[new_state.upper()]
                handler()
                print("chegou ao estado", new_state)
                return self.tokens
            else:
                handler = self.handlers[new_state.upper()]