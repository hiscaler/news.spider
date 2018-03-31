# coding=utf-8
import re
import urllib
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from selenium import webdriver


class Browser(object):

    def __init__(self):
        self._site_url = ''
        self._browser = None
        options = webdriver.ChromeOptions()
        options.add_argument('user-data-dir=D:/tmp')
        options.add_argument('-headless')
        options.add_argument('--disable-gpu')
        self._options = options

    def _check(self):
        if self._browser is None:
            raise Exception('webdriver Chrome get error.')

    def open(self):
        self._browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver', options=self._options)
        self._check()

    def get(self, url):
        print(url)
        self._check()
        self._browser.get(url)

    def page_source(self, url):
        url_result = urlparse(url)
        site_url = url_result.scheme
        if site_url:
            site_url += '://' + url_result.netloc + (url_result.port if url_result.port else '')
            self._site_url = site_url
        else:
            raise Exception(url + '地址无效。')

        self.get(url)
        return self._browser.page_source

    def get_all_links(self, page_source, check_func=None):
        links = set()
        soup = BeautifulSoup(page_source)
        for script in soup(["script", "style"]):
            script.decompose()

        links = soup.find_all('a', href=True)
        pattern = re.compile(r'.*href="(\S*)".*')
        post_urls = set()
        for link in links:
            link = link.prettify()
            href = pattern.findall(link)
            if href:
                href = href[0]
                if href and href.find('/article') > -1:
                    if not href.startswith('http'):
                        href = url + href

                    post_urls.add(href)

        return links

    def close(self):
        if self._browser is not None:
            self._browser.close()


if __name__ == '__main__':
    url = 'article/us-britain-russia-diplomats/russia-in-spy-rift-riposte-expels-59-diplomats-from-23-countries-idUSKBN1H612R?il=0'
    print(urllib.parse.urlsplit(url))
    url_result = urlparse(url)
    print(type(url_result))
    site_url = url_result.scheme
    if site_url:
        site_url += '://' + url_result.netloc + (url_result.port if url_result.port else '')
    # site_url = urllib.parse.urljoin('https://www.reuters.com/', url,'a.html')

    print(site_url)
