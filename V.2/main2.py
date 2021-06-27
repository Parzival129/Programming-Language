from ply import lex, yacc
import sys
import os
import time

print(f"Running script: {sys.argv[1]}")
print ("")
time.sleep(1)

tokens = (
    'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN',
)

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print(f"Integer value too large: {t.value}")
        t.value = 0
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character {t.value[0]!r} on line {t.lexer.lineno}")
    t.lexer.skip(1)

t_ignore = ' \t'

lexer = lex.lex()

# Parsing

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

def p_error(t):
    if t is None: # lexer error
        return
    print(f"Syntax Error: {t.value!r}")

parser = yacc.yacc()

if __name__ == "__main__":

    # that nice looking progress bar!

    from alive_progress import alive_bar
    from time import sleep

    with alive_bar(100) as bar:
        print ("[ Processing Operations... ]")
        for i in range(100):
            sleep(0.0092)
            bar()

    os.system("cls")

    print ("Output: ")
    print ("")

    while True:

        file1 = open(sys.argv[1], 'r')
        Lines = file1.readlines()

        for line in Lines:
            print(parser.parse(line))
        print ("done")
        exit()
        quit()
        break