# lexer.py

class Token:
    def __init__(self, type, value, position_start, position_end):
        self.type = type
        self.value = value
        self.position_start = position_start
        self.position_end = position_end

class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.length = len(code)

    def tokenize(self):
        while self.position < self.length:
            current_char = self.code[self.position]

            if current_char.isspace():
                self.position += 1
                continue

            if current_char.isalpha():
                start_pos = self.position
                while self.position < self.length and (self.code[self.position].isalnum() or self.code[self.position] == '_'):
                    self.position += 1
                value = self.code[start_pos:self.position]
                if value in {'fun', 'val'}:
                    yield Token(value.upper(), value, start_pos, self.position)
                else:
                    yield Token('IDENTIFIER', value, start_pos, self.position)
                continue

            if current_char in {'(', ')', '{', '}', ':', ';'}:
                self.position += 1
                yield Token(current_char, current_char, self.position - 1, self.position)
                continue

            self.position += 1
            yield Token('UNKNOWN', current_char, self.position - 1, self.position)

        yield Token('EOF', '', self.position, self.position)
