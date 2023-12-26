import ply.lex as lex

reserved_keywords = {
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'int' : 'INT_TYPE',
    'double' : 'DOUBLE_TYPE',
    'print' : 'PRINT'
}

tokens = [
    'ID',
    'INT',
    'DOUBLE',
    'COMMENT',
    'WHITESPACE',
    'RO',
    'RC',
    'BO',
    'BC',
    'SO',
    'SC',
    'EQ',
    'NOT',
    'OR',
    'AND',
    'MIN',
    'MAJ',
    'MIN_EQ',
    'MAJ_EQ',
    'PLUS',
    'MINUS',
    'STAR',
    'DIV',
    'CM',
    'S',
] + list(reserved_keywords.values())

t_RO = r'\('
t_RC = r'\)'
t_BO = r'\{'
t_BC = r'\}'
t_SO = r'\['
t_SC = r'\]'
t_EQ = r'='
t_NOT = r'!'
t_OR = r'\|'
t_AND = r'\&'
t_MIN = r'<'
t_MAJ = r'>'
t_MIN_EQ = r'<='
t_MAJ_EQ = r'>='
t_PLUS = r'\+'
t_MINUS = r'-' 
t_STAR = r'\*'
t_DIV = r'/'
t_CM = r','
t_S = r';'

t_ignore  = ' \t'
t_ignore_COMMENT = r'\#.*'

def t_ignore_DOUBLE_SLASH_COMMENT(t):
    r'\/\/.*'

def t_NEWLINE(t):
    r'[\n]+'
    t.lexer.lineno += len(t.value)

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved_keywords.get(t.value, 'ID')
    return t

def t_DOUBLE(t):
    r'[-?[0-9]*\.[0-9]+|-[0-9]+]'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_WHITESPACE(t):
    r'[ \t\n\r]+'
    pass

def t_error(t):
    print("Invalid Token:", t.value[0])
    pass

lexer = lex.lex()

textFile = open('Test_program.txt', 'r')
data = textFile.read()

lexer.input(data)

while True:
    token = lexer.token()
    if not token:
        break
    print(f"Token Type: {token.type}, Value: {token.value}, Line: {token.lineno}")
