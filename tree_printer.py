from __future__ import print_function
import mAST


def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

def addToClasses(*classes):
    def decorator(func):
        for cls in classes:
            setattr(cls, func.__name__, func)
    return decorator

def print_with_indent(indent, to_print):
    print(f"{'|  ' * indent}{to_print}")

class TreePrinter:

    @addToClass(mAST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClasses(mAST.Program, mAST.Instructions, mAST.Instruction)
    def printTree(self, indent=0):
        for child in self.children:
            child.printTree(indent)


    @addToClass(mAST.Number)
    def printTree(self, indent=0):
        print_with_indent(indent, self.leaf.leaf)


    @addToClass(mAST.IntNum)
    def printTree(self, indent=0):
        print_with_indent(indent, self.leaf)

    @addToClasses(mAST.Assignment, mAST.BinOp, mAST.Relation)
    def printTree(self, indent=0):
        print_with_indent(indent, self.leaf)
        self.children[0].printTree(indent+1)
        self.children[1].printTree(indent+1)

    @addToClass(mAST.Variable)
    def printTree(self, indent=0):
        print_with_indent(indent, self.leaf)

    @addToClass(mAST.Reference)
    def printTree(self, indent=0):
        print_with_indent(indent, 'REF')
        print_with_indent(indent+1, self.leaf)
        for child in self.children:
            child.printTree(indent + 1)

    @addToClass(mAST.List)
    def printTree(self, indent=0):
        print_with_indent(indent, 'VECTOR')
        for child in self.children:
            child.printTree(indent+1)

    @addToClass(mAST.ValueList)
    def printTree(self, indent=0):
        for child in self.children:
            child.printTree(indent)

    @addToClass(mAST.Transpose)
    def printTree(self, indent=0):
        print_with_indent(indent, 'TRANSPOSE')
        self.leaf.printTree(indent+1)


    @addToClass(mAST.Function)
    def printTree(self, indent=0):
        print_with_indent(indent, self.leaf)
        for arg in self.children:
            arg.printTree(indent+1)

    @addToClass(mAST.For)
    def printTree(self, indent=0):
        print_with_indent(indent, 'FOR')
        self.children[0].printTree(indent+1)
        self.children[1].printTree(indent+1)
        self.children[2].printTree(indent+1)


    @addToClass(mAST.While)
    def printTree(self, indent=0):
        print_with_indent(indent, 'WHILE')
        self.children[0].printTree(indent+1)
        self.children[1].printTree(indent+1)

    @addToClass(mAST.Range)
    def printTree(self, indent=0):
        print_with_indent(indent, 'RANGE')
        self.children[0].printTree(indent+1)
        self.children[1].printTree(indent+1)

    @addToClass(mAST.Print)
    def printTree(self, indent=0):
        print_with_indent(indent, 'PRINT')
        for child in self.children:
            child.printTree(indent+1)

    @addToClass(mAST.String)
    def printTree(self, indent=0):
        print_with_indent(indent, self.leaf)

    @addToClass(mAST.UMinus)
    def printTree(self, indent=0):
        print_with_indent(indent, 'UMINUS')
        self.children[0].printTree(indent + 1)

    @addToClass(mAST.If)
    def printTree(self, indent=0):
        print_with_indent(indent, 'IF')
        self.children[0].printTree(indent+1)
        print_with_indent(indent, 'THEN')
        self.children[1].printTree(indent+1)
        if self.children[2]:
            print_with_indent(indent, 'ELSE')
            self.children[2].printTree(indent + 1)

    @addToClass(mAST.Error)
    def printTree(self, indent=0):
        pass
        # fill in the body


    # define printTree for other classes
    # ...
