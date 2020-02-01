import time
import urllib
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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
        url_this = self.browser.current_url
        
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


if __name__ == "__main__":
    b = xinxin_spider(headless=False, dtLoadPicture=False)
    url = "https://www.177mh.net/202001/438701.html"
    b.get_url(url)
    pass