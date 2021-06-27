from sly import Lexer
from sly import parser
import sys
import os
import time
import math
# this is a test
print(f"Running script: {sys.argv[1]}")
print ("")
time.sleep(1)
STRING = None
NAME = None
class BasicLexer(Lexer):
    tokens = { NAME, NUMBER, STRING, PRINTR }
    ignore = '\t '
    literals = { '=', '+', '-', '/', '>', '<', ':', '^', '@', '#',
                '*', '(', ')', ',', ';', '}', '?', '{', ':', 'p', '[', ']'}
    # define tokens as regular expressions
    # (stored as raw strings)
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'
    PRINTR = r'\[.*?\]'

    # Number token
    @_(r'\d+')
    def NUMBER(self, t):

        # convert it into a python integer
        t.value = int(t.value)
        return t

    # Comment token
    @_(r'//.*')
    def COMMENT(self, t):
        pass

    # Newline token(used only for showing
    # errors in new line)
    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')

class BasicParser(Parser):

    # place the op character in ""
    # extra stuff goes in ''

    #tokens are passed from lexer to parser
    tokens = BasicLexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.env = { }

    @_('')
    def statement(self, p):
        pass

    @_('var_assign')
    def statement(self, p):
        return p.var_assign


    @_('NAME "=" expr')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.expr)

    @_('NAME ">" STRING')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.STRING)
    
    @_('expr')
    def statement(self, p):
        return (p.expr)

    @_('expr "+" expr')
    def expr(self, p):
        return ('add', p.expr0, p.expr1)

    @_('"^" expr')
    def expr(self, p):
        return ('square', p.expr)

    @_('expr "-" expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    @_('expr "/" STRING')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    # declare a function
    @_('NAME "}" STRING')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.STRING)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr

    @_('"@" NAME')
    def expr(self, p):
        return ('var', p.NAME)

    # call a function
    @_('"?" NAME')
    def expr(self, p):
        return ('func', p.NAME)

    @_('"#" PRINTR')
    def statement(self, p):
        pass

    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)

    @_('":" PRINTR')
    def expr(self, p):
        print (p.PRINTR)
        return ('print', p.PRINTR)

class BasicExecute:

    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int):
            print(result)
        if isinstance(result, str) and result[0] == '"':
            print(result)

    def walkTree(self, node):

        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == 'program':
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        if node[0] == 'num':
            return node[1]
            print (node[1])

        if node[0] == 'str':
            return node[1]

        if node[0] == 'comment_assign':
            pass

        # define math tokens.kn jkijopj

        if node[0] == 'square':
            num = (self.walkTree(node[1])) ** 0.5
            # print (math.sqrt(self.walkTree(node[1])))
            return math.sqrt(self.walkTree(node[1]))

        if node[0] == 'add':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'mul':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'div':
            return self.walkTree(node[1]) / self.walkTree(node[2])

        if node[0] == 'var_assign':
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        if node[0] == 'name_assign':
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        if node[0] == 'func_assign':
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Undefined variable '"+node[1]+"' found!")
                return 0

        if node[0] == 'print':
            return node[1]
            print (node[1])

        # call a function

        if node[0] == 'func':
            try:
                return self.env[node[1]]
                print (node[1])
            except LookupError:
                print("Undefined function '"+node[1]+"' found!")
                return 0

if __name__ == '__main__':
    # time.sleep(20)
    # that nice looking progress bar!

    from alive_progress import alive_bar
    from time import sleep

    with alive_bar(100) as bar:
        print ("[ Processing Operations... ]")
        for i in range(100):
            sleep(0.0092)
            bar()


    print ("Output: ")
    print ("")

    lexer = BasicLexer()
    parser = BasicParser()
    env = {}

    # Using readlines() 
    file1 = open(sys.argv[1], 'r') 
    Lines = file1.readlines() 

    count = 0
    # Strips the newline character 
    for line in Lines: 

            tree = parser.parse(lexer.tokenize(line))
            BasicExecute(tree, env)
