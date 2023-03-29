import sys
import ply.yacc as yacc
from mparser import parser
from scanner import lexer
from tree_printer import TreePrinter
from type_checker import TypeChecker
from interpreter import Interpreter

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/primes.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    # parser = Mparser
    # parser = yacc.yacc(module=Mparser)
    text = file.read()

    ast = parser.parse(text, lexer=lexer)

    # Below code shows how to use visitor
    typeChecker = TypeChecker()
    isFine = typeChecker.check(ast, verbose=True)

    if isFine:
        interpret = Interpreter()
        interpret.visit(ast)
    else:
        pass
    # ast.accept(Interpreter())
    # in future
    # ast.accept(OptimizationPass1())
    # ast.accept(OptimizationPass2())
    # ast.accept(CodeGenerator())