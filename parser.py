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
    ('left', 'MAS'),
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
        print('programa sentencia -> programa')
    else:
        print('sentencia -> programa')


def p_sentencia(p:YaccProduction):
    '''sentencia : declaracion
                |  asignacion
                |  iteracion
    '''
    print(f'{p.slice[1].type} -> sentencia')

def p_declaracion(p:YaccProduction):
    '''declaracion : INIT A_LLAVES decl_lista C_LLAVES
    '''
    print('INIT A_LLAVES decl_lista C_LLAVES -> DECLARACION')

# INT this must be changed to type
def p_decl_lista(p:YaccProduction):
    '''decl_lista : var_lista COLON TIPO 
                  | decl_lista  var_lista COLON TIPO
    '''
    print('var_lista COLON TIPO -> decl_lista')

def p_tipo(p:YaccProduction):
    '''TIPO : TIPO_INT
            | TIPO_FLOAT
            | TIPO_STRING
    '''
    print(f'{p.slice[1].type}-> TIPO')
    p[0] = p[1]

def p_var_lista(p:YaccProduction):
    '''var_lista : ID
                 | var_lista COMA ID
    '''
    if len(p) >= 3:
        print(f'VAR_LISTA COMA ID: {p[3]} -> var_lista')
    else:
        print(f'ID: {p[1]} -> var_lista')

def p_asignacion(p:YaccProduction):
    '''asignacion : ID OP_ASIGNACION expresion
    '''
    print(f'ID:{p.slice[1].value} OP_ASIGNACION expresion -> asignacion')

def p_iteracion(p:YaccProduction):
    '''iteracion : WHILE A_PARENTESIS condicion C_PARENTESIS A_LLAVES programa C_LLAVES
    '''
    print('WHILE A_PARENTESIS condicion C_PARENTESIS A_LLAVES programa C_LLAVES -> iteracion')

def p_condicion(p:YaccProduction):
    '''condicion : condicion OR conjuncion
                 | conjuncion
    '''
    if len(p) >= 3:
        print(f' condicion OR conjuncion -> condicion')
    else:
        print(f'conjuncion -> condicion')

def p_conjuncion(p:YaccProduction):
    '''conjuncion : conjuncion AND termino_logico
                  | termino_logico
    '''
    if len(p) >= 3:
        print(f'conjuncion AND termino_logico -> conjuncion')
    else:
        print(f'termino_logico -> conjuncion')

def p_termino_logico(p:YaccProduction):
    '''termino_logico : comparacion
                      | NOT termino_logico
                      | A_PARENTESIS condicion C_PARENTESIS
    '''
    if len(p) == 4:
        print(f'A_PARENTESIS condicion C_PARENTESIS -> termino_logico')
    elif len(p) == 3:
        print(f'NOT termino_logico -> termino_logico')
    elif len(p) == 2:
        print(f'comparacion -> termino_logico')

def p_comparacion(p:YaccProduction):
    '''comparacion : expresion comparador expresion
    '''
    print('expresion comparador expresion -> comparacion')

def p_comparador(p:YaccProduction):
    '''comparador : IGUAL
                  | DISTINTO
                  | MAYOR
                  | MENOR
                  | MAYOR_IGUAL
                  | MENOR_IGUAL
    '''
    print(f'{p.slice[1].type}({p.slice[1].value}) -> comparador')

def p_expresion_menos(p:YaccProduction):
    'expresion : expresion MENOS termino'
    print('expresion - termino -> expresion')

def p_expresion_mas(p:YaccProduction):
    'expresion : expresion MAS termino'
    print('expresion + termino -> expresion')

def p_expresion_termino(p:YaccProduction):
    'expresion : termino'
    print('termino -> expresion\n')


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
                | N_FLOAT
                | ID
    '''
    print(f'\n{p.slice[1].type}:{p.slice[1].value} -> elemento')
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
