# pip install pymysql

import numpy as np
import pandas as pd
import pymysql
from datetime import datetime, date, time

#__________________________________________________________#

class MySQL:
    def __init__(self, db, host='localhost', user='root', password='Qawsedrf1!', charset='utf8'):
        self.db = db
        self.host = host
        self.user = user
        self.password = password
        self.charset = charset
        
        self.sql_cursor = self._get_connection()
        
        self.fetchall = None
        
    def _get_connection(self):
        connection = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        return connection.cursor()
    
    def send_queries(self,queries,col_name=None):
        self.sql_cursor.execute(query = queries)
        self.fetchall = self.sql_cursor.fetchall()
                
        result = pd.DataFrame(self.fetchall)
        if col_name is not None:
            result.columns = col_name
            
        self.table = result


sql_class = MySQL(db='employees')

q = """ 
SELECT sal.emp_no, em.first_name, em.last_name, MAX(sal.to_date) AS max_to_date, sal.salary
FROM (SELECT emp_no, to_date, salary FROM salaries
		GROUP BY emp_no
        HAVING YEAR(to_date) != 9999) AS sal
INNER JOIN employees AS em
	ON em.emp_no = sal.emp_no
GROUP BY sal.emp_no;

 """

c = ['emp_no','first_name','last_name','max_to_date','salary']

sql_class.send_queries(queries=q, col_name=c)
t = sql_class.table
