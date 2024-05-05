# parser.py
from lexer import Lexer, Token
import json

class Parser:
    def __init__(self, tokens, source_code):
        self.tokens = iter(tokens)
        self.current_token = next(self.tokens, None)
        self.source_code = source_code
        self.declarations = []  # Store only top-level declarations

    def eat(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self.current_token = next(self.tokens, None)
        else:
            raise Exception(f"Unexpected token: expected {token_type}, got {self.current_token.type if self.current_token else 'EOF'}")

    def parse_function_declaration(self, is_nested=False):
        self.eat('FUN')
        function_name = self.current_token.value
        self.eat('IDENTIFIER')
        self.eat('(')
        parameters = self.parse_parameters()
        self.eat(')')

        return_type = 'Unit'
        if self.current_token and self.current_token.type == ':':
            self.eat(':')
            return_type = self.current_token.value
            self.eat('IDENTIFIER')

        self.eat('{')
        function_body, nested_declarations = self.parse_function_body()
        self.eat('}')

        function_declaration = {
            'type': 'function',
            'name': function_name,
            'parameters': parameters,
            'returnType': return_type,
            'body': function_body
        }

        # Only add to global declarations if it's a top-level function
        if not is_nested:
            self.declarations.append(function_declaration)

        return function_declaration, nested_declarations

    def parse_function_body(self):
        body_contents = []
        declarations = []
        start_pos = self.current_token.position_start

        while self.current_token and self.current_token.type != '}':
            if self.current_token.type == 'FUN':
                nested_function, nested_declarations = self.parse_function_declaration(is_nested=True)
                # Add all nested functions directly to the top-level declarations list
                self.declarations.extend([nested_function] + nested_declarations)
            else:
                body_contents.append(self.current_token.value)
                self.eat(self.current_token.type)

        end_pos = self.current_token.position_end
        function_body = self.source_code[start_pos:end_pos].strip()

        return function_body, declarations


    def parse_parameters(self):
        parameters = []
        while self.current_token and self.current_token.type != ')':
            param_name = self.current_token.value
            self.eat('IDENTIFIER')
            self.eat(':')
            param_type = self.current_token.value
            self.eat('IDENTIFIER')
            parameters.append({'name': param_name, 'type': param_type})
            if self.current_token and self.current_token.type == ',':
                self.eat(',')
        return parameters

    def generate_json(self, filename):
        with open(filename, 'w') as file:
            data = {'declarations': self.declarations}
            json.dump(data, file, indent=4)
