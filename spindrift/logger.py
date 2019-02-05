from sqlite3 import Error

import pandas as pd
import sqlite3


class SQLiteLogger:
    def __init__(self, db_name):
        self.create_user = \
        '''CREATE TABLE IF NOT EXISTS user (
            user_id integer PRIMARY KEY,
            user_name text,
            first_name text,
            last_name text
        )
        '''
        self.create_record = \
        '''CREATE TABLE IF NOT EXISTS record (
            user_id integer,
            chat_id integer,
            message_id integer,
            button text NOT NULL,
            meta text,
            FOREIGN KEY (user_id) REFERENCES user (user_id),
            CONSTRAINT record_id PRIMARY KEY (user_id, chat_id, message_id)
        )
        '''
        self.conn = sqlite3.connect(db_name)
        self._create_table(self.create_user)
        self._create_table(self.create_record)

    def record(self, user_id, user_name, first_name, lastname, chat_id, message_id, button, meta):
        if not self._user_contains(user_id):
            self._new_user(user_id, user_name, first_name, lastname)
        self._new_record(user_id, chat_id, message_id, button, meta)

    def get_user_df(self):
        return pd.read_sql_query("SELECT * FROM user", self.conn)

    def get_record_df(self):
        return pd.read_sql_query("SELECT * FROM record", self.conn)

    def _create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def _new_user(self, user_id, user_name, first_name, lastname):
        sql = ''' INSERT INTO user(user_id,user_name,first_name,last_name)
                  VALUES(?,?,?,?)'''
        cur = self.conn.cursor()
        user = (user_id, user_name, first_name, lastname)
        cur.execute(sql, user)
        return cur.lastrowid

    def _new_record(self, user_id, chat_id, message_id, button, meta):
        sql = ''' INSERT INTO record(user_id,chat_id,message_id,button,meta)
                  VALUES(?,?,?,?,?)'''
        cur = self.conn.cursor()
        record = (user_id, chat_id, message_id, button, meta)
        cur.execute(sql, record)
        return cur.lastrowid

    def _user_contains(self, user_id):
        return len(self._get_user_with_id(user_id)) > 0

    def _get_user_with_id(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user WHERE user_id = {0}".format(user_id))
        return(cursor.fetchall())
