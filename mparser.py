#!/usr/bin/python
from distlib.compat import raw_input

import scanner
import ply.yacc as yacc
from mAST import *

tokens = scanner.tokens

precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('nonassoc', '=', 'SUBASSIGN', 'ADDASSIGN', 'MULASSIGN', 'DIVASSIGN'),
    ("right", ':'),
    ("left", 'LT', 'GT', 'LE', 'GE', 'NE', 'EQ'),
    ("left", '+', '-'),
    ("left", '*', '/'),
    ('left', 'DOTADD', 'DOTSUB'),
    ('left', 'DOTMUL', 'DOTDIV'),
    ("right", 'ID', '['),
    ('right', 'UMINUS'),
    ('left', "\'")
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""
    p[0] = Program([p[1]])

def p_instructions_opt(p):
    """instructions_opt : instructions
                        | empty"""
    p[0] = Instructions([p[1]])

def p_instructions(p):
    """instructions : instructions instruction
                    | instruction """
    if len(p) == 3:
        p[0] = Instructions(p[1].children+[p[2]])
    else:
        p[0] = Instructions([p[1]])


def p_empty(p):
    """empty :"""
    pass


def p_instruction(p):
    """instruction : instruction_block
                   | assignment ';'
                   | relation ';'
                   | expression ';'
                   | break ';'
                   | continue ';'
                   | return ';'
                   | print ';'
                   | if
                   | while
                   | for
                   | ';' """
    p[0] = Instruction(p[1])

def p_instruction_block(p):
    """instruction_block : '{' instructions '}'"""
    p[0] = Instruction(p[2])

def p_break(p):
    """break : BREAK"""
    p[0] = Break(line=p.lexer.lineno)

def p_continue(p):
    """continue : CONTINUE"""
    p[0] = Continue(line=p.lexer.lineno)

def p_return(p):
    """return : RETURN
              | RETURN expression"""
    p[0] = Return(name=p[1], expression=p[1:], line=p.lexer.lineno)

def p_print(p):
    """print : PRINT value_list"""
    p[0] = Print(p[2], line=p.lexer.lineno)


def p_assignment(p):
    """assignment : var assign_op expression
                  | ref assign_op expression """
    p[0] = Assignment(p[1], p[2], p[3], line=p.lexer.lineno)


def p_assign_op(p):
    """assign_op : '='
                 | ADDASSIGN
                 | SUBASSIGN
                 | MULASSIGN
                 | DIVASSIGN"""
    p[0] = p[1]

def p_var(p):
    """var : ID"""
    p[0] = Variable(p[1], line=p.lexer.lineno)


def p_ref(p):
    """ref : ID '[' value_list ']' """
    p[0] = Reference(p[1], p[3:4], line=p.lexer.lineno)

def p_expression_binop(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression"""

    p[0] = BinOp(p[1], p[2], p[3], line=p.lexer.lineno)

def p_expression_group(p):
    """expression : '(' expression  ')' """
    p[0] = p[2]


def p_expression(p):
    """expression : var
                 | ref
                 | number
                 | list
                 | function
                 | string"""
    p[0] = p[1]

def p_string(p):
    """string : STRING"""
    p[0] = String(p[1][1:-1], line=p.lexer.lineno)

def p_function(p):
    """function : ZEROS '(' value_list ')'
                | EYE '(' value_list ')'
                | ONES '(' value_list ')'"""
    p[0] = Function(p[1], ValueList([p[3]], line=p.lexer.lineno), line=p.lexer.lineno)

def p_list(p):
    """list : '[' value_list ']'
            | '[' ']' """

    p[0] = List(p[2:3], line=p.lexer.lineno)

def p_value_list(p):
    """value_list : value_list ',' expression
                  | expression"""
    if len(p) == 2:
        p[0] = ValueList([p[1]], line=p.lexer.lineno)
    else:
        p[0] = ValueList(p[1].children + [p[3]], line=p.lexer.lineno)

def p_expression_transpose(p):
    """expression : expression "'" """
    p[0] = Transpose(p[1], line=p.lexer.lineno)


def p_number_float(p):
    """number : FLOAT"""
    p[0] = Number(FloatNum(p[1], line=p.lexer.lineno), line=p.lexer.lineno)


def p_number_int(p):
    """number : INT"""
    p[0] = Number(IntNum(p[1], line=p.lexer.lineno), line=p.lexer.lineno)


def p_expr_uminus(p):
    """expression : '-' expression %prec UMINUS"""
    p[0] = UMinus(p[2], line=p.lexer.lineno)

def p_relation(p):
    """relation : expression LT expression
                | expression GT expression
                | expression LE expression
                | expression GE expression
                | expression NE expression
                | expression EQ expression"""
    p[0] = Relation(p[1], p[2], p[3], line=p.lexer.lineno)

def p_instruction_if(p):
    """if : IF '(' relation ')' instruction %prec IFX
          | IF '(' relation ')' instruction ELSE instruction"""

    if len(p) > 6:
        p[0] = If(p[3], p[5], p[7], line=p.lexer.lineno)
    else:
        p[0] = If(p[3], p[5], line=p.lexer.lineno)

def p_instruction_while(p):
    """while : WHILE '(' relation ')' instruction"""
    p[0] = While(p[3], p[5], line=p.lexer.lineno)


def p_range(p):
    """range : expression ':' expression"""

    p[0] = Range(p[1], p[3], line=p.lexer.lineno)

def p_instruction_for(p):
    """for : FOR ID '=' range instruction"""
    p[0] = For(Variable(p[2]), p[4], p[5], line=p.lexer.lineno)

parser = yacc.yacc()

if __name__ == '__main__':
    while True:
        try:
            s = raw_input('calc > ')
        except EOFError:
            break
        if not s: continue
        result = parser.parse(s)
        print(result)