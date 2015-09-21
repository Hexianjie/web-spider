# -*- coding: utf-8 -*-
import requests
import re
import sys
import time
import sqlite3
import mail
##设置系统shell编码，不设的话shell输出为乱码。
reload(sys)
sys.setdefaultencoding("utf-8")
#获取页面源代码
def getSource(url):
    cookie = {"Cookie":'__jda=122270672.1199899340.1437205060.1442463454.1442465572.80; __jdv=122270672|c.duomai.com|t_16282_29835855|tuiguang|79a1da8fca9c4d22b05b76d4a6fdf176; __jdu=1199899340; TrackID=1bcn4aXfYQvOZe23IiPKFK1Nix4YOLWXUeY4-EUdnhfiJL3h9aObC74Pisf3qjm740olCs_DbpP3XUnjTfCvwAueUp3pzo1Aayd1Up5UdSos; pinId=vhJ6rXYMaWxjvB5oK0iAKg; lighting=8FDB324A4157FBC72AB5A068BCDCDD1444C6F9228E8E30E247FEB0366D5F56C0035C052C323D139583F7F69931BEDDCA27CD1D1807CE74E13BDC2886035E85715772F6F2DBBB4F338602EBFB39F3710971CC3926EC77EEFC2FB560E49D13F3ECF55BB10B494848AAE1545F0243F39ABAED583F066EAE86424DB04F7399802FB7C1A8B03CB07C1207CCBC487483C2AAED; cart-main=xx; cn=6; ipLocation=%u5317%u4EAC; areaId=1; __utmz=122270672.1438497488.1.1.utmcsr=trade.jd.com|utmccn=(referral)|utmcmd=referral|utmcct=/shopping/order/getOrderInfo.action; dmpjs=dmp-d1532155f101e8796b68.24514700; __jdc=122270672; user-key=7ef1be5c-fe1e-4537-95b0-ed61b53c6b8f; _tp=U51GU9R8xUKxEdxvvGznpQ%3D%3D; _pst=maiqianqin; unick=maiqianqin; pin=maiqianqin; thor=9C77AD000056B07E7450D206D441C583E13E31F8711F8905BD175B4AD6048F492DC60ED4094FAFA17DD0E8D11F5E543DED1F42312CFDFC5F03DCD47A687C3B80B6BE46BC1253CC5A1DFDEDBDEFB509C56F5B30215FBC541D79AE75BE33FE365FFA285A2647CBA7245C9267EBD78D130D34B7283C2C72D11645ED368CE91C819CDEA37C8F6A70E4B2813DDDA3C37694C4; __jdb=122270672.3.1199899340|80.1442465572; ipLoc-djd=1-72-2799-0'}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"
                      "\ *0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive"
        }
    html = requests.get(url,cookies=cookie,headers=headers).text
    return html

#获取商品页面源代码到列表 productListText
def getProductListText():
    url = 'http://cart.jd.com/cart'
    productListText = []
    try:
        html = getSource(url)
        productListText = re.findall('(<div class="item-form">.*?<div class="item-line">)',html,re.S)
    except:
        pass
    return productListText

#获取商品信息到字典 ProductInfo
def getProductInfo(chunk):
    productIonfo = {}
    productIonfo['name'] = re.search('<img alt="(.*?)" clstag',chunk,re.S).group(1)
    a = float(re.search('<strong>(.*?)</strong>',chunk,re.S).group(1))
    productIonfo['price'] = float('%0.1f'%a)
    productIonfo['url'] = re.search('<a href="(.*?)" target=',chunk,re.S).group(1)
    productIonfo['time'] = time.time()
    return productIonfo

#保存商品信息到数据库
def saveToSqlite(productList):
    connection = sqlite3.connect('product.sqlite')
    cursor = connection.cursor()
    connection.text_factory = str

    for each in productList:
        cursor.execute("""INSERT INTO product(name,price,time,url) VALUES (?,?,?,?)""",
               (each['name'],
                each['price'],
                each['time'],
                each['url']))
    connection.commit()
    connection.close()

#查询商品价格
def querryPrice(eachproduct):
    connection = sqlite3.connect('product.sqlite')
    cursor = connection.cursor()
    connection.text_factory = str
    cursor.execute("SELECT price FROM product WHERE name=? ORDER BY price",(eachproduct['name'],))
    minPrice = 0.0
    try:
        minPrice = cursor.fetchall()[0][0]
    except IndexError as e:
        minPrices = 0.0
    connection.commit()
    connection.close()
    return minPrice

if __name__ == '__main__':
    #获取商品页面源代码到列表 productListText
    productListText = getProductListText()

    #保存商品信息到列表 productList
    productList= []
    for each in productListText:
        productIonfo = getProductInfo(each)
        productList.append(productIonfo)
    if productList:
        print u'完成添加商品信息到productList.'
        print u'抓取到 %d 个商品：\n'%len(productList)
    else:
        print u'抓取商品信息失败,估计是网络不行~'
    # print productList[0]

    #对比历史最低价格并提取降价商品商品到列表 discountedProducts
    discountedProducts = []
    for each in productList:
        print u'《%s》：%0.1f'%(each['name'],each['price'])
        minPrice = querryPrice(each)
        if each['price'] < minPrice:     #对比历史最低价格
            minusPrice = minPrice- each['price']
            each['minusPrice'] = minusPrice
            discountedProducts.append(each)

    #保存商品信息到数据库
    saveToSqlite(productList)

    #输出降价商品
    print ''
    print u'降价商品：'
    contentList=[]
    for each in discountedProducts:
        print u'《%s》降价 %fRMB 啦~现价为:%sRMB'%(each['name'],each['minusPrice'],each['price'])
        content = '《'+each['name']+'》'+' 降价'+str(each['minusPrice'])+'啦~现价为:'+str(each['price'])
        contentList.append(content)

    #发送邮件
    if discountedProducts:
        mailto_list=['hexianjie1995@qq.com'] #此处填写接收邮件的邮箱
        title = u"购物车商品降价了~"                      #此处填写邮件主题
        content = '\n'.join(contentList)             #此处填写邮件内容
        mail = mail.Mailhelper(mailto_list)
        if mail.send_mail(title,content):
            print u"发送提醒邮件成功"
        else:
            print u"发送失败"





