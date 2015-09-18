# -*- coding: utf-8 -*-
'''分离数据库操作，尚未完成'''
import sqlite3
import time

# def initSqlite(dbname):
#     connection = sqlite3.connect(dbname)
#     connection.commit()
#     connection.close()
#
# def createTable():
#     connection = sqlite3.connect(dbname)
#     connection.text_factory = str
#     cursor.execute("""CREATE TABLE product(
#                        id INTEGER PRIMARY KEY autoincrement UNIQUE NOT NULL,
#                        name TEXT NOT NULL,
#                        price INTEGER NOT NULL,
#                        time REAL NOT NULL,
#                        url TEXT NOT NULL)""")
#     connection.commit()
#     connection.close()

#查询价格并对比
productList = []
productInfo = {
    'name': '大数据丛书：数据可视化',
    'price': 50.20,
    'time': time.time(),
    'url': 'http://item.jd.com/11349429.html'
}
productList.append(productInfo)
productList.append(productInfo)
productList.append(productInfo)
# print productList
#查询最小价格
def querryPrice(eachproduct):
    connection = sqlite3.connect('product.sqlite')
    cursor = connection.cursor()
    connection.text_factory = str
    cursor.execute("SELECT price FROM product WHERE name=? ORDER BY price",(eachproduct['name'],))
    minPrices = cursor.fetchall()[0][0]
    connection.commit()
    connection.close()
    return minPrices

print productList
for each in productList:
    minPrice = querryPrice(each)
    print '以往最低价格：%d'%minPrice
    if each['price'] < minPrice:
        print '发现商品：'+each['name']+' 降价啦~'
        print each['name'],each['price']
        print ''
    else:
        pass







#查询时间并转换为localtime
# connection = sqlite3.connect('product.sqlite')
# cursor = connection.cursor()
# cursor.execute("""SELECT time FROM product WHERE price=107.2""")
# timeSec = cursor.fetchall()[0][0]
# print timeSec
# localtime = time.localtime(timeSec)
# print localtime