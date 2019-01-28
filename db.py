#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql, pymysql.cursors
import configparser, sys, os
from warnings import filterwarnings

# ignore MySQL warnings
filterwarnings('ignore', category = pymysql.Warning)
config_dir = os.path.dirname(os.path.realpath(__file__)) + "/config.ini"

# 加载配置文件
config = configparser.ConfigParser(allow_no_value=True)
config.read(config_dir)

class Database:
    sql_host = config.get("SQL","sql_host")
    sql_user = config.get("SQL","sql_user")
    sql_passwd = config.get("SQL","sql_passwd")
    sql_db_name = config.get("SQL","sql_db_name")
    sql_prefix = config.get("SQL","sql_prefix")
    
    def __init__(self):
        self.db = pymysql.connect(self.sql_host, self.sql_user, self.sql_passwd, self.sql_db_name, cursorclass = pymysql.cursors.DictCursor)
        self.cursor = self.db.cursor()

    def version(self):
        self.cursor.execute("SELECT VERSION()")
        data = self.cursor.fetchone()
        print("Database version: %s " % data['VERSION()'])
        return "Database version: %s " % data['VERSION()']

    def clear_table(self, name):
        sql = "TRUNCATE `%s_%s`" % (self.sql_prefix, name)
        self.query(sql)

    def optimze(self):
        sql = "OPTIMIZE TABLE `%s_devices`, `%s_firmwares`, `%s_firmwares_info`" % ((self.sql_prefix,) * 3)
        self.query(sql)

    def query(self, sql):
        try:
            # execute sql
            self.cursor.execute(sql)
            # commit to database
            self.db.commit()

        except Exception as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
            # rollback if database error
            self.db.rollback()
    def fetchone(self, sql):
        try:
            # execute sql
            self.cursor.execute(sql)
            # fetch result
            return self.cursor.fetchone()
        except Exception as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def fetchall(self, sql):
        try:
            # execute sql
            self.cursor.execute(sql)
            # fetch result
            return self.cursor.fetchall()
        except Exception as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
    def get_option(self):
        sql = "SELECT * FROM %s_options" % self.sql_prefix
        return self.fetchone(sql)

    def update_option(self, key, value):
        sql = "UPDATE %s_options SET %s = \'%s\'" % (self.sql_prefix, key, value)
        self.query(sql)

    def save_beta_ipsw(self, value):
        self.clear_table('beta_firmwares')
        sql = "INSERT IGNORE INTO %s_beta_firmwares(device, url, version, buildid) \
        VALUES %s" % (self.sql_prefix, value)
        self.query(sql)
