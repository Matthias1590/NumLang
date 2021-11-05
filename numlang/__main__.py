import argparse
import os

from .lexer import Lexer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The NumLang compiler.")
    parser.add_argument(
        "file", type=argparse.FileType("r"), help="The NumLang file to compile."
    )
    parser.add_argument(
        "-r",
        "--run",
        action="store_true",
        help="Run the program after successful compilation.",
    )
    args = parser.parse_args()

    # Read and close the file
    code = args.file.read()
    args.file.close()

    # Lex the code into tokens
    lexer = Lexer(os.path.abspath(args.file.name), code)
    tokens = lexer.lex()

    for token in tokens:
        print(token)
