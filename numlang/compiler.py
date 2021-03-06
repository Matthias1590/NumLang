import random
import time
from typing import List

from .lexer import Statement, Token, TokenTypes

random.seed(350930)

_print = print


def print(*args, **kwargs) -> None:
    kwargs["end"] = ""
    return _print(*args, **kwargs)


class Stack:
    def __init__(self, size: int) -> None:
        self.size = size
        self.__stack = [
            random.randint(0, 2 ** 32 - 1) for _ in range(self.size)
        ]  # Declaring __stack as a private variable to prevent it from being accessed outside of the class.
        self.pointer = 0

    def push(self, value: int) -> None:
        self.__stack[self.pointer] = value
        self.pointer += 1
        if self.pointer == len(self.__stack):
            self.pointer = 0

    def pop(self) -> int:
        self.pointer -= 1
        if self.pointer == -1:
            self.pointer = self.size - 1
        return self.__stack[self.pointer]

    def __repr__(self) -> str:
        return str(self.__stack)


class Compiler:
    def __init__(self, operations: List[Token]) -> None:
        self.operations = operations

    def cross_reference(self) -> None:
        # Loop through all the operations in reverse order (if and else)
        end_addresses = []
        program_counter = len(self.operations) - 1
        while program_counter >= 0:
            operation = self.operations[program_counter]

            if isinstance(operation.type, TokenTypes.Keywords.End):
                end_addresses.append((program_counter, operation))
            elif isinstance(operation.type, TokenTypes.Statements.Else):
                end = end_addresses.pop()
                operation.data["end"] = end[0]
                end[1].data["used"] = True
                end_addresses.append((program_counter, operation))
            elif isinstance(operation.type, TokenTypes.Statements.If):
                end = end_addresses.pop()
                operation.data["end"] = end[0]
                end[1].data["used"] = True

            program_counter -= 1

        # Loop through all the operations (while)
        while_addresses = []
        end_addresses = []
        program_counter = 0
        while program_counter < len(self.operations):
            operation = self.operations[program_counter]

            if isinstance(operation.type, TokenTypes.Statements.While):
                while_addresses.append(program_counter)
            elif (
                isinstance(operation.type, TokenTypes.Keywords.End)
                and while_addresses
                and not operation.data.get("used", False)
            ):
                operation.data["start"] = while_addresses.pop()
                end_addresses.append(program_counter)

            program_counter += 1

        # Loop through all the operations in reverse order (do)
        end_addresses = []
        program_counter = len(self.operations) - 1
        while program_counter >= 0:
            operation = self.operations[program_counter]

            if isinstance(operation.type, TokenTypes.Keywords.End):
                if not operation.data.get("used", False):
                    end_addresses.append(program_counter)
            elif isinstance(operation.type, TokenTypes.Statements.Do):
                operation.data["end"] = end_addresses.pop()

            program_counter -= 1

    def simulate(self) -> int:
        self.cross_reference()

        # Allocate 1024 bytes of memory
        memory = bytearray(1024)

        # Create a stack of size 1024
        stack = Stack(1024)

        # Set the program_counter to 0
        program_counter = 0

        start = time.time()
        exit_code = 0

        variable_map = {}
        variable_pointer = 0
        last_variables = []

        # Simulate the operations
        while program_counter < len(self.operations):
            operation: Token = self.operations[program_counter]
            word, operation, arguments, data = (
                operation.word,
                operation.type,
                operation.type.arguments,
                operation.data,
            )
            if isinstance(operation, TokenTypes.Operations.Push):
                value = arguments[0]
                if isinstance(value, TokenTypes.Literals.Numbers.Integer):
                    stack.push(value.value)
                elif isinstance(value, TokenTypes.Literals.String):
                    stack.push(0)
                    for char in value.value[::-1]:
                        stack.push(ord(char))
                elif isinstance(value, TokenTypes.Literals.Character):
                    stack.push(ord(value.value))
            elif isinstance(operation, TokenTypes.Operations.Pop):
                stack.pop()
            elif isinstance(operation, TokenTypes.Operations.Duplicate):
                a = stack.pop()
                stack.push(a)
                stack.push(a)
            elif isinstance(operation, TokenTypes.Operations.Add):
                a = stack.pop()
                b = stack.pop()
                stack.push(b + a)
            elif isinstance(operation, TokenTypes.Operations.Subtract):
                a = stack.pop()
                b = stack.pop()
                stack.push(b - a)
            elif isinstance(operation, TokenTypes.Operations.Multiply):
                a = stack.pop()
                b = stack.pop()
                stack.push(a * b)
            elif isinstance(operation, TokenTypes.Operations.Divide):
                a = stack.pop()
                b = stack.pop()
                stack.push(b % a)  # Remainder
                stack.push(b // a)  # Result
            elif isinstance(operation, TokenTypes.Operations.Print):
                print(f"{stack.pop()}\n")
            elif isinstance(operation, TokenTypes.Statements.If):
                if stack.pop() == 0:
                    program_counter = data["end"] + 1
                    continue
            elif isinstance(operation, TokenTypes.Statements.Else):
                program_counter = data["end"]
                continue
            elif isinstance(operation, TokenTypes.Statements.While):
                pass
            elif isinstance(operation, TokenTypes.Statements.Do):
                if stack.pop() == 0:
                    program_counter = data["end"] + 1
                    continue
            elif isinstance(operation, TokenTypes.Keywords.End):
                if "start" in data:
                    program_counter = data["start"]
                    continue
            elif isinstance(operation, TokenTypes.Operations.GreaterThan):
                a = stack.pop()
                b = stack.pop()
                stack.push(int(b > a))
            elif isinstance(operation, TokenTypes.Operations.LessThan):
                a = stack.pop()
                b = stack.pop()
                stack.push(int(b < a))
            elif isinstance(operation, TokenTypes.Operations.GreaterThanOrEqual):
                a = stack.pop()
                b = stack.pop()
                stack.push(int(b >= a))
            elif isinstance(operation, TokenTypes.Operations.LessThanOrEqual):
                a = stack.pop()
                b = stack.pop()
                stack.push(int(b <= a))
            elif isinstance(operation, TokenTypes.Operations.Equal):
                a = stack.pop()
                b = stack.pop()
                stack.push(int(b == a))
            elif isinstance(operation, TokenTypes.Operations.NotEqual):
                a = stack.pop()
                b = stack.pop()
                stack.push(int(b != a))
            elif isinstance(operation, TokenTypes.Operations.Write):
                buffer = bytearray()
                while True:
                    char = stack.pop()
                    buffer.append(char)
                    if char == 0:
                        break
                print(buffer.decode("utf-8"))
            elif isinstance(operation, TokenTypes.Operations.Exit):
                exit_code = stack.pop()
                break
            elif isinstance(operation, TokenTypes.Operations.Load):
                address = stack.pop()
                value = 0

                if arguments:
                    bytes_to_store = int(repr(arguments[0]))
                else:
                    bytes_to_store = last_variables.pop()[0]
                for i in range(bytes_to_store):
                    value = (value << 8) + memory[address + (bytes_to_store - 1) - i]

                stack.push(value)
            elif isinstance(operation, TokenTypes.Operations.Store):
                address = stack.pop()
                value = stack.pop()

                if arguments:
                    bytes_to_store = int(repr(arguments[0]))
                else:
                    bytes_to_store = last_variables.pop()[0]
                for i in range(bytes_to_store):
                    memory[address + i] = value & 0xFF
                    value >>= 8
            elif isinstance(operation, TokenTypes.Operations.BitwiseOr):
                a = stack.pop()
                b = stack.pop()
                stack.push(b | a)
            elif isinstance(operation, TokenTypes.Operations.BitwiseAnd):
                a = stack.pop()
                b = stack.pop()
                stack.push(b & a)
            elif isinstance(operation, TokenTypes.Operations.ShiftLeft):
                a = stack.pop()
                b = stack.pop()
                stack.push(b << a)
            elif isinstance(operation, TokenTypes.Operations.ShiftRight):
                a = stack.pop()
                b = stack.pop()
                stack.push(b >> a)
            elif isinstance(operation, TokenTypes.Operations.CreateVariable):
                variable_map[arguments[0]] = (arguments[1], variable_pointer)
                variable_pointer += arguments[1]
            elif isinstance(operation, TokenTypes.Misc.Variable):
                stack.push(variable_map[word][1])
                last_variables.append(variable_map[word])
            elif isinstance(operation, TokenTypes.Operations.Modulo):
                a = stack.pop()
                b = stack.pop()
                stack.push(b % a)
            else:
                raise NotImplementedError(f"Operation {operation} not implemented")
            program_counter += 1

        # Return with the exit code and execution time
        return exit_code, time.time() - start
