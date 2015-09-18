# -*- coding: utf-8 -*-
import sqlite3
import time

#链接数据库
connection = sqlite3.connect('coachdata.sqlite')
cursor = connection.cursor()
connection.text_factory = str

#创建表
cursor.execute("""CREATE TABLE test(
                   id INTEGER PRIMARY KEY autoincrement UNIQUE NOT NULL,
                   name TEXT NOT NULL,
                   price INTEGER NOT NULL,
                   time REAL NOT NULL,
                   URL TEXT NOT NULL)""")

#插入数据到表test
productInfo = {
    'name': '大数据丛书：数据可视化',
    'price': 90.20,
    'time': time.time(),
    'URL': 'http://item.jd.com/11349429.html'
}
cursor.execute("""INSERT INTO test(name,price,time,URL) VALUES (?,?,?,?)""",
               (productInfo['name'],
                productInfo['price'],
                productInfo['time'],
                productInfo['URL']))

#删除表中数据
cursor.execute("""DELETE FROM test WHERE price=90.2 OR price=166.2""")

#查询数据
cursor.execute("""SELECT price FROM test ORDER BY price ASC""")
print cursor.fetchone()[0]

#根据id查询表内容
def get_athlete_from_id(athlete_id):
    connection = sqlite3.connect('coachdata.sqlite')
    cursor = connection.cursor()

    results = cursor.execute("SELECT name,dob from athletes WHERE athlete_id=?",(athlete_id))   #查询
    (name,dob) = results.fetchall()

    results = cursor.execute("SELECT value FROM timing_data WHERE athlete_id=?",(athlete_id))
    data = [row[0] for row in results.fetchall()]

    response = {
        'Name': name,
        'DOB': dob,
        'data': data,
    }
    connection.close()
    return response

