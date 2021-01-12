import pyodbc
class Conexion:
    def get_string_conection():
        connection = pyodbc.connect('Driver={sql server};'
                                        'Server=ONELKY\SQLEXPRESS;'
                                        'Database=Universidad;'
                                        'Trusted_Connection=yes;')
        
        return connection
