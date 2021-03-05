import psycopg2

class Conexao:
    def __init__(self, **kwargs):
        self.config = kwargs
        self.connect()
         
    def connect(self):
        try: self.__conexao = psycopg2.connect(**self.config)
        except: self.__conexao = False
        return self.__conexao and True

    def disconnect(self):
        try: self.__conexao.close()
        except: return False
        return True

    def cursor(self): return self.__conexao and self.__conexao.cursor() or False

    def commit(self): 
        try: self.__conexao.commit()
        except: return False
        return True

    def __select(self, **kwargs):
        table = kwargs.get('table')
        where = kwargs.get('where')
        columns = kwargs.get('columns') or '*'
        if not isinstance(columns, str): columns = self.__formatColumns(columns)

        return f'select { columns } from { table } { self.__formatWhere(where) }'

    def selectAll(self, **kwargs): 
        query = self.__select(**kwargs)
        cursor = self.cursor()
        cursor.execute(query)

        values = cursor.fetchall()

        columns = kwargs.get('columns')
        if columns: 
            if isinstance(columns, str): columns = [ columns, ]
            values = self.__transformDict(columns, values)
        return values
    
    def selectOne(self, **kwargs): 
        query = self.__select(**kwargs)
        cursor = self.cursor()
        cursor.execute(query)

        values = cursor.fetchone()

        columns = kwargs.get('columns')
        if columns: 
            if isinstance(columns, str): columns = [ columns, ]
            values = self.__transformListsInDict(columns, values)
            if len(columns) == 1: return values[columns[0]]
        return values

    def __transformListsInDict(self, keys, values):
        return dict([ [ keys[i], values[i] ] for i in range(len(keys)) ])

    def __transformDict(self, keys, values):
        return [ self.__transformListsInDict(keys, value) for value in values ]
   
    def insert(self, **kwargs): 
        table = kwargs.get('table')
        inserts = kwargs.get('inserts')

        columns = self.__formatColumns(inserts.keys())
        values = tuple(inserts.values())

        cursor = self.cursor()
        cursor.execute(f'insert into { table } ({ columns }) values { values }')
   
    def delete(self, **kwargs): 
        table = kwargs.get('table')
        where = kwargs.get('where')

        cursor = self.cursor()
        cursor.execute(f'delete from { table } { self.__formatWhere(where) }')

    def update(self, **kwargs): 
        table = kwargs.get('table')
        set = kwargs.get('set')
        where = kwargs.get('where') 

        cursor = self.cursor()
        cursor.execute(f'update { table } set { self.__formatSetUpdate(set) } { self.__formatWhere(where) }')
    
    def __formatSetUpdate(self, dictSet):
        listaSets = []
        for chave, valor in dictSet.items():
            listaSets.append(f"{ chave } = { self.__addAspasIfString(valor) }")
        return self.__formatColumns(listaSets)

    def __formatWhere(self, where):
        if isinstance(where, dict):
            key = list( where.keys() )[0]
            return f"where { key } = { self.__addAspasIfString( where[key] ) }"

        else: return ""

    def __formatColumns(self, columns): return ', '.join(columns)

    def __addAspasIfString(self, value): return f"'{ value }'" if type(value) == str else value