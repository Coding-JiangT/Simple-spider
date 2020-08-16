# Beautiful Soup框架
# Scrapy
# 爬虫、反爬虫
# 频繁爬取会导致被封，解决办法有使用代理IP




# 前奏：
# 1、明确爬虫的目的
# 2、找到数据对应的网页
# 3、分析网页的结构，找到数据所在的标签位置

# 模拟http请求，向服务器发送这个请求，获取服务器返回的html
# 用正则表达式提取我们要的数据

# 在该简易爬虫中，爬取虎牙的英雄联盟直播中各主播的人气排名
import urllib.request
import re

class Spider():
    # 将要爬取的网站的URL作为类变量，即该类专门用来爬取该网站的信息
    url = 'https://www.huya.com/g/2336'
    root_regex = '<span class="txt">([\w\W]*?)</li>'  # 找到包含了主播名和主播人气的所有信息段
    # 找到所有信息段中每个主播的名字和对应的人气
    child_regex = '<i class="nick" title="([\w\W]*?)">[\w\W]*<i class="js-num">([\w\W]*?)万</i>'
    
    # private 发起http请求，获取网站相应的html信息
    def __fetch_contant(self):
        with urllib.request.urlopen(self.__class__.url) as f: # 实现http请求
            html = f.read().decode('utf-8')
        # html = str(html, encoding = 'utf-8')
        
        return html
    
    # private, 对获得的html进行数据分析和提取
    def __analysis(self, html):
        root_html = re.findall(self.__class__.root_regex, html)  # 提取包含所有主播的信息，list
        # print(root_html[1])
        func = lambda x: re.findall(self.__class__.child_regex, x)  # 匿名函数，找到每个主播的info

        # 返回结果为map obj，其实就是一个迭代器，迭代器中的每个元素都是[('卡尔', '709.7万')]的类型
        return map(func, root_html)  

    # private, 对数据进行再处理
    def __refine(self, anchors):
        func = lambda x: {'name': x[0][0], 'pop':x[0][1]}
        
        return map(func, anchors)  # 返回map object

    # private, 对数据排序
    def __sort(self, anchors):
        func = lambda x: float( re.sub(',', '', x['pop']) )  # 如果出现千万级别的人气，则要把会出现的','号去除
        pop_ranking = sorted(anchors, key = func, reverse = True)  # 根据每个元素的人气值来排序
        
        return pop_ranking  # 返回排行榜

    # private, 展示数据
    def __show(self, pop_ranking):
        print('    英雄联盟直播人气排行榜    \n')
        print('ID                     人气/万')
        for anchor in pop_ranking:
            margin = 16 - len(anchor['name'])
            print(anchor['name'] + ' '*margin + anchor['pop'] + '万')

    # 将排行榜信息写入指定文件（路径）
    def __save_file(self, pop_ranking, file_path):
        with open(file_path, 'w') as file_object:
            file_object.write( str(pop_ranking) )

    # 公开方法，入口
    def go(self, file_path):
        html = self.__fetch_contant()
        anchors = self.__analysis(html)  # 主播的信息
        anchors_mod = self.__refine(anchors)  # 再修改后的主播的信息
        pop_ranking = self.__sort(anchors_mod)  # 排好序的
        self.__save_file(pop_ranking, file_path)  # 写入文件
        self.__show(pop_ranking)  # 展示排行榜


spider = Spider()  # 实例化一个对象
file_path = r'E:\Visual Studio Code Projects\Python\spider\game_2336_pop_ranking.txt'
spider.go(file_path)
# print(popularity_ranking)
# print(len(obj[0][0]))
# print('\n')
