from typing import List

from .lexer import Token, TokenTypes

import random


class Stack:
    def __init__(self, size: int) -> None:
        self.size = size
        self.__stack = [random.randint(0, 2 ** 32 - 1) for _ in range(self.size)]

    def push(
        self,
    ) -> None:
        ...


class Compiler:
    def __init__(self, operations: List[Token]) -> None:
        self.operations = operations

    def simulate(self) -> int:
        # Allocate 1024 bytes of memory
        memory = bytearray(1024)
        # Create a stack containing garbage values
        stack = Stack(1024)

        # Simulate the operations
        for operation in self.operations:
            operation, arguments = operation.type, operation.type.arguments
            if isinstance(operation, TokenTypes.Operations.Push):
                stack.push(arguments[0])
            elif isinstance(operation, TokenTypes.Operations.Pop):
                stack.pop()
            else:
                print(stack)

        # Return with exit code 0
        return 0
