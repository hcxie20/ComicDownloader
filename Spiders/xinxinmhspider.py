import time
import urllib
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import os
import re

import spider


class xinxin_spider(spider.spider):
    def start_browser(self):
        print("177mh v 0.1")
        self.boot_up_browser()

    def get_img(self):        
        tmp = self.browser.find_element_by_css_selector("select.selectTT").find_elements_by_tag_name("option")
        nums = len(tmp)
        urls = [None] * nums
        filenames = [None] * nums

        urls[0] = self.browser.find_element_by_css_selector("img#dracga").get_attribute("src")
        filenames[0] = "{0:03}.jpg".format(1)

        for i in range(1, nums):
            self.browser.find_element_by_css_selector("a.pNext").click()
            urls[i] = self.browser.find_element_by_css_selector("img#dracga").get_attribute("src")
            filenames[i] = "{0:03}.jpg".format(i+1)
        return urls, filenames
    
    def download(self, urls, filenames, path):
        print("Start downloading...")
        l = len(urls)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        }
        #Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36
        for i in range(l):
            # req = urllib.request.Request(url = urls[i], headers=headers)
            # img = urllib.request.urlopen(req).read()
            # # img = requests.get(urls[i], headers=headers)
            # with open(path + "/" + filenames[i], "wb") as f:
            #     f.write(img)
            #     f.close()
            self.browser.get(urls[i])
            img = self.browser.find_element_by_tag_name("img")
            action = ActionChains(self.browser).move_to_element(img)
            action.context_click(img)
            action.send_keys(Keys.ARROW_DOWN)
            action.send_keys('V')
            action.perform()
            print(self.browser.page_source)
        pass

if __name__ == "__main__":
    b = xinxin_spider(headless=False, dtLoadPicture=False)
    url = "https://www.177mh.net/202001/438701.html"
    b.get_url(url)
    pass