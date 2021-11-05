import argparse
import os

from .compiler import Compiler
from .lexer import Lexer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The NumLang compiler.")
    parser.add_argument(
        "file", type=argparse.FileType("r"), help="The NumLang file to compile."
    )
    parser.add_argument(
        "mode",
        choices=["compile", "simulate"],
        help="The mode to run the compiler in.",
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

    # Create a lexer
    lexer = Lexer(os.path.abspath(args.file.name), code)

    # Preprocess the code
    lexer.preprocess()

    # Lex the code into tokens
    tokens = lexer.lex()

    # Create a compiler
    compiler = Compiler(tokens)

    if args.mode == "compile":
        # Compile the program
        compiler.compile()

        if args.run:
            # Run the program
            compiler.run()
    elif args.mode == "simulate":
        # Simulate the program
        compiler.simulate()
