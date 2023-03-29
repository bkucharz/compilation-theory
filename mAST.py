from symbol_table import Type

class Node(object):
    def __init__(self, children=None, leaf=None, line=None, size=None):
        if children:
            self.children = children
        else:
            self.children = []
        self.line = line
        self.type = Type.UNKNOWN
        self.leaf = leaf
        self.size = size


class Program(Node):
    def __init__(self, instructions, line=None):
        super().__init__(children=instructions, line=line)


class Instructions(Node):
    def __init__(self, instructions, line=None):
        super().__init__(children=instructions, line=line)


class Instruction(Node):
    def __init__(self, instruction, line=None):
        super().__init__(children=[instruction], line=line)



class Return(Node):
    def __init__(self, name, expression, line=None):
        super().__init__(leaf=name, children=[expression], line=line)


class Break(Node):
    def __init__(self, line=None):
        super().__init__(line=line)


class Continue(Node):
    def __init__(self, line=None):
        super().__init__(line=line)


class Assignment(Node):
    def __init__(self, left, op, right, line=None):
        super().__init__(leaf=op, children=[left, right], line=line)

class Function(Node):
    def __init__(self, name, arg, line=None):
        super().__init__(leaf=name, children=[arg], line=line)


class Number(Node):
    def __init__(self, value, line=None):
        super().__init__(leaf=value, line=line)

class IntNum(Node):
    def __init__(self, value, line=None):
        super().__init__(leaf=value, line=line)


class FloatNum(Node):
    def __init__(self, value, line=None):
        super().__init__(leaf=value, line=line)


class Variable(Node):
    def __init__(self, name, line=None):
        super().__init__(leaf=name, line=line)

class Reference(Node):
    def __init__(self, name, value_list, line=None):
        super().__init__(leaf=name, children=value_list, line=line)


class ValueList(Node):
    def __init__(self, value_list, line=None):
        super().__init__(children=value_list, line=line)


class Transpose(Node):
    def __init__(self, value, line=None):
        super().__init__(leaf=value, line=line)

class BinOp(Node):
    def __init__(self, left, op, right, line=None):
        super().__init__(leaf=op, children=[left, right], line=line)

class For(Node):
    def __init__(self, id, range, instruction, line=None):
        super().__init__(children=[id, range, instruction], line=line)

class Range(Node):
    def __init__(self, start, stop, line=None):
        super().__init__(children=[start, stop], line=line)

class Print(Node):
    def __init__(self, value_list, line=None):
        super().__init__(children=[value_list], line=line)


class While(Node):
    def __init__(self, relation, instruction, line=None):
        super().__init__(children=[relation, instruction], line=line)

class Relation(Node):
    def __init__(self, left, op, right, line=None):
        super().__init__(leaf=op, children=[left, right], line=line)

class List(Node):
    def __init__(self, value_list, line=None):
        super().__init__(children=value_list, line=line)


class BinExpr(Node):
    def __init__(self, op, left, right, line=None):
        super().__init__(children=[left, right], leaf=op, line=line)


class If(Node):
    def __init__(self, relation, instruction, else_instruction=None, line=None):
        super().__init__(children=[relation, instruction, else_instruction], line=line)

class String(Node):
    def __init__(self, string, line=None):
        super().__init__(leaf=string, line=line)

class UMinus(Node):
    def __init__(self, expr, line=None):
        super().__init__(children=[expr], line=line)

class Error(Node):
    def __init__(self, line=None):
        pass
