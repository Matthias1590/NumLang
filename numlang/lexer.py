from __future__ import annotations
from typing import Any, List, Tuple, Type


def get_number_type(string: str) -> bool:
    """
    Returns the type of the number.
    """

    if string.count("-") > 1:
        return None
    if string.count("x") > 1:
        return None
    if string.count("o") > 1:
        return None
    if string.count("b") > 1:
        return None
    for char in string:
        if char not in "0123456789-.xob":
            return None
    if "." in string:
        if "x" in string or "o" in string or "b" in string:
            return None
        return TokenTypes.Literals.Numbers.Float
    return TokenTypes.Literals.Numbers.Integer


class Location:
    def __init__(self, file: str, line: int, column: int) -> None:
        self.file = file
        self.line = line
        self.column = column

    def __repr__(self) -> str:
        return f"{self.file}:{self.line + 1}:{self.column + 1}"


class TokenType:
    def __init__(self, *arguments: List[Any]) -> None:
        self.arguments = arguments

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(map(lambda x: repr(x), self.arguments))})"


class Literal:
    def __init__(self, value: Any) -> None:
        self.value = value

    def __repr__(self) -> str:
        return repr(self.value)


class Statement(TokenType):
    ...


class TokenTypes:
    class Literals:
        """
        Literals are used to represent literal, constant values.
        """

        class Numbers:
            """
            Used to represent numbers.
            """

            class Float(Literal):
                """
                Used to represent floating point numbers.
                """

                def __init__(self, value: Any) -> None:
                    super().__init__(float(value))

            class Integer(Literal):
                """
                Used to represent integer numbers.
                """

                def __init__(self, value: Any) -> None:
                    if value.startswith("0x"):
                        value = int(value, 16)
                    elif value.startswith("0o"):
                        value = int(value, 8)
                    elif value.startswith("0b"):
                        value = int(value, 2)
                    super().__init__(int(value))

        class String(Literal):
            """
            Used to represent a piece of text terminated by a null character.
            """

            def __init__(self, value: Any) -> None:
                super().__init__(eval(value))

        class Character(Literal):
            """
            Used to represent a single character.
            """

            def __init__(self, value: Any) -> None:
                super().__init__(eval(value))

    class Operations:
        """
        Operations are used to manipulate values.

        To specify arguments, push the arguments onto the stack in the order they are specified.
        To retrieve results, pop the arguments off the stack in the order they are specified.
        """

        class Push(TokenType):
            """
            Pushes a value onto the stack.

            Syntax: `push(value)`

            Arguments:
            - `value`: The value to push, can be any literal.

            Returns: none
            """

            def __init__(self, value: Literal) -> None:
                super().__init__(value)

        class Pop(TokenType):
            """
            Pops a value off the stack.

            Syntax: `pop`

            Arguments: none

            Returns: none
            """

        class Duplicate(TokenType):
            """
            Duplicates the top value on the stack.

            Syntax: `dup`

            Arguments:
            - `number`: The number to duplicate.

            Returns:
            - `number`: The given number.
            - `number`: The given number duplicated.
            """

        class Add(TokenType):
            """
            Adds the top two values on the stack.

            Syntax: `+`

            Arguments:
            - `a`: The first value to add.
            - `b`: The second value to add.

            Returns:
            - `a + b`.
            """

        class Subtract(TokenType):
            """
            Subtracts the top two values on the stack.

            Syntax: `-`

            Arguments:
            - `a`: The first value to subtract.
            - `b`: The second value to subtract.

            Returns:
            - `a - b`.
            """

        class Multiply(TokenType):
            """
            Multiplies the top two values on the stack.

            Syntax: `*`

            Arguments:
            - `a`: The first value to multiply.
            - `b`: The second value to multiply.

            Returns:
            - `a * b`.
            """

        class Divide(TokenType):
            """
            Divides the top two values on the stack.

            Syntax: `/`

            Arguments:
            - `a`: The first value to divide.
            - `b`: The second value to divide.

            Returns:
            - `a // b`.
            - `a % b`.
            """

        class GreaterThan(TokenType):
            """
            Determines if the second top value on the stack is greater than the top value on the stack.

            Syntax: `>`

            Arguments:
            - `a`: The first value to compare.
            - `b`: The second value to compare.

            Returns:
            - `1` if `a > b`, else `0`.
            """

        class LessThan(TokenType):
            """
            Determines if the second top value on the stack is less than the top value on the stack.

            Syntax: `<`

            Arguments:
            - `a`: The first value to compare.
            - `b`: The second value to compare.

            Returns:
            - `1` if `a < b`, else `0`.
            """

        class GreaterThanOrEqual(TokenType):
            """
            Determines if the second top value on the stack is greater than or equal to the top value on the stack.

            Syntax: `>=`

            Arguments:
            - `a`: The first value to compare.
            - `b`: The second value to compare.

            Returns:
            - `1` if `a >= b`, else `0`.
            """

        class LessThanOrEqual(TokenType):
            """
            Determines if the second top value on the stack is less than or equal to the top value on the stack.

            Syntax: `<=`

            Arguments:
            - `a`: The first value to compare.
            - `b`: The second value to compare.

            Returns:
            - `1` if `a <= b`, else `0`.
            """

        class Equal(TokenType):
            """
            Determines if the second top value on the stack is equal to the top value on the stack.

            Syntax: `==`

            Arguments:
            - `a`: The first value to compare.
            - `b`: The second value to compare.

            Returns:
            - `1` if `a == b`, else `0`.
            """

        class NotEqual(TokenType):
            """
            Determines if the second top value on the stack is not equal to the top value on the stack.

            Syntax: `!=`

            Arguments:
            - `a`: The first value to compare.
            - `b`: The second value to compare.

            Returns:
            - `1` if `a != b`, else `0`.
            """

        class Print(TokenType):
            """
            Prints the top number on the stack as a string.

            Syntax: `print`

            Arguments:
            - `number`: The number to print.

            Returns: none
            """

        class Write(TokenType):
            """
            Keeps popping from the stack until a zero is found and then interprets all the numbers as a null terminated string.

            Syntax: `write`

            Arguments:
            - `string`: A bunch of characters terminated by a null character.

            Returns: none
            """

        class Exit(TokenType):
            """
            Exits the program with the given exit code.

            Syntax: `exit`

            Arguments:
            - `code`: The code to exit with.

            Returns: none
            """

    class Statements:
        """
        Statements are used to manipulate the program flow.
        """

        class If(Statement):
            """
            If the top value on the stack is not 0, execute the code in the if block, else execute the code in the else block (if it exists)

            Syntax:\n
            ```numl
            if
                // Code
            end
            ```
            """

        class Else(Statement):
            """
            If the previous if block was not ran, the code within the else block will run.

            Syntax:\n
            ```numl
            if
                // Code
            else
                // Code
            end
            ```
            """

    class Keywords:
        """
        Keywords are used to manipulate the program flow.
        """

        class End(TokenType):
            """
            End a code block.

            Syntax: `end`

            """


