from collections import UserString
from typing import List


class Token(UserString):
    """A string that has additional information about the source code for the string."""
    def __init__(self, s: str, line_number:int, character_number: int, filename: str = None):
        super().__init__(s)
        self.line_number = line_number
        self.character_number = character_number
        self.filename = filename