#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 加载包
import itchat
import time
import re
from db import Database

db = Database()
VERSION = '1.0'
# 登陆
itchat.auto_login(True)


# 获取打卡列表
def query_clock_in_list():
    date = time.strftime("%Y-%m-%d", time.localtime())
    sql = "SELECT s.`id`, t.`id`, s.`name`, t.`date` FROM (%s_task as t INNER JOIN %s_log as l ON t.`ID` = l.`task_id`) \
        INNER JOIN %s_students as s ON s.`ID` = l.`student_id` WHERE t.`date`='%s'" % (db.sql_prefix, db.sql_prefix, db.sql_prefix, date)
    print(sql)
    res = db.fetchall(sql)
    message = '%s 打卡记录\n' % date
    t = 0
    for i in res:
        t += 1
        message += 'No.%s %s\n' % (t, i['name'])
    return message[:-1]


# 获取学生信息
def get_student(name):
    sql = "SELECT * FROM `%s_students` WHERE `name`='%s'" % (db.sql_prefix, name)
    print(sql)
    return db.fetchone(sql)


# 打卡
def handle_clockin(msg):
    message = ''
    stu_res = get_student(msg['ActualNickName'])

    sql = "SELECT * FROM `%s_task` WHERE `date`='%s'" % (db.sql_prefix, time.strftime("%Y-%m-%d", time.localtime()))
    print(sql)
    task_res = db.fetchone(sql)
    if stu_res:
        stu_id = stu_res['ID']
        if task_res:
            task_id = task_res['ID']
            print('已匹配 Student ID:%s, Task ID:%s' % (stu_id, task_id))
            sql = "SELECT * FROM `%s_log` WHERE `student_id`='%s' AND `task_id`='%s'" % (db.sql_prefix, stu_id, task_id)
            print(sql)
            link_res = db.fetchone(sql)
            if not link_res:
                sql = "INSERT INTO `%s_log` (student_id, task_id) VALUE ('%s', '%s')" % (db.sql_prefix, stu_id, task_id)
                print(sql)
                try:
                    db.query(sql)
                    sql = 'SELECT MAX(id) as id FROM `%s_log`' % db.sql_prefix
                    print(sql)
                    message += '打卡成功, 日志ID: %s' % db.fetchone(sql)['id']
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


# 管理
def has_power(name):
    stu_res = get_student(name)
    if stu_res and stu_res['power'] == 1:
        return True
    else:
        return False


def get_clock_in_count():
    sql = 'SELECT `name`, COUNT(l.task_id) as times FROM `%s_students` LEFT JOIN %s_log as l ON l.student_id = `%s_students`.ID GROUP BY(`%s_students`.`name`) ORDER BY times DESC' % ((db.sql_prefix,)*4)
    result = db.fetchall(sql)
    message = 'Name|总次数\n'
    for r in result:
        message += '%s %s\n' % (r['name'], r['times'])
    return message[:-1]


def delete_log(msg):
    if not has_power(msg['ActualNickName']):
        return '无权访问'
    else:
        log_id = re.findall('\d+', msg['Content'])[0]
        sql = 'DELETE FROM `%s_log` WHERE `ID`=%s' % (db.sql_prefix, log_id)
        print(sql)
        try:
            db.query(sql)
            return '操作成功'
        except Exception as e:
            return '操作失败，错误信息: %s' % e


# 处理群聊消息
@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_reply(msg):
    print('当前消息: ' + msg['ActualNickName'] + ': ' + msg['Content'])
    if u'不' not in msg['Content'] and 'Tan' not in msg['Content']:
        tan = 'Project Tan v%s\n' % VERSION
        message = tan
        if u'打卡总记录' in msg['Content']:
            if has_power(msg['ActualNickName']):
                message += str(get_clock_in_count())
            else:
                message += '无权访问'
        elif u'删除记录' in msg['Content']:
            message += str(delete_log(msg))
        elif u'查询打卡' in msg['Content']:
            print('已匹配到关键词' + '查询')
            message += str(query_clock_in_list())
        elif u'我' in msg['Content'] and u'打卡' in msg['Content']:
            print('已匹配到关键词' + '我/打卡')
            message += handle_clockin(msg)
        else:
            pass
        if message != tan:
            print(message)
            itchat.send(u'@%s\u2005%s' % (msg['ActualNickName'], message), msg['FromUserName'])


itchat.run()
