# parser.out -> se genera solo

# Se importan los tokens generado previamente en el lexer
from lexer import tokens
from ply.yacc import * # analizador sintactico
from pathlib import Path

diccionarioComparadores = {
    ">=":   "BLT",
    ">":   "BLE",
    "<=":   "BGT",
    "<":   "BGE",
    "<>":   "BEQ",
    "==":   "BNE"
}

diccionarioComparadoresNot = {
    ">=":   "BGE",
    ">":   "BGT",
    "<=":   "BLE",
    "<":   "BLT",
    "<>":   "BNE",
    "==":   "BEQ"
}


precedence = (
    ('right', 'OP_ASIGNACION'),
    ('left', 'MENOS'),
    # ('left', 'MAS'),
    ('left', 'MULTIPLICACION', 'DIVISION'),
    ('left', 'A_PARENTESIS', 'C_PARENTESIS'),
)


def p_start(_p:YaccProduction):
    '''start : programa'''
    print('FIN')


def p_programa(p:YaccProduction):
    '''programa : programa sentencia
                | sentencia
    '''
    if len(p) == 3:
        print(f'programa sentencia -> programa')
    else:
        print(f'sentencia -> programa')


def p_sentencia(p:YaccProduction):
    '''sentencia : declaracion
                |  asignacion
    '''
    print(f'{p.slice[1].type} -> sentencia2 ')

def p_declaracion(p:YaccProduction):
    '''declaracion : INIT A_LLAVES decl_lista C_LLAVES
    '''
    print(f'DECLARACION -> INIT A_LLAVES decl_lista C_LLAVES')

# INT this must be changed to type
def p_decl_lista(p:YaccProduction):
    '''decl_lista : var_lista COLON TIPO 
                  | decl_lista  var_lista COLON TIPO
    '''
    print('decl_lista -> var_lista COLON TIPO')

def p_tipo(p:YaccProduction):
    '''TIPO : TIPO_INT
            | TIPO_FLOAT
            | TIPO_STRING
    '''
    print(f'TIPO -> {p.slice[1].type}')
    # p[0] = p[1]

def p_var_lista(p:YaccProduction):
    '''var_lista : ID
                 | var_lista COMA ID
    '''
    if len(p) >= 3:
        print(f'var_lista -> VAR_LISTA COMA ID: {p[3]}')
    else:
        print(f'var_lista -> ID: {p[1]}')

def p_asignacion(p:YaccProduction):
    '''asignacion : ID OP_ASIGNACION expresion
    '''
    print(f'asignacion -> ID:{p.slice[1].value} OP_ASIGNACION expresion')

def p_expresion_menos(p:YaccProduction):
    'expresion : expresion MENOS termino'
    print('expresion - termino -> expresion')


def p_expresion_termino(p:YaccProduction):
    'expresion : termino'
    print('termino -> expresion')


def p_termino_multiplicacion(p:YaccProduction):
    'termino : termino MULTIPLICACION elemento'
    print('termino * elemento -> termino')


def p_termino_division(p:YaccProduction):
    'termino : termino DIVISION elemento'
    print('termino / elemento -> termino')


def p_termino_elemento(p:YaccProduction):
    'termino : elemento'
    print('elemento -> termino')


def p_elemento_expresion(p:YaccProduction):
    'elemento : A_PARENTESIS expresion C_PARENTESIS'
    print('( expresion ) -> elemento')


def p_elemento(p:YaccProduction):
    '''elemento : N_ENTERO
                | ID
    '''
    print(f'{p.slice[1].type} -> elemento')
    p[0] = p[1]


# Error rule for syntax errors
def p_error(p):
    raise Exception(f"Error en la linea {p.lineno or ''} at {p.value or ''}")


def ejecutar_parser():
    # Build the parser
    parser:LRParser = yacc()
    path_parser = Path("./resources/parser_test_2.txt")
    code = path_parser.read_text()
    parser.parse(code)
