import time

from bs4 import BeautifulSoup
from curl_cffi import requests
from multiprocessing import Queue
from collections import deque

from curl_cffi.requests.exceptions import DNSError


def extract_yahoo_news_header_link():
    base_url = "https://tw.news.yahoo.com"
    r = requests.get("https://tw.news.yahoo.com/archive/", impersonate="chrome")
    soup = BeautifulSoup(r.content, 'html5lib')
    stream_news_list = soup.find_all("a", {'class': 'mega-item-header-link'})
    news_list = []
    for elem in stream_news_list:
        news_list.append(base_url + elem.attrs['href'])
    news_list.reverse()
    return news_list


def extract_yahoo_news_content(url):
    base_url = "https://tw.news.yahoo.com/"
    r = requests.get(url, impersonate="chrome")
    soup = BeautifulSoup(r.content, 'html5lib')
    content = soup.find_all("div", {'class': 'caas-body'})[0]
    paragraphs = content.find_all('p')
    # title = soup.find('h1')
    all_text = ' '.join(p.get_text(strip=True) for p in paragraphs)
    return all_text


def extract_cna_news_header_link():
    base_url = "https://www.cna.com.tw"
    cmd_url = "/list/aall.aspx"
    r = requests.get(base_url + cmd_url, impersonate="chrome")
    soup = BeautifulSoup(r.content, 'html5lib')
    content = soup.find_all("ul", {'id': 'jsMainList'})
    news_list = []
    for elem in content[0].find_all('a'):
        if elem.attrs['href'][1:5] != "news":
            continue
        news_list.append(base_url + elem.attrs['href'])
    news_list.reverse()
    return news_list


def extract_cna_news_content(url: str):
    r = requests.get(url, impersonate="chrome")
    soup = BeautifulSoup(r.content, 'html5lib')
    title = soup.find('h1')
    content = soup.find_all("div", {'class': 'paragraph'})[0]
    paragraphs = content.find_all('p')
    all_text = ' '.join(p.get_text(strip=True) for p in paragraphs)
    return title.get_text() + " " + all_text


def news_feeder(queue: Queue, news_supplier: str):
    news = deque()

    while True:

        if len(news) == 0:
            if news_supplier == "CNA":
                stream_news_list = extract_cna_news_header_link()
            if news_supplier == "YAHOO":
                stream_news_list = extract_yahoo_news_header_link()
            for elem in stream_news_list:
                news.append(elem)

        if not queue.full():
            link = news.pop()
            try:
                if news_supplier == "CNA":
                    content = extract_cna_news_content(link)
                if news_supplier == "YAHOO":
                    content = extract_yahoo_news_content(link)
                queue.put(content)
            except DNSError:
                continue

        time.sleep(30)
