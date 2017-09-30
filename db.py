#!/usr/bin/env python
import sqlite3, atexit, time

class DB:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        atexit.register(self.close)

    def close(self):
        self.cursor.close()
        self.conn.close()

    def execute_file(self, filename):
        schema = open(filename, 'r').read()
        self.cursor.execute(schema)
        self.conn.commit()

    def dump(self):
        for line in self.conn.iterdump():
            print(line)

    def build_db(self):
        self.execute_file('schema.sql')
        #self.execute_file('schema.sql')

db = DB()
db.build_db()
db.dump()
