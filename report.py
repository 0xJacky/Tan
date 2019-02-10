#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 加载包
import os
import time
import collections
import xlsxwriter
from db import Database
db = Database()

ABS_PATH = os.path.split(os.path.realpath(__file__))[0]
REPORT_PATH = os.path.join(ABS_PATH, 'report-%s.xlsx' % time.strftime("%Y-%m-%d", time.localtime()))

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


# 标题
head = [u'姓名']
dates = []
for t in get_tasks():
    dates = dates + [str(t['date'])]
head = head + dates
print(head)

# 内容
context = {}
context = collections.OrderedDict(sorted(context.items(), key=lambda t: t[0]))
students = get_students_list()
for n in students:
    context[n] = {u'姓名':n}
print(context)

for d in dates:
    list = query_clock_in_list(d)
    for i in students:
        if i in list:
            context[i][d] = '√'
        else:
            context[i][d] = '×'
print(context)


# 定义excel操作句柄
o = xlsxwriter.Workbook(REPORT_PATH)
e = o.add_worksheet(u'打卡统计')
workfomat = o.add_format({
    'align' : 'center',
    'valign' : 'vcenter'
})
index = 0


# 标题
for data in head:
    e.write(0, index, data, workfomat)
    e.set_column(0, index, 10)
    index += 1

index = 1


# 内容
for k,v in context.items():
    col_index = 0
    for i in head:
        e.write(index, col_index, v[i], workfomat)
        col_index += 1
    index += 1
# 关闭
o.close()
