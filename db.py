import psycopg2, psycopg2.extras
from datetime import datetime

class DB:
    
    def __init__(self):
        """Database connection
        """
                
        self.params = {
            "database": "hospital_db",
            "user": "ubuntu",
            "password": "1234",
            "host": "127.0.0.1",
            "port": "5432"
        }
        self.con = psycopg2.connect(**self.params)
        self.cursor = self.con.cursor(cursor_factory = psycopg2.extras.DictCursor)
        
        
    def table(self,table_name):
        """Accepts table name on which perform query methods
        """
        
        self.table_name = table_name
        return self
    
    
    def get(self,order='ASC',single=False):
        """Returns all or one record of a table
        """
        
        self.cursor.execute('SELECT * FROM '
                            +self.table_name
                            +' ORDER BY id '+order)
        return self.cursor.fetchone() if single else self.cursor.fetchall()
    
    
    def where(self,field,value,single=True):
        """Returns all or one record depending the given condition condition
        """
        
        self.cursor.execute('SELECT * FROM '
                            +self.table_name
                            +' WHERE '+field+' = %s', (value,))
        return self.cursor.fetchone() if single else self.cursor.fetchall()


    def delete(self,field,value):
        """Deletes records depending on the given condition
        """
        
        query = 'DELETE FROM '+self.table_name+' WHERE '+field+' = %s'
        self.cursor.execute(query, (value,))
        return self.con.commit()
    
        
    def add(self,fields,values):
        """Adds a new record
        """
        
        query = 'INSERT INTO '+self.table_name+'('
        wildcard = ''
        for i in fields:
            query+=i+','
            wildcard+='%s,'
        query = query[0:len(query)-1]
        wildcard = wildcard[0:len(wildcard)-1]
        query +=') values ('+wildcard+')'
        
        self.cursor.execute(query,values)
        return self.con.commit()
    
    
    def update(self,fields,values,id):
        """Updates a record
        """
        
        query = 'UPDATE '+self.table_name+' SET '
        for i in fields:
            query+=i+' = %s,'
        query = query[0:len(query)-1]
        query +=' WHERE id = '+str(id)
        
        self.cursor.execute(query,values)
        return self.con.commit()
    
    
    def where_and(self,field1,field2,values,single=True):
        """Returns all or one records depending on the two given condition
        """
        
        self.cursor.execute('SELECT * FROM '
                            +self.table_name+' WHERE '
                            +field1+'=%s AND '+field2+'=%s',values)
        return self.cursor.fetchone() if single else self.cursor.fetchall()
    
    
    def count(self):
        """Returns count of all records in a table
        """
        
        self.cursor.execute('SELECT COUNT(id) FROM '+self.table_name)
        return self.cursor.fetchone()[0]
    
    
    def inner_join(self,table_A,tableB,id_A,id_B):
        """Inner joins two tables based on the given columns
        """
        
        self.cursor.execute('SELECT * FROM '+table_A+' inner join '
                            +tableB+' on '+id_A+'='+id_B+' ORDER BY '+id_A+' DESC')
        return self.cursor.fetchall()



