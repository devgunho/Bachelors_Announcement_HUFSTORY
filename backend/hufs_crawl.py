import re
import os
import requests
import json
import string
from bs4 import BeautifulSoup
import datetime
from dateutil.parser import parse
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


import os
# Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hufs_crawl.settings")
# 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
django.setup()

from post.models import Bachelor_data

def get_list_article_headline(url):
    link = []

    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    article = soup.find_all('tr')[1:40]

    p = re.compile('\S')

    for i in article:
        notification = i.find('td').find('span', class_='mini_eng')
        # 공지 아닌것들
        if notification:
            arr = []
            data = []

            text_notification = ''.join(p.findall(i.find('td', class_='title').text.strip()))

            # mini_eng의 content : 순서대로 ( 번호, 작성자, 작성일, 조회수)
            for notification_td in i.select('td'):
                for mini_eng_class in notification_td.find_all('span', class_='mini_eng'):
                    if mini_eng_class:
                        data.append(mini_eng_class.text.strip())

            arr.append(text_notification)
            arr.append('http://builder.hufs.ac.kr/user/' + i.a['href'])
            data += arr
            link.append(data)
    return link


def parse_bechelor():
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    url_list = {
        "학사_게시판": 'http://builder.hufs.ac.kr/user/indexSub.action?codyMenuSeq=37080&siteId=hufs&menuType=T&uId=4&sortChar=AB&linkUrl=04_0202.html&mainFrame=right&dum=dum&boardId=109336176&page=',
    }

    bachelor_data = []
    bachelor_data_json = {}

    #for i in url_list.values():
    #   result = {**result, **get_list_article_headline(i)}
    for i in range(1, 4):
        bachelor_url = url_list['학사_게시판'] + str(i)
        bachelor_data += get_list_article_headline(bachelor_url)

    for n in range(len(bachelor_data)):
        bachelor_data_json[bachelor_data[n][0]] = bachelor_data[n][1:]

    return bachelor_data_json


if __name__ == '__main__':
    Bachelor_dict = parse_bechelor()

    for n, d in Bachelor_dict.items():
        try:
            Bachelor_data.objects.get(number=n)
        except Exception:
            Bachelor_data(number=n, data=d).save()
            try:
                Bachelor_data.objects.get(number=int(n)-45).delete()
            except Exception:
                pass
            print('Number {} new'.format(n))
