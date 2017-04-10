#!/usr/bin/env python
# encoding: utf-8

# conda install MySQL-python
import MySQLdb as mdb  #数据库连接器

class MysqlTester():
    def __init__(self):
        self.host='127.0.0.1'
        self.user = 'root'
        self.password = ''
        self.name = 'oksousou'
        
    def connect(self):
        self.dbconn = mdb.connect(self.host, self.user, self.password, self.name, charset='utf8')
        self.dbconn.autocommit(False)
        self.dbcurr = self.dbconn.cursor()
        self.dbcurr.execute('SET NAMES utf8')
        
    def select(self):
        print "select"
        
    def insert(self):
        print "insert"  
        
    def delete(self):
        print "delete"      
    
if __name__ == "__main__":
    mysqlTester = MysqlTester()
    mysqlTester.connect()
    mysqlTester.select()
    
    