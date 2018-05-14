#encoding=utf-8
import json,time,datetime,requests,re
from insert import insert
from lxml import etree
class QuTouTiao(insert):
    def __init__(self):
        insert.__init__(self)
    def getjson(self):
        dict = {'娱乐': 6,'健康': 42,'养生': 5,'励志': 4,'科技': 7,'生活': 8,'财经': 10,'汽车': 9,'星座': 18,'美食': 12,'时尚': 14,'游戏': 19,'育儿': 17,'军事': 15,'体育': 13}
        for key,value in dict.items():
            print(key,value)
            remark = key
            value = value
            for page in range(1,3):
                url = 'http://api.1sapp.com/content/outList?cid=' + str(value) + '&tn=1&page=' + str(page) + '&limit=10&user=temporary'
                print(url)
                url_type = 1
                jsona = self.getcontent(url,url_type)
                jsona = json.loads(jsona)
                data = jsona['data']
                datas = data['data']
                print(datas)
                for data in datas:
                    url = data['url']
                    url = url.split('&key=')[0].replace('\/','/')
                    title = data['title']
                    timestr = data['publish_time']
                    timestr = int(timestr)/1000
                    timestr = str(timestr).split('.')[0]
                    timea = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestr)))
                    visited_count = data['read_count']
                    print(url,title,visited_count,remark)
                    table = 't_texts'
                    index = 1
                    mapx = {}
                    mapx['linkUri'] = url
                    mapx['title'] = title
                    mapx['visited_count'] = visited_count
                    mapx['type'] = 111
                    mapx['nature'] = 111
                    mapx['create_time'] = timea
                    mapx['remark'] = remark
                    result = self.select(title)
                    if int(result) == 1:
                        insertid = self.insert(table,mapx)
                        self.gettext(url,title,visited_count,index,insertid)
    def gettext(self,url,title,visited_count,index,insertid):
        url_type = 1
        text = self.getcontent(url,url_type).decode('utf-8')
        text = etree.HTML(text).xpath('//div[@class="content"]//text() | //div[@class="content"]//img//@data-src')
        table = 't_text_html'
        for p in text:
            if '//' in p:
                type = 2
            else:
                type = 1
            mapx ={}
            mapx['text_id'] = insertid
            mapx['sort'] = index
            mapx['type'] = type
            mapx['html'] = p
            self.insert(table,mapx)
            index = index + 1
        return index
    def select(self,title):
        selecturl = 'https://apipre.xiaomatv.cn/V3/Article/checkArticle?title=' + title
        print(selecturl)
        result = requests.get(selecturl).text
        print(result)
        return result
    def getcontent(self,url,url_type):
        if url_type == 1:
            text = requests.get(url).content
            return text
qutoutiao = QuTouTiao()
qutoutiao.getjson()