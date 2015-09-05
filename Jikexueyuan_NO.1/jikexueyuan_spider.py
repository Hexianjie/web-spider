# -*- coding: utf-8 -*-
import requests
import re
import sys

PATTERN = 'pageNum='
reload(sys)
sys.setdefaultencoding("utf-8")

class Spider():
    def __init__(self):
        print '初始化爬虫...'

    # 生成页面链接列表
    def generate_url_list(self,url,pange_number):
        # now_page = int(re.search('pageNum=\d+',url).group(1))
        url_list = []
        for number in range(1,pange_number+1):
            page_url = re.sub('pageNum=\d+','pageNum=%d'%number,url,re.S)
            url_list.append(page_url)
        return url_list

    # 获取页面源代码
    def get_source(self,url):
        html = requests.get(url)
        return html.text
    # 获取课程块列表
    def get_class_list(self,html):
        all_class_list = re.findall('(<li id=".*?</li>)',html,re.S)
        return all_class_list
    #  获取每个课程信息，保存到字典info
    def get_class_info(self,each_class):
        info = {}
        info['title'] = re.search('class="lessonimg" title="(.*?)" alt="',each_class,re.S).group(1)
        info['content'] = re.search('<p style="height: 0px; opacity: 0; display: none;">(.*?)</p>',each_class,re.S).group(1).strip()
        time_and_level = re.findall('<em>(.*?)</em>',each_class,re.S)
        info['classtime'] = re.sub('\s+','',time_and_level[0])      #使用正则表达去除空白符号：\t\n
        info['classlevel'] = time_and_level[1]
        info['learnnum'] = re.search('"learn-number">(.*?)</em>',each_class,re.S).group(1)
        return info
    # 保存所有课程信息列表class_list到 info.txt
    def save_class_info(self,class_list):
        with open('info.txt','w') as data:
            for each in class_list:
                data.writelines('title: '+each['title']+'\n')
                data.writelines('content:' + each['content'] + '\n')
                data.writelines('classtime:' + each['classtime'] + '\n')
                data.writelines('classlevel:' + each['classlevel'] + '\n')
                data.writelines('learnnum:' + each['learnnum'] +'\n\n')

if __name__ == '__main__':
    url = 'http://www.jikexueyuan.com/course/python/?pageNum=1'
    jikespider = Spider()
    url_list = jikespider.generate_url_list(url,2)          #生成两页链接

    class_list = []             #保存所有课程信息列表
    for each_url in url_list:
        print '正在处理页面：%s'%each_url
        html = jikespider.get_source(each_url)
        all_class_list = jikespider.get_class_list(html)
        for each_class in all_class_list:
            class_info = jikespider.get_class_info(each_class)
            print '\t处理课程： '+class_info['title']+'完毕。'
            class_list.append(class_info)
    jikespider.save_class_info(class_list)
    print '\n保存所有课程信息到info.txt完毕。'
