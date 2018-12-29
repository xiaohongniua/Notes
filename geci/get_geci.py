# encoding: utf-8

import requests
import re
import json
from bs4 import BeautifulSoup
# =============================================================================
# 薛之谦的专辑ID是 5781
# 周杰伦的专辑ID是 6452
# 毛不易的专辑ID是 12138269
# 张韶涵的专辑ID是 10562
# =============================================================================
####################################
#user define
art_name='张韶涵'
art_id=10562


def get_album_info(art_id):
    """
    得到专辑信息
    :param art_id:
    :return:
    """
    urls = "http://music.163.com/artist/album?id={}&limit=100&offset=0".format(art_id)#limit=100对应着网页里面的专辑每页显示100
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': '_iuqxldmzr_=32; _ntes_nnid=dc7dbed33626ab3af002944fabe23bc4,1524151830800; _ntes_nuid=dc7dbed33626ab3af002944fabe23bc4; __utmc=94650624; __utmz=94650624.1524151831.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=94650624.1505452853.1524151831.1524151831.1524176140.2; WM_TID=RpKJQQ90pzUSYfuSWgFDY6QEK1Gb4Ulg; JSESSIONID-WYYY=ZBmSOShrk4UKH5K%5CVasEPuc0b%2Fq6m5eAE91jWCmD6UpdB2y4vbeazO%2FpQK%5CgiBW0MUDDWfB1EuNaV5c4wIJZ08hYQKDhpsHnDeMAgoz98dt%2B%2BFfhdiiNJw9Y9vRR5S4GU%2FziFp%2BliFX1QTJj%2BbaIGD3YxVzgumklAwJ0uBe%2FcGT6VeQW%3A1524179765762; __utmb=94650624.24.10.1524176140',
        'Host': 'music.163.com',
        'Referer': 'https://music.163.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    html = requests.get(urls, headers=headers)
    pattern = re.compile(r'<div class="u-cover u-cover-alb3" title="(.*?)">')
    items = re.findall(pattern, html.text)
    cal = 0
    for i in items:
        cal += 1
        try:
            pattern1 = re.compile(r'<a href="/album\?id=(.*?)" class="tit s-fc0">%s</a>' % (i))
            id1 = re.findall(pattern1, html.text)
            with open("%s_专辑信息.txt"%art_name, 'a') as f:
                f.write('%s\t%s\n'%(i, id1[0]))
        except:
            print('专辑%s获取id有错误！！'%i)
    print("总数是%d" % (cal))
    print("获取专辑以及专辑ID成功！！！！！")


def get_song_info(album_id):
    urls3 = "http://music.163.com/#/album?id={}".format(album_id)
    urls = urls3.replace("[", "").replace("]", "").replace("'", "").replace("#/", "")
    headers = {
        'Cookie': '_iuqxldmzr_=32; _ntes_nnid=dc7dbed33626ab3af002944fabe23bc4,1524151830800; _ntes_nuid=dc7dbed33626ab3af002944fabe23bc4; __utmz=94650624.1524151831.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=94650624.1505452853.1524151831.1524176140.1524296365.3; __utmc=94650624; WM_TID=RpKJQQ90pzUSYfuSWgFDY6QEK1Gb4Ulg; JSESSIONID-WYYY=7t6F3r9Uzy8uEXHPnVnWTXRP%5CSXg9U3%5CN8V5AROB6BIe%2B4ie5ch%2FPY8fc0WV%2BIA2ya%5CyY5HUBc6Pzh0D5cgpb6fUbRKMzMA%2BmIzzBcxPcEJE5voa%2FHA8H7TWUzvaIt%2FZnA%5CjVghKzoQXNM0bcm%2FBHkGwaOHAadGDnthIqngoYQsNKQQj%3A1524299905306; __utmb=94650624.21.10.1524296365',
        'Host': 'music.163.com',
        'Referer': 'http://music.163.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
    }

    html = requests.get(urls, headers=headers)
    soup = BeautifulSoup(html.text, "html.parser")
    book_div = soup.find_all("ul")
    string_array = book_div[0].find_all("li")
    for something in string_array:
        html_data2 = something.find("a").text
        items = re.findall(r"\d+\.?\d*", str(something))[0].replace("'", "")
        with open("%s_歌曲信息.txt"%art_name, 'a') as f:
            if (len(something) > 0):
                f.write('%s\t%s\n'%(html_data2, items))

def get_total_songs_info():
    a=open('%s_专辑信息.txt'%art_name)
    for i in a:
        album_id=i.rstrip('\n').split('\t')[1]
        get_song_info(album_id)
    a.close()

def get_total_lyric():
    file_object = open('%s_歌曲信息.txt'%art_name)
    for i in file_object:
        song_name=i.rstrip('n').split('\t')[0]
        song_id=i.rstrip('n').split('\t')[1]
        
        headers = {
            'Request URL': 'http://music.163.com/weapi/song/lyric?csrf_token=',
            'Request Method': 'POST',
            'Status Code': '200 OK',
            'Remote Address': '59.111.160.195:80',
            'Referrer Policy': 'no-referrer-when-downgrade'
        }
        urls = "http://music.163.com/api/song/lyric?" + "id=" + song_id + '&lv=1&kv=1&tv=-1'
        html = requests.get(urls, headers=headers)
        json_obj = html.text
        j = json.loads(json_obj)
        try:
            lrc = j['lrc']['lyric']
            pat = re.compile(r'\[.*\] |\[.*\]|')
            lrc = re.sub(pat, "", lrc)
            with open("%s_全部歌曲.txt"%art_name, 'a') as f:
                f.write(song_name+'\n')
                f.write(lrc+'*'*50+'\n')
        except:
            print("歌曲有错误 %s !!" % (song_name))
    file_object.close()

if __name__ == '__main__':
    pass
    #get album information
    get_album_info(art_id)
    #根据专辑返回的东西  爬到相关歌曲和信息
    get_total_songs_info()
    get_total_lyric()
