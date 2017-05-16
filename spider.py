# -*-coding:utf-8-*-
from requests.exceptions import RequestException
from multiprocessing import Pool
import requests
import re
import os


def get_index_page(page):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'
    headers = {
        'User-Agent': user_agent
    }
    url = 'https://www.qiushibaike.com/text/page/%s/?s=4983114' % page
    try:
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def get_html_content(html):
    article_content = re.compile(r'<h2>(.*?)</h2>.*?<div.*?class="content".*?<span>(.*?)</span>.*?</div>', re.S)
    contents = re.findall(article_content, html)
    for content in contents:
        title = content[0]
        text = content[1].replace('<br/>', '')
        down_text(title, text)


def down_text(title, text):
    path = 'F:/pic/qiubai/'
    if not os.path.exists(path):
        os.mkdir(path)
    file_name = '{0}/{1}.{2}'.format(path, str(title), 'txt')
    if not os.path.exists(file_name):
        with open(file_name, 'w+') as f:
            f.write(text)
            f.close()
            print('保存完成', title)


def main(page):
    html = get_index_page(page)
    get_html_content(html)


if __name__ == '__main__':
    groups = [x for x in range(1, 36)]
    pool = Pool()
    pool.map(main, groups)