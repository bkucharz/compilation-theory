import numpy as np

import mAST
import symbol_table
from memory import *
from exeptions import  *
from operations import operations
from visit import *
import sys
from memory import MemoryStack

class Interpreter(object):

    def __init__(self):
        self.memory_stack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass


    @when(mAST.Program)
    def visit(self, node):
        for child in node.children:
            self.visit(child)


    @when(mAST.Instructions)
    def visit(self, node):
        for child in node.children:
            self.visit(child)


    @when(mAST.Instruction)
    def visit(self, node):
        self.visit(node.children[0])

    @when(mAST.BinOp)
    def visit(self, node):
        r1 = self.visit(node.children[0])
        r2 = self.visit(node.children[1])
        return operations[node.leaf](r1, r2)


    @when(mAST.Print)
    def visit(self, node):
        vals = self.visit(node.children[0])
        print(*vals)

    @when(mAST.ValueList)
    def visit(self, node):
        vals = []
        for value in node.children:
            vals.append(self.visit(value))
        return vals

    @when(mAST.Variable)
    def visit(self, node):
        return self.memory_stack.get(node.leaf)


    @when(mAST.Reference)
    def visit(self, node):
        indexes = self.visit(node.children[0])
        return self.memory_stack.get(node.leaf)[(*indexes,)]

    @when(mAST.String)
    def visit(self, node):
        return node.leaf

    @when(mAST.Number)
    def visit(self, node):
        return node.leaf.leaf

    @when(mAST.Assignment)
    def visit(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        new_val = operations[node.leaf](left, right)
        if isinstance(node.children[0], mAST.Variable):
            self.memory_stack.set(node.children[0].leaf, new_val)
        elif isinstance(node.children[0], mAST.Reference):
            var = self.memory_stack.get(node.children[0].leaf)
            indexes = self.visit(node.children[0].children[0])
            var[(*indexes,)] = new_val


    @when(mAST.For)
    def visit(self, node):
        self.memory_stack.push(Memory('for'))
        mrange = self.visit(node.children[1])
        range_id = node.children[0].leaf
        for i in range(*mrange):
            try:
                self.memory_stack.set(range_id, i)
                self.visit(node.children[2])
            except BreakException:
                break
            except ContinueException:
                continue
        self.memory_stack.pop()


    @when(mAST.While)
    def visit(self, node):
        self.memory_stack.push(Memory('while'))
        status = self.visit(node.children[0])
        while status:
            try:
                self.visit(node.children[1])
                status = self.visit(node.children[0])
            except BreakException:
                break
            except ContinueException:
                continue
        self.memory_stack.pop()


    @when(mAST.If)
    def visit(self, node):
        self.memory_stack.push(Memory('if'))
        status = self.visit(node.children[0])
        if status:
            self.visit(node.children[1])
        else:
            self.visit(node.children[2])

        self.memory_stack.pop()


    @when(mAST.Range)
    def visit(self, node):
        return (self.visit(node.children[0]), self.visit(node.children[1]))

    @when(mAST.Relation)
    def visit(self, node):
        l = self.visit(node.children[0])
        r = self.visit(node.children[1])
        return operations[node.leaf](l, r)

    @when(mAST.Function)
    def visit(self, node):
        to_return = None
        params = self.visit(node.children[0].children[0])
        if node.leaf == 'eye':
            to_return = np.eye(*params)
        elif node.leaf == 'ones':
            to_return = np.ones(params)
        elif node.leaf == 'zeros':
            to_return = np.zeros(params)

        return to_return
