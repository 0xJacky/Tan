#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 加载包
import os
import time
from xlwt import Workbook
from db import Database
db = Database()

ABS_PATH = os.path.split(os.path.realpath(__file__))[0]
REPORT_PATH = os.path.join(ABS_PATH, 'report%s.xls' % time.strftime("%Y-%m-%d", time.localtime()))

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

# excel 第一行数据
head = [u'姓名']
dates = []
for t in get_tasks():
    dates = dates + [str(t['date'])]
head = head + dates
print(head)

# 内容
context = {}
students = get_students_list()
for n in students:
    context[n] = {u'姓名':n}
print(context)

for d in dates:
    list = query_clock_in_list(d)
    print(list)
    for i in students:
        if i in list:
            context[i][d] = '√'
        else:
            context[i][d] = '×'
print(context)


# 定义excel操作句柄
o = Workbook()
e = o.add_sheet(u'打卡统计')
index = 0
#标题
for data in head:
    e.write(0, index, data)
    index += 1

index = 1

#内容
for k,v in context.items():
    colIndex = 0
    for item in head:
        e.write(index, colIndex, v[item])
        colIndex += 1
    index += 1

#保存
o.save(REPORT_PATH)
