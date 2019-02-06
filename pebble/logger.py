from sqlite3 import Error

import pandas as pd
import sqlite3


class SQLiteLogger:
    """
    Class loggs all information about user's actions and bot's answers to them
    to SQLite DB.
    """
    def __init__(self, db_name):
        """Creats database with 2 tables: user and record"""
        self._create_user = \
        '''CREATE TABLE IF NOT EXISTS user (
            user_id integer PRIMARY KEY,
            user_name text,
            first_name text,
            last_name text
        )
        '''
        self._create_record = \
        '''CREATE TABLE IF NOT EXISTS record (
            user_id integer,
            chat_id integer,
            message_id integer,
            dt text,
            message text,
            is_image integer,
            meta text,
            button text,
            FOREIGN KEY (user_id) REFERENCES user (user_id),
            CONSTRAINT record_pk PRIMARY KEY (user_id, chat_id,
                                              message_id, button)
        )
        '''
        self._conn = sqlite3.connect(db_name, check_same_thread=False)
        self._create_table(self._create_user)
        self._create_table(self._create_record)

    def record(self, user_id, user_name, first_name, last_name, chat_id,
               message_id, dt, message, is_image, meta, button):
        """Adds information about user's action to database"""
        if not self._user_contains(user_id):
            self._new_user(user_id, user_name, first_name, last_name)
        self._new_record(user_id, chat_id, message_id, dt, message, is_image,
                         meta, button)
        self._conn.commit()

    def get_user_df(self):
        """Retuns pandas.DataFrame with 'user' table"""
        return pd.read_sql_query("SELECT * FROM user", self._conn)

    def get_record_df(self):
        """Retuns pandas.DataFrame with 'record' table"""
        return pd.read_sql_query("SELECT * FROM record", self._conn)

    def _create_table(self, create_table_sql):
        try:
            c = self._conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def _new_user(self, user_id, user_name, first_name, last_name):
        sql = ''' REPLACE INTO user(user_id,user_name,first_name,last_name)
                  VALUES(?,?,?,?)'''
        cur = self._conn.cursor()
        user = (user_id, user_name, first_name, last_name)
        cur.execute(sql, user)
        return cur.lastrowid

    def _new_record(self,user_id,chat_id,message_id,dt,message, is_image, meta,
                    button):
        sql = '''REPLACE INTO record(user_id, chat_id, message_id, dt,
                                     message, is_image, meta, button)
                 VALUES(?,?,?,?,?,?,?,?)'''
        cur = self._conn.cursor()
        record = (user_id, chat_id, message_id, dt, message, is_image, meta,
                  button)
        cur.execute(sql, record)
        return cur.lastrowid

    def _user_contains(self, user_id):
        return len(self._get_user_with_id(user_id)) > 0

    def _get_user_with_id(self, user_id):
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM user WHERE user_id = {}".format(user_id))
        return(cursor.fetchall())
