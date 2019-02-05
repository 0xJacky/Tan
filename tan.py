#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 加载包
import itchat
import time
from db import Database

db = Database()
VERSION = '0.9'
# 登陆
itchat.auto_login(True)


# 获取学生名单
def get_students_list():
    sql = "SELECT * FROM `%s_students`" % db.sql_prefix
    print(sql)
    return db.fetchall(sql)


# 获取打卡列表
def query_clockin_list():
    date = time.strftime("%Y-%m-%d", time.localtime())
    sql = "SELECT s.`id`, t.`id`, s.`name`, t.`date` FROM (%s_task as t INNER JOIN %s_log as l ON t.`ID` = l.`task_id`) \
        INNER JOIN %s_students as s ON s.`ID` = l.`student_id` WHERE t.`date`='%s'" % (
    db.sql_prefix, db.sql_prefix, db.sql_prefix, date)
    print(sql)
    res = db.fetchall(sql)
    message = '%s 打卡记录\n' % date
    t = 0
    for i in res:
        t += 1
        message += 'No.%s %s\n' % (t, i['name'])
    return message[:-1]


# 打卡
def handle_clockin(msg):
    message = ''
    sql = "SELECT * FROM `%s_students` WHERE `name`='%s'" % (db.sql_prefix, msg['ActualNickName'])
    print(sql)
    stu_res = db.fetchone(sql)

    sql = "SELECT * FROM `%s_task` WHERE `date`='%s'" % (db.sql_prefix, time.strftime("%Y-%m-%d", time.localtime()))
    print(sql)
    task_res = db.fetchone(sql)
    if (stu_res):
        stu_id = stu_res['ID']
        if (task_res):
            task_id = task_res['ID']
            print('已匹配 student_id:%s task_id:%s' % (stu_id, task_id))
            sql = "SELECT * FROM `%s_log` WHERE `student_id`='%s' AND `task_id`='%s'" % (db.sql_prefix, stu_id, task_id)
            print(sql)
            link_res = db.fetchone(sql)
            if not link_res:
                sql = "INSERT INTO `%s_log` (student_id, task_id) VALUE ('%s', '%s')" % (db.sql_prefix, stu_id, task_id)
                print(sql)
                try:
                    db.query(sql)
                    message += '打卡成功'
                except Exception as e:
                    message += '打卡失败，错误信息: %s' % e
            else:
                message += '你已经打过卡了'
        else:
            print('已匹配 Student ID:%s, 今天没有打卡任务噢' % stu_id)
            message += '今天没有打卡任务噢'

    else:
        message += '未匹配，请修改群名片'
    return message


# 处理群聊消息
@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_reply(msg):
    print('当前消息: ' + msg['ActualNickName'] + ': ' + msg['Content'])
    if u'不' not in msg['Content'] and 'Tan' not in msg['Content']:
        Tan = 'Project Tan v%s\n' % VERSION
        message = Tan
        if (u'获取学生名单' in msg['Content']):
            message += str(get_students_list())
        elif (u'查询打卡' in msg['Content']):
            print('已匹配到关键词' + '查询')
            message += str(query_clockin_list())
        elif (u'我' in msg['Content'] and u'打卡' in msg['Content']):
            print('已匹配到关键词' + '我/打卡')
            message += handle_clockin(msg)
        else:
            pass
        if message != Tan:
            print(message)
            itchat.send(u'@%s\u2005%s' % (msg['ActualNickName'], message), msg['FromUserName'])


itchat.run()
