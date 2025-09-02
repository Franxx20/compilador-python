import logging
# parser.out -> se genera solo

# Se importan los tokens generado previamente en el lexer
from lexer import tokens, lexer
from ply.yacc import * # analizador sintactico
from pathlib import Path
from SymbolTableGenerator import stg, SymbolTableObject

# Configure logging at the top of the file
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

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
    stg.generate_file()

    logging.info('FIN')


def p_programa(p:YaccProduction):
    '''programa : programa sentencia
                | sentencia
    '''
    if len(p) == 3:
        logging.info('programa sentencia -> programa')
    else:
        logging.info('sentencia -> programa')


def p_sentencia(p:YaccProduction):
    '''sentencia : declaracion
                |  asignacion
                |  iteracion
                |  seleccion
                |  entrada_salida
    '''
    logging.info(f'{p.slice[1].type} -> sentencia')

def p_declaracion(p:YaccProduction):
    '''declaracion : INIT A_LLAVES decl_lista C_LLAVES
    '''
    logging.info('INIT A_LLAVES decl_lista C_LLAVES -> DECLARACION')

def p_decl_lista(p:YaccProduction):
    '''decl_lista : var_lista COLON TIPO
                  | decl_lista  var_lista COLON TIPO
    '''
    if len(p) == 4:
        logging.info(f'var_lista COLON TIPO: {p[3]} -> decl_lista 123123123')
        for id in p[1]:
            stg.add_symbol(name=id, type=p[3])
        p[0] = None
    else:
        logging.info(f'decl_lista var_lista COLON TIPO: {p[4]} -> decl_lista 1123123123')
        for id in p[2]:
            stg.add_symbol(name=id, type=p[4])
        p[0] = None

def p_tipo(p:YaccProduction):
    '''TIPO : TIPO_INT
            | TIPO_FLOAT
            | TIPO_STRING
    '''
    logging.info(f'{p.slice[1].type}-> TIPO')
    p[0] = p[1]

def p_var_lista(p:YaccProduction):
    '''var_lista : ID
                 | var_lista COMA ID
    '''
    if len(p) == 2:
        logging.info(f'ID: {p[1]} -> var_lista')
        p[0] = [p[1]]
    else:
        logging.info(f'VAR_LISTA COMA ID: {p[3]} -> var_lista')
        p[0] = p[1] + [p[3]]

def p_asignacion(p:YaccProduction):
    '''asignacion : ID OP_ASIGNACION expresion
    '''

    sym: SymbolTableObject = stg.get_symbol(name = str(p.slice[1].value))
    if not sym:
        logging.debug(f"Error: Variable '{p.slice[1].value}' no declarada antes de la asignacion.")

    logging.info(f'ID: ({p.slice[1].value}) OP_ASIGNACION expresion -> asignacion')

def p_iteracion(p:YaccProduction):
    '''iteracion : WHILE A_PARENTESIS condicion C_PARENTESIS A_LLAVES programa C_LLAVES
    '''
    logging.info('WHILE A_PARENTESIS condicion C_PARENTESIS A_LLAVES programa C_LLAVES -> iteracion')

def p_condicion(p:YaccProduction):
    '''condicion : condicion OR conjuncion
                 | conjuncion
    '''
    if len(p) >= 3:
        logging.info('condicion OR conjuncion -> condicion')
    else:
        logging.info('conjuncion -> condicion')

def p_conjuncion(p:YaccProduction):
    '''conjuncion : conjuncion AND termino_logico
                  | termino_logico
    '''
    if len(p) >= 3:
        logging.info('conjuncion AND termino_logico -> conjuncion')
    else:
        logging.info('termino_logico -> conjuncion')

def p_termino_logico(p:YaccProduction):
    '''termino_logico : comparacion
                      | NOT termino_logico
                      | A_PARENTESIS condicion C_PARENTESIS
    '''
    if len(p) == 4:
        logging.info('A_PARENTESIS condicion C_PARENTESIS -> termino_logico')
    elif len(p) == 3:
        logging.info('NOT termino_logico -> termino_logico')
    elif len(p) == 2:
        logging.info('comparacion -> termino_logico')

