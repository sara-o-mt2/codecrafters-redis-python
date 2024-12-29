from enum import Enum

class RESPDataType(Enum):
    SIMPLE_STRING = b"+"
    ERROR = b"-"
    INTEGER = b":"
    BULK_STRING = b"$"
    ARRAY = b"*"
