from symbol_table import Symbol

class Memory:

    def __init__(self, name):
        self.name = name
        self.symbols = {}

    def has_key(self, name):
        return name in self.symbols

    def get(self, name):
        return self.symbols.get(name, None)

    def put(self, name, value):
        self.symbols[name] = value

    def __str__(self):
        return f"<{self.name}>:\n{str(self.symbols)}"

class MemoryStack:

    def __init__(self, memory=None):
        memory = Memory('global') if memory is None else memory
        self.stack = [memory]

    def get(self, name):
        memory = self._get_memory_with_name(name)
        if memory is not None:
            return memory.get(name)
        return None

    def set(self, name, value):
        memory = self._get_memory_with_name(name)
        if memory is not None:
            memory.put(name, value)
        else:
            self.insert(name, value)

    def insert(self, name, value):
        self.stack[-1].put(name, value)

    def push(self, memory):
        self.stack.append(memory)

    def pop(self):
        self.stack.pop()

    def __str__(self):
        ans = ""
        for m in self.stack:
            ans += "\n" + str(m)
        return ans

    def _get_memory_with_name(self, name):
        for mem in reversed(self.stack):
            if mem.has_key(name):
                return mem
        return None