def p_comparacion(p:YaccProduction):
    '''comparacion : expresion comparador expresion
    '''
    logging.info('expresion comparador expresion -> comparacion')

def p_comparador(p:YaccProduction):
    '''comparador : IGUAL
                  | DISTINTO
                  | MAYOR
                  | MENOR
                  | MAYOR_IGUAL
                  | MENOR_IGUAL
    '''
    logging.info(f'{p.slice[1].type}({p.slice[1].value}) -> comparador')

def p_seleccion(p:YaccProduction):
    '''seleccion : IF A_PARENTESIS condicion C_PARENTESIS A_LLAVES programa C_LLAVES
                 | IF A_PARENTESIS condicion C_PARENTESIS A_LLAVES programa C_LLAVES ELSE A_LLAVES programa C_LLAVES
    '''
    if len(p) == 8:
        logging.info('IF A_PARENTESIS condicion C_PARENTESIS A_LLAVES programa C_LLAVES')
    elif len(p) == 12:
        logging.info('IF A_PARENTESIS condicion C_PARENTESIS A_LLAVES programa C_LLAVES ELSE A_LLAVES programa C_LLAVES')

def p_entrada_salida(p:YaccProduction):
    '''entrada_salida : READ A_PARENTESIS ID C_PARENTESIS
                     | WRITE A_PARENTESIS expresion C_PARENTESIS
    '''
    if p.slice[1].type == 'READ':
        logging.info('READ A_PARENTESIS ID C_PARENTESIS -> entrada_salida')
    elif p.slice[1].type == 'WRITE':
        logging.info('WRITE A_PARENTESIS expresion C_PARENTESIS -> entrada_salida')

def p_expresion(p:YaccProduction):
    '''expresion : expresion MENOS termino
                | expresion MAS termino
                | termino
    '''
    if len(p) == 4:
        if p.slice[2].type == 'MAS':
            logging.info('expresion + termino -> expresion')
        elif p.slice[2].type == 'MENOS':
            logging.info('expresion - termino -> expresion')
    elif len(p) == 2:
        logging.info('termino -> expresion')

def p_termino(p:YaccProduction):
    '''termino : termino MULTIPLICACION elemento
              | termino DIVISION elemento
              | elemento
    '''
    if len(p) == 4:
        if p.slice[2].type == 'MULTIPLICACION':
            logging.info('termino * elemento -> termino')
        elif p.slice[2].type == 'DIVISION':
            logging.info('termino / elemento -> termino')
    elif len(p) == 2:
        logging.info('elemento -> termino')

def p_elemento(p:YaccProduction):
    '''elemento : N_ENTERO
                | MENOS N_ENTERO
                | N_FLOAT
                | MENOS N_FLOAT
                | ID
                | MENOS ID
                | STRING
                | A_PARENTESIS expresion C_PARENTESIS
    '''
    if len(p) == 4:
        logging.info('A_PARENTESIS expresion C_PARENTESIS -> elemento')
    elif len(p) == 3:
        logging.info(f'MENOS {p.slice[2].type}:{p.slice[2].value} -> elemento')
        p[0] = -p[2]
    elif len(p) == 2:
        logging.info(f'{p.slice[1].type}:{p.slice[1].value} -> elemento')
        p[0] = p[1]



# Error rule for syntax errors
def p_error(p):
    raise Exception(f"Error en la linea {p.lineno or ''} at {p.value or ''}")


def ejecutar_parser(source_file: str = "./resources/parser_test_2.txt"):
    # Build the parser
    parser:LRParser = yacc()
    path_parser = Path("./resources/parser_test_2.txt")
    code = path_parser.read_text()
    parser.parse(code, lexer=lexer)
