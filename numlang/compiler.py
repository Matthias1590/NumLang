from typing import List

from .lexer import Token, TokenTypes

import random


class Compiler:
    def __init__(self, operations: List[Token]) -> None:
        self.operations = operations

    def simulate(self) -> int:
        memory = bytearray(1024)  # Allocate 1024 bytes of memory
        # Create a stack containing garbage values
        stack = [random.randint(0, 2 ** 32 - 1)] * 1024
        for operation in self.operations:
            operation, arguments = operation.type, operation.type.arguments
            if isinstance(operation, TokenTypes.Operations.Push):
                print("Push!")
            else:
                print("Idk")
        return 0
