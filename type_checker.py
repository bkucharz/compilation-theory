import mAST
from symbol_table import Symbol, SymbolTable, Type

class NodeVisitor(object):
    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, mAST.Node):
                            self.visit(item)
                elif isinstance(child, mAST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)


class TypeChecker(NodeVisitor):

    def __init__(self):
        super().__init__()
        self.all_correct = True

    def check(self, ast, verbose=False):
        self.all_correct = True
        self.visit(ast)
        if verbose:
            if self.all_correct:
                print("OK no errors")
            else:
                print("ERROR, do not interpret")
        return self.all_correct

    def put_symbol(self, name, symbol_type, symbol_size=None):
        self.symbol_table.put(name, Symbol(name, symbol_type, symbol_size))

    def visit_and_push_scope(self, node, scope_name):
        self.symbol_table.push_scope(scope_name)
        for child in node.children:
            self.visit(child)
        self.symbol_table.pop_scope()


    def visit_Program(self, node):
        self.visit_and_push_scope(node, "program")


    def visit_Number(self, node):
        self.visit(node.leaf)
        node.type = node.leaf.type

    def visit_IntNum(self, node):
        node.type = Type.INT


    def visit_FloatNum(self, node):
        node.type = Type.FLOAT

    def visit_String(self, node):
        node.type = Type.STRING

    def visit_UMinus(self, node):
        self.visit(node.children[0])
        node.type = node.children[0].type

    def visit_Expression(self, node):
        self.visit(node.children[0])

    def visit_BinOp(self, node):
        left = node.children[0]
        right = node.children[1]
        op = node.leaf
        self.visit(left)
        self.visit(right)
        binop_type = self._get_binop_type(left, right, op)
        if binop_type is None:
            self.error(node.line, f"Wrong types: {left.type} ! {right.type}")
        else:
            node.type = binop_type
            node.size = left.size
            self._check_binop(left, right, op, node.line, node.type)

    def _get_binop_type(self, left, right, op):
        if left.type == right.type:
            return left.type
        elif (left.type == Type.STRING and Type.is_number(right.type)) or (right.type == Type.STRING and Type.is_number(left.type)):
            if op in ['*', '*=']:
                return Type.STRING
        elif Type.is_number(left.type) and Type.is_number(right.type):
            return Type.FLOAT
        return None

    def _check_binop(self, left, right, op, line, types):

        if op in ['.+', './', '.*', '.-'] and types not in [Type.VECTOR, Type.MATRIX]:
            self.error(line, f"Operation '{op}' undefined for type {types}")
        if left.type == Type.MATRIX:
            if op in ['-', '+', '.+', './', '.*', '.-'] and left.size != right.size:
                self.error(line,
                      f"Different sizes ({left.size} ! {right.size}) for '{op}' operation  ")
            if op in ['*', '/']:
                if len(left.size) != len(right.size) or left.size[1] != right.size[0]:
                    self.error(line,
                          f"Different sizes  ({left.size} ! {right.size}) for '{op}' operation ")


    def visit_Variable(self, node):
        symbol = self.symbol_table.get(node.leaf)
        if symbol is not None:
            node.type = symbol.type
            node.size = symbol.size
        else:
            node.type = Type.NULL  # id doesnt yet exist


    def visit_Assignment(self, node):
        self.visit(node.children[0])
        self.visit(node.children[1])
        if isinstance(node.children[0], mAST.Variable):
            if node.children[0].type == Type.NULL and node.leaf != '=':
                self.error(node.line, "Operation with not initialized variable")
            else:
                if node.leaf == '=':
                    node.children[0].type = node.children[1].type
                    node.children[0].size = node.children[1].size

                    # print()
                    # print('right', node.children[1].leaf, node.children[1].size, node.children[1].type)
                    # print('left', node.children[0].leaf, node.children[0].size, node.children[0].type)
                    self.put_symbol(node.children[0].leaf, node.children[1].type, node.children[0].size)

                if node.leaf != '=':
                    binop_type = self._get_binop_type(node.children[0], node.children[1], node.leaf)
                    if binop_type is None:
                        self.error(node.line, f"Wrong types for {node.leaf} operation: {node.children[0].type} ! {node.children[1].type}")
                    else:
                        node.type = binop_type
                        self._check_binop(node.children[0], node.children[1], node.leaf[0], node.line, node.type)

    def visit_Function(self, node):
        self.visit(node.children[0])
        values = node.children[0].children[0].children
        if node.leaf == 'eye' and len(values) == 1:
            node.size = (values[0].leaf.leaf, values[0].leaf.leaf)
        else:
            node.size = tuple(v.leaf.leaf for v in values)
        node.type = Type.MATRIX

    def visit_List(self, node):
        value_list = node.children[0]
        self.visit(value_list)
        node.size = value_list.size
        node.type = Type.MATRIX

    def visit_ValueList(self, node):
        self.visit(node.children[0])
        size = node.children[0].size
        for child in node.children[1:]:
            self.visit(child)
            if size != child.size:
                self.error(child.line, "wrong size of matrix")

        if not (node.children[0].type == Type.MATRIX):
            node.size = (len(node.children),)
        else:
            node.size = (len(node.children), *node.children[0].size)


    def visit_Reference(self, node):
        name = node.leaf
        if symbol := self.symbol_table.get(name):
            if symbol.type != Type.MATRIX:
                self.error(node.line, f"Cannot index {symbol.type}")
                return
        else:
            self.error(node.line, f"Reference to not initialized variable {name}")
            return

        value_list = node.children[0]
        if len(value_list.children) > len(symbol.size):
            self.error(node.line, f"Too many indexes")
        else:
            for i, child in enumerate(value_list.children):
                self.visit(child)
                if child.type != Type.INT:
                    self.error(child.line, f"Matrix indexes should be integers, {child.type} given")
                else:
                    value = child.leaf.leaf
                    if not (0 <= value < symbol.size[i]):
                        self.error(node.line, f'Index out of range')


    def visit_While(self, node):
        self.visit_and_push_scope(node, 'while')


    def visit_For(self, node):
        self.visit(node.children[0])
        self.visit(node.children[1])
        self.put_symbol(node.children[0].leaf, Type.INT)
        self.symbol_table.push_scope("for")
        self.visit(node.children[2])
        self.symbol_table.pop_scope()

    def visit_Range(self, node):
        self.visit(node.children[0])
        self.visit(node.children[1])
        node.type = Type.RANGE
        if node.children[0].type != Type.INT or node.children[1].type != Type.INT:
            self.error(node.pos, f"Range must be defined with integers, given {node.fr.type}, {node.to.type}")

    def visit_Break(self, node):
        if not self.symbol_table.is_in_loop():
            self.error(node.line, "'break' outside loop")

    def visit_Continue(self, node):
        if not self.symbol_table.is_in_loop():
            self.error(node.line, "'continue' outside loop")


    def error(self, line, message):
        self.all_correct = False
        print(f"[line {line}]: {message}")
