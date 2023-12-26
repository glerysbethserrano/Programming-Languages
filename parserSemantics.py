import ply
import ply.lex as lex
import ply.yacc as yacc
import re

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
    'UMINUS',
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

precedence = (
    ('nonassoc', 'MIN', 'MAJ', 'MIN_EQ', 'MAJ_EQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'STAR', 'DIV'),
    ('right', 'UMINUS'),
    ('nonassoc', 'RO', 'RC')
)

# ---------- parser implementation ----------

label_count = 0
assembly_code = []

def process_labels(instructions):
    label_mapping, label_counter = {}, 1
    new_instructions = []

    for instruction in instructions:
        labels = re.findall(r'(LABEL\d+)', instruction)
        for label in labels:
            if label not in label_mapping:
                label_mapping[label] = f'L{label_counter}'
                label_counter += 1
        for label, new_label in label_mapping.items():
            instruction = re.sub(r'\b' + re.escape(label) + r'\b', new_label, instruction)
        new_instructions.append(instruction)

    return new_instructions

def p_prog(p):
    '''prog : decl_list stmt_list'''
    
    for instruction in p[1]:
        assembly_code.append(instruction)

    for instruction in process_labels(p[2]):
        assembly_code.append(instruction)
    assembly_code[-1] += ' END' 

    pass

def p_decl_list(p):
    '''decl_list : empty
                 | decl decl_list
    '''
    if p[1] is None:
        p[0] = None
    elif p[2] is None:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

    pass

def p_empty(p):
    'empty :'
    pass

def p_decl(p):
    '''decl : type var_list S'''
    decl_instructions = [f"{p[1]} {variable}" for variable in p[2]]
    p[0] = decl_instructions

    pass

def p_stmt_list(p):
    '''stmt_list : stmt stmt_list
                 | stmt
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

    pass

def p_stmt(p):
    '''stmt : if_stmt
            | while_stmt
            | block_stmt
            | print_stmt
            | assignment
    '''
    p[0] = p[1]

    pass

def p_if_stmt(p):
    '''if_stmt : IF RO exp RC stmt else_stmt'''
    
    global label_count

    if_instruction = [f'    EVAL {p[3]}', f'    GOTOF LABEL{label_count + 1}']
    statement = p[5]
    if_jump_instruction = [f'LABEL{label_count + 1}:']
    else_instruction = p[6] if p[6] is not None else []
    else_jump_instruction = [f'LABEL{label_count + 2}:'] if p[6] is not None else []

    label_count += 3 if p[6] is not None else 2
    p[0] = if_instruction + statement + if_jump_instruction + else_instruction + else_jump_instruction

    pass

def p_else_stmt(p):
    '''else_stmt : ELSE stmt
                 | empty
    '''
    if p[1] == None:
        p[0] = None
    else:
        p[0] = p[2]
    
    pass

def p_while_stmt(p):
    '''while_stmt : WHILE RO exp RC stmt'''
    
    global label_count

    p[0] = [
    f'LABEL{label_count}: EVAL {p[3]}',
    f'    GOTOF LABEL{label_count + 1}',
] + p[5] + [
    f'    GOTO LABEL{label_count}',
    f'LABEL{label_count + 1}:'
]

    label_count += 2
    
    pass

def p_print_stmt(p):
    '''print_stmt : PRINT exp S'''
    
    p[0] = [f'    PRINT {p[2]}']
    
    pass

def p_block_stmt(p):
    '''block_stmt : BO stmt_list BC'''
    
    p[0] = p[2]
    
    pass

def p_assignment(p):
    '''assignment : id EQ exp S'''
    
    p[0] = [f'    EVAL {p[3]}\n    ASS  {p[1]}']
    
    pass

def p_type(p):
    '''type : INT_TYPE
            | DOUBLE_TYPE
    '''
    if p[1] == 'int': #check
        p[0] = 'INT'
    elif p[1] == 'double':
        p[0] = 'DOUBLE'
    
    pass

def p_var_list(p):
    '''var_list : var
                | var CM var_list
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]
   
    pass

def p_var(p):
    '''var : ID array'''
    
    if p[2] is None:
        p[0] = p[1]
    else:
        p[0] = f'{p[1]}{p[2]}'
    
    pass

def p_array(p):
    '''array : empty
             | SO INT SC array
    '''
    if p[1] == None:
        p[0] = None
    else:
        if p[4] is None:
            p[0] = f'[{p[2]}]'
        else:
            p[0] = f'[{p[2]}]{p[4]}'
   
    pass

def p_id_array(p):
    '''id_array : SO INT SC id_array
                | SO id SC id_array
                | empty
    '''
    if len(p) == 5:
        if p[4] is None:
            p[0] = f'[{p[2]}]'
        else:
            p[0] = f'[{p[2]}] {p[4]}'
    else:
        p[0] = None
    
    pass

def p_id(p):
    '''id : ID
          | ID id_array
    '''
    if p[2] is not None:
        p[0] = f'{p[1]}{p[2]}'
    else:
        p[0] = f'{p[1]}'
    
    pass

def p_exp(p):
    '''exp : RO exp RC
           | condition
           | arithmetic
           | number_id
           | unumber_id
    '''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

    pass 

def p_condition(p):
    '''condition : NOT exp
                 | exp OR exp
                 | exp AND exp
                 | exp MIN exp
                 | exp MAJ exp
                 | exp EQ EQ exp
                 | exp MAJ_EQ exp
                 | exp MIN_EQ exp
    '''
    if len(p) == 3:
        p[0] = f'{p[2]} {p[1]}'
    elif len(p) == 4: 
        p[0] = f'{p[3]} {p[1]} {p[2]}'
    elif len(p) == 5: 
        p[0] = f'{p[1]} {p[4]} =='
    
    pass

def p_arithmetic(p):
    '''arithmetic : exp PLUS exp
                  | exp MINUS exp
                  | exp STAR exp
                  | exp DIV exp
    '''
    p[0] = f'{p[3]} {p[1]} {p[2]}'
    
    pass

def p_number_id(p):
    '''number_id : id 
                 | INT
                 | DOUBLE
    '''
    p[0] = f'{p[1]}'

    pass

def p_unumber_id(p):
    '''unumber_id : UMINUS
                  | exp UMINUS
                  | MINUS exp %prec UMINUS
    '''
    if len(p) == 2:
        p[0] = f'{p[1]}'
    elif p[1] == '-':
        p[0] = f'0 {p[2]} -'
    else:
        p[0] = f'{p[1]} {p[2]} +'
   
    pass

def p_error(p):
    print(f"Syntax error at line {p.lineno}, position {p.lexpos}, token {p.type}")

textFile = open('Test_program.txt', 'r')
data = textFile.read()

lexer = lex.lex()
lexer.input(data)

parser = yacc.yacc()
result = parser.parse(data)

for code in assembly_code:
    print(code)