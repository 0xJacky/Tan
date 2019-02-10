# Project Tan
基于 itchat 的微信机器人（高度分化）

© 2019 0xJacky

## 使用方法 Usage
1. 将 tan.sql 导入 MySQL
2. 在 tan.task 中添加任务 (id,date), 在 tan.student 中导入学生名单
3. 拷贝 config-default.ini 为 config.ini 并完成配置
4. 安装依赖 `pip3 install -r requirements.txt`
5. 运行（需要扫描二维码登录微信，itchat 在项目的根目录生成 QR.png）
````
python3 tan.py
````


| 触发词 | 权限 | 功能 |
| :------: | :------: | :------: |
| 打卡总记录 | 课代表 | 输出所有人打卡总次数 |
| 删除记录[日志ID] | 课代表 | 删除打卡记录 |
| 查询打卡 | 所有人 | 查询今日打卡顺序排名 |
| 我/打卡 | 所有人 | 打卡（返回[日志ID]）|


忽略词：「Tan」,「不」避免两个机器人复读/避免奇怪的打卡激活语句


### 打卡总记录
![image][image-0]


### 删除记录
![image][image-1]


### 查询打卡
![image][image-2]


### 我/打卡
![image][image-3]


### 生成打卡报告 Excel
````
python3 report.py
````
![image][image-4]


### LICENSE

MIT


[image-0]:	https://github.com/0xJacky/Tan/raw/master/screenshot/0.png
[image-1]:	https://github.com/0xJacky/Tan/raw/master/screenshot/1.jpg
[image-2]:	https://github.com/0xJacky/Tan/raw/master/screenshot/2.png
[image-3]:	https://github.com/0xJacky/Tan/raw/master/screenshot/3.jpg
[image-4]:	https://github.com/0xJacky/Tan/raw/master/screenshot/4.jpg