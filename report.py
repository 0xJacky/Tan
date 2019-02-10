#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 加载包
import os
import time
import xlsxwriter
from db import Database
db = Database()

ABS_PATH = os.path.split(os.path.realpath(__file__))[0]
REPORT_PATH = os.path.join(ABS_PATH, 'report-%s.xlsx' % time.strftime("%Y-%m-%d"))

def get_tasks():
    sql = 'SELECT * FROM %s_task' % db.sql_prefix
    print(sql)
    return db.fetchall(sql)


def get_students_list():
    sql = "SELECT `name` FROM `%s_students`" % db.sql_prefix
    print(sql)
    list = []
    for i in db.fetchall(sql):
        list = list + [i['name']]
    return list


def query_clock_in_list(date):
    sql = "SELECT s.`name` FROM (%s_task as t INNER JOIN %s_log as l ON t.`ID` = l.`task_id`) \
            INNER JOIN %s_students as s ON s.`ID` = l.`student_id` WHERE t.`date`='%s'" % (db.sql_prefix, db.sql_prefix, db.sql_prefix, date)
    print(sql)
    list = []
    for i in db.fetchall(sql):
        list = list + [i['name']]
    return list


# 定义 excel 操作句柄
o = xlsxwriter.Workbook(REPORT_PATH)
e = o.add_worksheet(u'打卡统计')
workfomat = o.add_format({
    'align' : 'center',
    'valign' : 'vcenter'
})

# (0,0)
e.write(0, 0, u'姓名', workfomat)
# (x,0)
index = 1
students = get_students_list()
for s in students:
    e.write(index, 0, s, workfomat)
    index += 1


# (x,y)(x=>1,y=>0)
col_index = 1
for t in get_tasks():
    e.write(0, col_index, str(t['date']), workfomat)
    e.set_column(0, index, 10)
    list = query_clock_in_list(t['date'])
    index = 1
    for i in students:
        status = '√' if i in list else 'x'
        e.write(index, col_index, status, workfomat)
        index += 1
    col_index += 1


# 关闭 & 保存
o.close()
