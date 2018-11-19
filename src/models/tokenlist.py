from .token import Token

class TokenList(list):

    def __init__(self, text_dict=None):
        if text_dict is None:
            raise Exception("E necessario definir o variable text_dict")
        self.text_dict = text_dict

    def append(self, object):

        if isinstance(object, Token):


            super().append(object)

        else:
            raise Exception("E permitido somente adicionar objetos do tipo 'Token'")






