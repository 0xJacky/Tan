#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 加载包
import itchat
import time
from db import Database
db = Database()
VERSION = '0.0.1'
# 登陆
itchat.auto_login(True)
# 处理群聊消息
@itchat.msg_register(itchat.content.TEXT, isGroupChat = True)
def text_reply(msg):
    if msg['isAt']:
        message = 'Project Tan V%s' % VERSION
        if(u'打卡' in msg['Content']):
            if (u'获取学生名单' in msg['Content']):
                sql = "SELECT * FROM `%s_students`" % db.sql_prefix
                message = db.fetchall(sql)
        if(u'查询打卡' in msg['Content']):
            sql = "SELECT s.`id`, t.`id`, s.`name` FROM (%s_task as t INNER JOIN %s_log as l ON t.`ID` = l.`task_id`) \
    INNER JOIN %s_students as s ON s.`ID` = l.`student_id`" % ((db.sql_prefix,)*3)
            print(sql)
            res = db.fetchall(sql)
            message +=str(res)
        if(u'我' in msg['Content']):
            sql = "SELECT * FROM `%s_students` WHERE `name`='%s'" % (db.sql_prefix, msg['ActualNickName'])
            stu_res = db.fetchone(sql)

            sql = "SELECT * FROM `%s_task` WHERE `date`='%s'" % (db.sql_prefix, time.strftime("%Y-%m-%d", time.localtime()))
            print(sql)
            task_res = db.fetchone(sql)
            if(stu_res):
                stu_id = stu_res['ID']
                if (task_res):
                    task_id = task_res['ID']
                    message +='已匹配 student_id:%s task_id:%s' % (stu_id, task_id)
                    sql = "SELECT * FROM `%s_log` WHERE `student_id`='%s' AND `task_id`='%s'" % (db.sql_prefix, stu_id, task_id)
                    link_res = db.fetchone(sql)
                    if not link_res:
                        sql = "INSERT INTO `%s_log` (student_id, task_id) VALUE ('%s', '%s')" % (db.sql_prefix, stu_id, task_id)
                        try:
                            db.query(sql)
                            message += '打卡成功'
                        except Exception as e:
                            message += '打卡失败，错误信息: %s' % e
                    else:
                        message += '你已经打过卡了'
                else:
                    message += '已匹配 ID:%s, 今天没有打卡任务噢' % stu_id

            else:
                message += '未匹配，请修改群名片'

        itchat.send(u'@%s\u2005I received: %s, %s' % (msg['ActualNickName'], msg['Content'], message), msg['FromUserName'])

itchat.run()