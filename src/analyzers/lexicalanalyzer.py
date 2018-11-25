from builtins import Exception
from models.terminals import terminals
from models.token import Token


class LexicalAnalyzer:

    def __init__(self):
        self.text = None
        self.text_lined = {}
        self.current_line = 1
        self.current_scope = 0
        self.scope_counter = 0
        self.current_char = None
        self.ident_buffer = ""
        self.value_buffer = ""
        self.error = ""
        self.tokens = []
        self.handlers = {
            "CHAR_STATE": self.char_handler,
            "SPECIAL_CHAR_STATE": self.special_char_handler,
            "WHITE_SPACE_STATE": self.white_space_handler,
            "DIGIT_STATE": self.digit_handler,
            "END_STATE": self.end_handler
        }
        self.start_state = "WHITE_SPACE_STATE"
        self.end_state = "END_STATE"
        self.error_state = "ERROR_STATE"
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
            
    def append_token_list(self, token):

        while not self.text_lined[self.current_line].strip():
            del self.text_lined[self.current_line]
            self.current_line += 1

        if token.identifier == 5: #PROCEDURE
            self.scope_counter += 1
            self.current_scope = self.scope_counter

        if token.identifier == 7 and self.current_scope > 0: #END
            self.current_scope = 0

        if self.text_lined:
            if str(token.value) in self.text_lined[self.current_line]:
                line = self.text_lined[self.current_line]
                token_value = token.value

                if token.literal:
                    token_value = "\'{}\'".format(token_value)

                self.text_lined[self.current_line] = \
                        line.replace(str(token_value), '', 1)

            token.line = self.current_line
            token.scope = self.current_scope
            self.tokens.append(token)
        

    def char_handler(self):
        if self.current_char:
            while self.current_char.isalnum() or self.current_char == '_':
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
                    if self.special_helper() == "error_state":
                        return "error_state"
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
        if self.current_char == '-' and \
                self.text[0].isdigit():
            self.value_buffer += self.current_char
            return "digit_state"
        if self.current_char == '.':
            if self.text and self.text[0] == '.':
                operator = self.current_char
                self.set_current_char()
                operator += self.current_char
                self.append_token_list(Token(operator, reserved=True))
            else:
                self.append_token_list(Token(self.current_char, reserved=True))
        elif self.current_char in ['<', '>'] and \
                self.text[0] in ['=', '>']:
            operator = self.current_char
            self.set_current_char()
            operator = operator + self.current_char
            self.append_token_list(Token(operator, reserved=True))
        elif self.current_char == ':' and \
                self.text[0] == '=':
            operator = self.current_char
            self.set_current_char()
            operator = operator + self.current_char
            self.append_token_list(Token(operator, reserved=True))
        elif self.current_char == '\'':
            self.set_current_char()
            buffer = ''
            while not self.current_char == '\'':
                buffer += self.current_char
                self.set_current_char()
            self.append_token_list(Token(buffer, literal=True))
        elif self.current_char == '(' and \
                self.text[0] == '*':
            self.skip_comment_char()
            while (self.current_char != '*') and \
                    (self.text[0] != ')'):
                self.set_current_char()
                if not self.text:
                    self.error = "Comentário não finalizado"
                    return "error_state"
            self.set_current_char()
        else:
            self.append_token_list(Token(self.current_char, reserved=True))

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
            self.append_token_list(Token(value))
            self.value_buffer = ""

    def register_identifier(self):
        value = self.ident_buffer
        if value:
            if self.is_reserved(value):
                token = Token(value, reserved=True)
            else:
                token = Token(value)
            self.append_token_list(token)
            self.ident_buffer = ""

    def is_reserved(self, identifier):
        return identifier.upper() in terminals.values()

    def run(self, text):
        if self.tokens:
            self.tokens = []
        self.text = text.replace('\t',' ').replace('\n', ' ')
        text_divided = text.replace('\t',' ').split('\n')
        for key, line in enumerate(text_divided):
            self.text_lined[key + 1] = line

        #Limpar comentários do dicionario
        for key in range(1, max(self.text_lined.keys()) + 1):
            if '(*' in self.text_lined[key]:
                for commented in range(key, max(self.text_lined.keys()) + 1):
                    text = self.text_lined[commented]
                    self.text_lined[commented] = ''
                    if '*)' in text:
                        break





        try:
            handler = self.handlers[self.start_state]
        except:
            raise Exception("Precisa chamar .set_start() antes de .run()")
        if not self.end_state:
            raise Exception("Pelo menos um estado final deve existir")

        while True:
            self.set_current_char()
            new_state = handler()
            print(new_state)
            if new_state.upper() == self.end_state:
                handler = self.handlers[new_state.upper()]
                handler()
                print("chegou ao estado", new_state)
                return self.tokens
            elif new_state.upper() == self.error_state:
                raise Exception("Comentário não finalizado")
            else:
                handler = self.handlers[new_state.upper()]