class Token:
    def __init__(self, type: TokenTypes, location: Location) -> None:
        self.type = type
        self.location = location
        self.data = {}

    def __repr__(self) -> str:
        return repr(self.type)


class Lexer:
    def __init__(self, file: str, code: str) -> None:
        self.file = file
        self.lines = [line + "\n" for line in code.splitlines()]
        self.line = 0
        self.column = 0
        self.index = 0

    def preprocess(self) -> None:
        # Mapping strings
        string_map = {}
        string_index = 0
        in_string = False
        string = ""
        for i, line in enumerate(self.lines):
            for j, char in enumerate(line):
                if char == '"':
                    in_string = not in_string
                    if not in_string:
                        string += char
                        string_map[string_index] = string
                        self.lines[i] = self.lines[i].replace(
                            string, f"STRING_{string_index}", 1
                        )
                        string = ""
                        string_index += 1
                if in_string:
                    string += char

        # Removing single line comments (//)
        for i, line in enumerate(self.lines):
            self.lines[i] = line.split("//")[0]

        # Removing multi line comments (/* and */)
        code = ""
        in_comment = False
        previous_char = ""
        for i, line in enumerate(self.lines):
            for char in line:
                if char == "*" and previous_char == "/":
                    in_comment = True
                    code = code[:-1]
                elif char == "/" and previous_char == "*":
                    in_comment = False
                    continue
                if not in_comment:
                    code += char
                previous_char = char
        self.lines = code.splitlines()
        # print("".join(code), self.lines)
        # exit()

        # Adding strings back in
        for i, line in enumerate(self.lines):
            for string in string_map:
                self.lines[i] = self.lines[i].replace(
                    f"STRING_{string}", string_map[string]
                )

        # Removing empty lines
        self.lines = [line.rstrip() + "\n" for line in self.lines if line.strip()]

    def lex(self) -> List[Token]:
        tokens = []

        while self.token_available:
            token = self.read_token()
            if token:
                tokens.append(token)

        return tokens

    def parse_word(self, word: str) -> Token:
        if word == "":
            return None

        word, arguments = self.parse_arguments(word)
        location = Location(self.file, self.line, self.column)

        type = {
            "push": TokenTypes.Operations.Push,
            "pop": TokenTypes.Operations.Pop,
            "dup": TokenTypes.Operations.Duplicate,
            "+": TokenTypes.Operations.Add,
            "-": TokenTypes.Operations.Subtract,
            "*": TokenTypes.Operations.Multiply,
            "/": TokenTypes.Operations.Divide,
            ">": TokenTypes.Operations.GreaterThan,
            "<": TokenTypes.Operations.LessThan,
            ">=": TokenTypes.Operations.GreaterThanOrEqual,
            "<=": TokenTypes.Operations.LessThanOrEqual,
            "==": TokenTypes.Operations.Equal,
            "!=": TokenTypes.Operations.NotEqual,
            "print": TokenTypes.Operations.Print,
            "write": TokenTypes.Operations.Write,
            "if": TokenTypes.Statements.If,
            "else": TokenTypes.Statements.Else,
            "end": TokenTypes.Keywords.End,
            "exit": TokenTypes.Operations.Exit,
        }.get(word, None)

        if not type:
            raise Exception(f"Unknown word: {repr(word)} at {location}")

        try:
            return Token(type(*arguments), location)
        except TypeError as e:
            raise Exception(f"Invalid arguments for {word} at {location}: {e}")

    def parse_value(self, string: str) -> Any:
        if string == "":
            raise Exception(
                f"Expected value, got nothing at {Location(self.file, self.line, self.column)}"
            )
        elif string.endswith('"') and string.startswith('"'):
            return TokenTypes.Literals.String(string)
        elif (
            string.endswith("'")
            and string.startswith("'")
            and (len(string) == 3 or (string[1] == "\\" and len(string) == 4))
        ):
            return TokenTypes.Literals.Character(string)
        elif number_type := get_number_type(string):
            return number_type(string)
        elif string.endswith(")"):
            raise Exception(
                f"Unmatched parenthesis at {Location(self.file, self.line, self.column)}"
            )
        else:
            raise Exception(
                f'Unknown value: "{string}" at {Location(self.file, self.line, self.column)}'
            )

    def parse_arguments(self, word: str) -> Tuple[str, List[str]]:
        arguments = []

        if "(" in word and ")" in word:
            add_argument = lambda argument: arguments.append(self.parse_value(argument))

            # Reading the arguments
            in_string = False
            argument = ""
            if word.rindex(")") != len(word) - 1:
                raise Exception(
                    f"Invalid syntax at {Location(self.file, self.line - 1, self.column + word.rindex(')') + 1)}"
                )
            for char in word[word.index("(") + 1 : word.rindex(")")]:
                if char == '"':
                    argument += char
                    if not in_string:
                        start = Location(
                            self.file, self.line - 1, self.column - len(word)
                        )
                    in_string = not in_string
                elif char == "\n":
                    raise Exception(f"Unterminated string at {start}")
                elif char == "," and not in_string:
                    add_argument(argument)
                    argument = ""
                else:
                    argument += char
            if argument.strip():
                add_argument(argument)

        return word.split("(")[0], arguments

    @property
    def token_available(self) -> bool:
        return self.index < len("".join(self.lines))

    def read_token(self) -> Token:
        in_string = False
        in_arguments = False

        word = ""
        while self.token_available:
            char = self.read_char()

            # Toggle the string flag when we encounter a quote
            if char == '"':
                in_string = not in_string
            elif char == "(" and not in_string:
                in_arguments = True
            elif char == ")" and not in_string:
                in_arguments = False

            # Stop reading when we encounter a space that's not in a string
            if not in_string and not in_arguments and char.isspace():
                break

            # Add the character if we're in a string or if it's not whitespace
            if not char.isspace() or in_string:
                word += char

        return self.parse_word(word)

    def read_char(self) -> str:
        char = self.lines[self.line][self.column]

        self.index += 1
        self.column += 1
        if char == "\n":
            self.line += 1
            self.column = 0

        return char
