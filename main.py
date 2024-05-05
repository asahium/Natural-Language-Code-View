from lexer import Lexer
from parser import Parser
import sys
import json

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename.kt>")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, 'r') as file:
        source_code = file.read()

    lexer = Lexer(source_code)
    tokens = list(lexer.tokenize())
    parser = Parser(tokens, source_code)

    try:
        parser.parse_function_declaration()
        output_filename = 'test.json'
        parser.generate_json(output_filename)  # Only pass the filename
        print(f"Output written to {output_filename}")
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    main()
