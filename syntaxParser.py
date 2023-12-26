import ply
import ply.lex as lex
import ply.yacc as yacc

# ---------- lexer implementation ----------

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
    'EQ_EQ', # added
    'NOT',
    'OR',
    'AND',
    'MIN',
    'MAJ',
    'MIN_EQ',
    'MAJ_EQ',
    'EQ_MIN', # added
    'EQ_MAJ', # added
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
t_EQ_EQ = r'==' # added 
t_NOT = r'!'
t_OR = r'\|'
t_AND = r'\&'
t_MIN = r'<'
t_MAJ = r'>'
t_MIN_EQ = r'<='
t_MAJ_EQ = r'>='
t_EQ_MIN = r'=<' # added
t_EQ_MAJ = r'=>' # added
t_PLUS = r'\+'
t_MINUS = r'\-' 
t_STAR = r'\*'
t_DIV = r'/'
t_CM = r','
t_S = r';'

t_ignore  = ' \t'
t_ignore_COMMENT = r'\#.*'

def t_ignore_DOUBLE_SLASH_COMMENT(t):
    r'\/\/.*'
    pass

def t_NEWLINE(t):
    r'[\n]+'
    t.lexer.lineno += len(t.value)
    pass

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved_keywords.get(t.value, 'ID')
    return t

def t_DOUBLE(t):
    r'-?[1-9]+\.[0-9]*([eE][-+]?[0-9]+)?'
    return t

def t_INT(t):
    r'[0-9][0-9]*'
    return t

def t_WHITESPACE(t):
    r'[ \t\n\r]+'
    pass

def t_error(t):
    print("Invalid Token:", t.value[0])
    pass

# added
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'STAR', 'DIV'),
    ('right', 'UMINUS'),
)

# ---------- parser implementation ----------

start = 'prog'


def p_prog(p):
    '''prog : decl_list stmt_list'''
    pass

def p_empty(p):
    '''empty :'''
    pass

def p_decl_list(p):
    '''decl_list : empty
                 | decl_list decl
    '''
    pass

def p_decl(p):
    '''decl : type var_list S'''
    pass

def p_stmt_list(p):
    '''stmt_list : stmt_list stmt
                 | stmt
    '''
    pass

def p_stmt(p):
    '''stmt : IF RO exp RC stmt
            | ELSE stmt
            | WHILE RO exp RC stmt
            | assignment
            | PRINT exp S
            | BO stmt_list BC
    '''
    pass

def p_assignment(p):
    '''assignment : id S
                  | id EQ exp S
    '''
    pass

def p_type(p):
    '''type : DOUBLE_TYPE
            | INT_TYPE
    '''
    pass

def p_var_list(p):
    '''var_list : var
                | var_list CM var
    '''
    pass

def p_var(p):
    '''var : ID array'''
    pass

def p_array(p):
    '''array : empty
             | SO INT SC
    '''
    pass

def p_id(p):
    '''id : ID
          | ID SO INT SC
          | ID SO ID SC
    '''
    pass

def p_exp(p):
    '''exp : exp AND exp
           | exp OR exp
           | NOT exp
           | exp EQ EQ exp
           | exp MIN exp
           | exp MAJ exp
           | exp MAJ_EQ exp
           | exp EQ_MAJ exp
           | exp MIN_EQ exp
           | exp EQ_MIN exp
           | exp PLUS exp
           | exp MINUS exp
           | MINUS exp %prec UMINUS
           | exp STAR exp
           | exp DIV exp
           | RO exp RC
           | id
           | DOUBLE
           | INT
    '''
    pass

def p_error(p):
    print(f"Syntax error: Line = {p.lineno}, Position = {p.lexpos}, Value = {p.type}")

lexer = lex.lex()
parser = yacc.yacc()

textFile = open('Test_program.txt', 'r')
data = textFile.read()

lexer.input(data)
parser.parse(data)

