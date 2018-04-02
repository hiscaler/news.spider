# coding=utf-8
import re
import urllib
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException


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
        try:
            self._browser.get(url)
        except TimeoutException as ex:
            print(str(ex))

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

    def get_all_links(self, page_source, valid_url_fun=None):
        all_links = set()
        soup = BeautifulSoup(page_source, 'lxml')
        for script in soup(["script", "style"]):
            script.decompose()

        links = soup.find_all('a', href=True)
        pattern = re.compile(r'.*href="(\S*)".*')
        for link in links:
            link = link.prettify()
            href = pattern.findall(link)
            if href:
                href = href[0]
                if href and valid_url_fun(href):
                    if not href.startswith('http'):
                        href = urllib.parse.urljoin(self._site_url, href)

                    all_links.add(href)

        return all_links

    def close(self):
        if self._browser is not None:
            self._browser.close()


def test_check_url(href=None):
    if href and href.find('viewmode') > -1:
        return True
    else:
        return False


if __name__ == '__main__':
    url = 'https://blog.csdn.net/handsomekang/article/details/41446319'
    print(urllib.parse.urlsplit(url))
    url_result = urlparse(url)
    print(type(url_result))
    site_url = url_result.scheme
    if site_url:
        site_url += '://' + url_result.netloc + (url_result.port if url_result.port else '')
    site_url += url_result.path
    if url_result.query:
        site_url += '?' + url_result.query
    print("Site URL = " + site_url)

    html = """ <ul>
            <li id="btnContents"><a href="https://blog.csdn.net/handsomekang?viewmode=contents"><span
                    onclick="_gaq.push(['_trackEvent','function', 'onclick', 'blog_articles_mulu'])">
                    <img src="https://csdnimg.cn/release/phoenix/images/ico_list.gif">目录视图</span></a></li>
            <li id="btnView"><a href="https://blog.csdn.net/handsomekang?viewmode=list"><span
                    onclick="_gaq.push(['_trackEvent','function', 'onclick', 'blog_articles_zhaiyao'])">
                    <img src="https://csdnimg.cn/release/phoenix/images/ico_summary.gif">摘要视图</span></a></li>
            <li id="btnRss"><a href="https://blog.csdn.net/handsomekang/rss/list"><span
                    onclick="_gaq.push(['_trackEvent','function', 'onclick', 'blog_articles_RSS'])">
                    <img src="https://csdnimg.cn/release/phoenix/images/ico_rss.gif">订阅</span></a></li>
                    </ul>"""
    browser = Browser()
    links = browser.get_all_links(html, test_check_url)
    print("Result:")
    print(links)
