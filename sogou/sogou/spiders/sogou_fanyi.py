# -*- coding: utf-8 -*-

import scrapy
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re


class SogouFanyi(scrapy.Spider):
    name = 'sogou_fanyi'
    page_index = 1

    start_urls = [
        'https://translate.sogoucdn.com/pcvtsnapshot?url=https%3A%2F%2Fwww.msn.com%2Fen-us%2Fnews%2Fpolitics%2Ftrump-takes-victory-lap-on-mccabe-firing-a-great-day-for-democracy%2Far-BBKkbJX%3Fli%3DBBnbcA1&query=&tabMode=1&noTrans=0&tfr=web_en&from=en&to=zh-CHS&_t=1521270440240'
    ]

    def __init__(self):
        browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver')
        browser.get(self.start_urls[0])
        scriptArray = """localStorage.setItem("TRANSPAGE_DIALOG_SHOW", '1');
                            """
        result = browser.execute_script(scriptArray)
        time.sleep(10)
        browser.switch_to.frame('translate-iframe-dest')
        time.sleep(10)
        # button_ok = browser.find_element_by_xpath('//button[@class="sm-dialog-button"]')
        # print(button_ok)
        # buttons = browser.find_elements_by_class_name('sm-dialog-button')
        # print(buttons)


        page_source = browser.page_source
        # print(page_source)
        soup = BeautifulSoup(page_source)
        obj = soup.select_one('div.articlecontent > h1')
        print(obj)
        browser.close()

    def parse(self, response):
        if not response or response is None:
            return

        print(response)

        raw_data = response.xpath('//div[@class="articlecontent"]')
        print(raw_data)
