from enum import Enum, auto

class Type(Enum):
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    VECTOR = auto()
    MATRIX = auto()
    BOOLEAN = auto()
    RANGE = auto()
    NULL = auto()
    UNKNOWN = auto()

    @staticmethod
    def is_number(mtype):
        return mtype in [Type.FLOAT, Type.INT]


class Symbol:

    def __init__(self, name, mtype, size):
        self.name = name
        self.type = mtype
        self.size = size


class SymbolTable(object):
    def __init__(self):
        self.scopes = []

    def push_scope(self, name):
        self.scopes.append((name, {}))

    def pop_scope(self):
        self.scopes.pop()

    def put(self, name, symbol):
        self.scopes[-1][1][name] = symbol

    def check_exists(self, name: str) -> bool:
        return self.get(name) is not None

    def get(self, name: str):
        for _, scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def is_in_loop(self) -> bool:
        for name, _ in self.scopes:
            if name in ["while", "for"]:
                return True
        return False

