import time

from bs4 import BeautifulSoup
from curl_cffi import requests
from multiprocessing import Queue
from collections import deque

from curl_cffi.requests.exceptions import DNSError


def extract_news_header_link():
    r = requests.get("https://tw.news.yahoo.com//world/archive/", impersonate="chrome")
    soup = BeautifulSoup(r.content, 'html5lib')
    stream_news_list = soup.find_all("a", {'class': 'mega-item-header-link'})
    return stream_news_list


def extract_news_content(url):
    r = requests.get(url, impersonate="chrome")
    soup = BeautifulSoup(r.content, 'html5lib')
    content = soup.find_all("div", {'class': 'caas-body'})[0]
    paragraphs = content.find_all('p')
    all_text = ' '.join(p.get_text(strip=True) for p in paragraphs)
    return all_text


def news_feeder(queue: Queue):
    news = deque()
    base_url = 'https://tw.news.yahoo.com'

    while True:

        if len(news) == 0:
            stream_news_list = extract_news_header_link()[:15]
            stream_news_list.reverse()
            for elem in stream_news_list:
                news.append(elem)

        if not queue.full():
            elem = news.pop()
            try:
                content = extract_news_content(base_url + elem.attrs['href'])
                queue.put(content)
            except DNSError:
                continue

        time.sleep(30)
