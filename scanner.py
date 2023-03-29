import ply.lex as lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT'}

literals = ['+', '-', '*', '/', '=', '(', ')', '[', ']', '{', '}', ':', '\'', ',', ';']

tokens = ['DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV', # macierzowe operatory binarne
          'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN', # operatory przypisania
          'LT', 'GT', 'LE', 'GE', 'NE', 'EQ', # operatory relacyjne
          'ID', # identyfikatory
          'INT', # liczby całkowite
          'FLOAT', # liczby zmiennoprzecinkowe
          'STRING' # stringi
          ] + list(reserved.values())

t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'

t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='

t_LE = r'<='
t_GE = r'>='
t_NE = r'!='
t_EQ = r'=='
t_LT = r'<'
t_GT = r'>'

def t_COMMENT(t):
    r'\#.*'

def t_FLOAT(t):
    r'((\.\d+)|(\d+\.\d*))([eE][+-]?\d+)?'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'0|([1-9][0-9]*)'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t

def t_STRING(t):
    r'\".*?\"'
    t.value = str(t.value)
    return t


def t_error(t) :
    print("Illegal character '%s'" %t.value[0])
    t.lexer.skip(1)



lexer = lex.lex()