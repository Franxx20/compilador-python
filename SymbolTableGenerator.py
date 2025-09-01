class SymbolTableObject:
    def __init__(self, name:str = None, type:str = None, value:str = None, symbol_size:int = None):
        self.name = name
        self.type = type
        self.value = value
        self.symbol_size = symbol_size

    def __repr__(self):
        string = 'SymbolTableObject('
        if self.name:
            string += f'name={self.name}, '
        if self.type:
            string += f'type={self.type}, '
        if self.value:
            string += f'value={self.value}, '
        if self.symbol_size:
            string += f'symbol_size={self.symbol_size}, '
        string = string.rstrip(', ')
        string += ')'
        return string


class SymbolTableGenerator:
    def __init__(self):
        self.symbol_table:dict[str, SymbolTableObject] = {}

    def add_symbol(self, name:str, type:str = None, value:str = None, symbol_size:int = None):
        if name in self.symbol_table:
            raise Exception(f"Symbol '{name}' already exists in the symbol table.")
        self.symbol_table[name] = SymbolTableObject(name, type, value, symbol_size)

    def get_symbol(self, name:str) -> SymbolTableObject:
        return self.symbol_table.get(name)

    def __repr__(self):
        return f'SymbolTable({self.symbol_table})\nname | type | value | symbol_size\n' + \
               '\n'.join(f'{symbol}' for symbol in self.symbol_table.values())

    def generate_file(self, filename:str = 'symbol_table.txt'):
        try:
            with open(filename, 'w') as f:
                f.write("name | type | value | symbol_size\n")
                for symbol in self.symbol_table.values():
                    f.write(f'{symbol}\n')
        except Exception as e:
            raise Exception(f"Error writing symbol table to file: {e}")