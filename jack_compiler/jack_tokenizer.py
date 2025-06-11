from enum import Enum


class TokenType(Enum):
    KEYWORD = 0
    SYMBOL = 1
    INT_CONST = 2
    STR_CONST = 3
    IDENTIFIER = 4


class Token:
    def __init__(self, token_type: TokenType, value):
        self.type: TokenType = token_type
        self.value: str | int = value


class Tokenizer:
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__file = open(file_path, 'r')
        self.__current_word: str = ""
        self.__current_token: Token = None

    def get_current_token(self) -> Token:
        return self.__current_token

    def __peek_current_char(self) -> str:
        current_position = self.__file.tell()
        char = self.__file.read(1)
        self.__file.seek(current_position)
        return char

    def __peek_next_char(self) -> str:
        current_pos = self.__file.tell()
        self.__file.read(1)
        next_char = self.__file.read(1)
        self.__file.seek(current_pos)
        return next_char

    def __skip_comments_and_whitespaces(self):
        while (True):  # Skip comments and empty chars
            if self.__peek_current_char().isspace():
                self.__file.read(1)
                continue
            if self.__peek_current_char() == "/":
                next_char = self.__peek_next_char()
                if next_char == "/":
                    self.__file.readline()
                    continue
                elif next_char == "*":
                    self.__file.read(1)
                    while (not (self.__peek_current_char() == "*" and self.__peek_next_char() == "/")):
                        self.__file.read(1)
                    self.__file.read(2)
                    continue
                else:
                    break
            else:
                break

    def has_more_tokens(self) -> bool:
        return self.__peek_current_char() != ""

    def advance(self) -> None:
        self.__skip_comments_and_whitespaces()
        self.__current_word = self.__peek_current_char()
        if self.__peek_current_char() in ['{', '}', '(', ')', '[', ']', '+', '-', '*', '/',
                                   '&', '|', '<', '>', '=', ';', ',', '.', '~']:
            self.__current_token = Token(TokenType.SYMBOL, self.__current_word)
            self.__file.read(1)
            return
        if self.__peek_current_char().isdigit():
            self.__file.read(1)
            while (self.__peek_current_char().isdigit()):
                self.__current_word += self.__peek_current_char()
                self.__file.read(1)
            self.__current_token = Token(TokenType.INT_CONST, int(self.__current_word))
            return
        if self.__peek_current_char() == '"':
            self.__file.read(1)
            self.__current_word = ""
            while (self.__peek_current_char() != '"'):
                self.__current_word += self.__peek_current_char()
                self.__file.read(1)
            self.__current_token = Token(TokenType.STR_CONST, self.__current_word)
            self.__file.read(1)
            return
        if self.__peek_current_char().isalpha() or self.__peek_current_char() == '_':
            self.__file.read(1)
            while (self.__peek_current_char().isalpha() or self.__peek_current_char().isalnum()
                   or self.__peek_current_char() == '_'):
                self.__current_word += self.__peek_current_char()
                self.__file.read(1)
            self.__file.tell()
            if self.__current_word in ["class", "constructor", "function", "method", "field", "static", "var", "int",
                                       "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if",
                                       "else", "while", "return"]:
                self.__current_token = Token(TokenType.KEYWORD, self.__current_word)
                return
            else:
                self.__current_token = Token(TokenType.IDENTIFIER, self.__current_word)
                return
        raise Exception("Unexpected character '{}'".format(self.__peek_current_char()))

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, '_Tokenizer__file'):  # Note: name mangling format
            self.__file.close()
