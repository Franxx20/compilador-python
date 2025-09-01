from ply.lex import *
from pathlib import Path
from constantes import MAX_STRING_LENGHT
import logging
import re
from SymbolTableGenerator import stg

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Palabras reservadas
reserved = {
    'if': "IF",
    'else': "ELSE",
    'while': "WHILE",
    'init': "INIT",
    'AND': "AND",
    'OR': "OR",
    'NOT': "NOT",
    'read': 'READ',
    'write': 'WRITE',
}

# El orden de los elementos de la lista de TOKENS no importa.
tokens = [
    'A_PARENTESIS',
    'C_PARENTESIS',

    'A_LLAVES',
    'C_LLAVES',

    'A_CORCHETES',
    'C_CORCHETES',

    'COMA',
    'COLON',

    'OP_ASIGNACION',

    'TIPO_FLOAT',
    'TIPO_INT',
    'TIPO_STRING',

    'N_FLOAT',
    'N_ENTERO',
    'STRING',

    'ID',

    'IGUAL',
    'DISTINTO',
    'MENOR_IGUAL',
    'MAYOR_IGUAL',
    'MENOR',
    'MAYOR',

    'MAS',
    'MULTIPLICACION',
    'MENOS',
    'DIVISION',
] + list(reserved.values())


# Expresiones regulares para TOKENS simples
# El orden de estas definiciones de TOKENS es importante


t_MAS =  r'\+'
t_MENOS = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'

t_IGUAL = r'=='
t_DISTINTO = r'!='
t_MENOR_IGUAL = r'<='
t_MAYOR_IGUAL = r'>='
t_MENOR = r'<'
t_MAYOR = r'>'

t_OP_ASIGNACION = r':='

t_A_PARENTESIS = r'\('
t_C_PARENTESIS = r'\)'

t_A_LLAVES = r'\{'
t_C_LLAVES = r'\}'

t_A_CORCHETES = r'\['
t_C_CORCHETES = r'\]'

t_COMA = r','
t_COLON = r':'


def t_COMENTARIO(t:LexToken):
    r'#\+.*?\+#'
    t.lexer.lineno += t.value.count('\n')

def t_TIPO_FLOAT(t:LexToken):
    r'Float'
    # stg.add_symbol(name=t.value, type=t.type)
    return t

def t_TIPO_INT(t:LexToken):
    r'Int'
    # stg.add_symbol(name=t.value, type=t.type)
    return t

def t_TIPO_STRING(t:LexToken):
    r'String'
    # stg.add_symbol(name=t.value, type=t.type)
    return t

def t_ID(t:LexToken):
    r'[a-zA-Z](\w|_)*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_N_FLOAT(t:LexToken):
    r'(\d+\.\d*|\.\d+)'
    t.value = float(t.value)
    return t

def t_N_ENTERO(t:LexToken):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t:LexToken):
    r'\"[^\"]*\"'
    # removemos las comillas dobles para obtener un string limpio
    t.value = t.value[1:-1]
    return t

# Regla que cuenta la cantidad de lineas
def t_newline(t:LexToken):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Ignorar tabulaciones y espacios
t_ignore = ' \t'

# Manejo de errores
def t_error(t:LexError):
    raise Exception(f"Caracter invalido '{t.value[0]}' en la linea: {t.lexer.lineno}")


# Build the lexer
lexer = lex(reflags=re.DOTALL)


def ejecutar_lexer(source_file: str = "./resources/lexer_test_2.txt"):
    path_lexter = Path(source_file)
    data = path_lexter.read_text()
    lexer.input(data)
    while True:
        token = lexer.token()
        if not token:
            break
        logging.info(f'TOKEN: {token.type} LEXEMA: {token.value}')
