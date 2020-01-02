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


class spider(object):
    def __init__(self, headless=True, dtLoadPicture=True, disableGPU=True):
        self.chrome_option = webdriver.ChromeOptions()

        self.mkdir("./download")

        if dtLoadPicture == True:
            prefs = {"profile.managed_default_content_settings.images":2}
            self.chrome_option.add_experimental_option("prefs",prefs)
        if headless == True:
            self.chrome_option.add_argument("--headless")
        if disableGPU == True:
            self.chrome_option.add_argument("--disable-gpu")

        self.chrome_option.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1')

        self.browser = None

        self.start_browser()

    def boot_up_browser(self):
        self.browser = webdriver.Chrome(options=self.chrome_option)
        self.browser.implicitly_wait(10)

    def start_browser(self):
        self.boot_up_browser()
        pass

    def get_url(self, url):
        pass

    def img_tag(self):
        pass

    def download(self, urls, filenames, path):
        print("Start downloading...")
        l = len(urls)

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1')]
        urllib.request.install_opener(opener)

        for i in range(l):
            print("  page {0:03d}/{1}".format(i + 1, l))        
            urllib.request.urlretrieve(urls[i], path + "/" + filenames[i])
        pass

    @staticmethod
    def mkdir(dir):
        if not os.path.exists(dir):
            os.mkdir(dir)
        return True


class pufeispider(spider):
    def start_browser(self):
        print("Pufei spider v 0.1")
        self.boot_up_browser()

    def get_url(self, url):
        print("Getting url...")
        self.browser.get(url)

        title = self.browser.title
        print(title)

        if not os.path.exists("./download/"+title):
            # not finished
            if not os.path.exists("./download/"+title+"_ongoing"):
                os.mkdir("./download/"+title+"_ongoing")

            pages = self.browser.find_element_by_class_name("manga-page").text
            pages = int(re.search("(/)([1-9][0-9]*)", pages).group(2))

            urls = [None] * pages
            filenames = [None] * pages
            print("Totally {0} pages, processing...".format(pages))

            i = 1
            while True:
                print("  Page {0}".format(i))
                img = self.browser.find_element_by_css_selector("div.manga-box").find_element_by_tag_name("img").get_attribute("src")

                urls[i-1] = img
                _format = img[img.rfind("."):]
                filenames[i-1] = "{0:03d}".format(i) + _format

                if i == pages:
                    break
                else:
                    i += 1
                    self.browser.find_element_by_css_selector("div.manga-panel-next").click()

            self.download(urls, filenames, "./download/"+title+"_ongoing")
            os.rename("./download/"+title+"_ongoing", "./download/"+title)
            
            pass
        else:
            print("  File exists")


class mangabzspider(spider):
    def start_browser(self):
        print("Mangabz.com spider v 0.5")
        self.boot_up_browser()

    def get_url(self, url):
        print("Getting url...")
        self.browser.get(url)

        title = self.browser.title
        print(title)

        if not os.path.exists("./download/"+title):
            # not finished
            if not os.path.exists("./download/"+title+"_ongoing"):
                os.mkdir("./download/"+title+"_ongoing")

            a = self.browser.find_element_by_class_name("bottom-page2")
            pages = int(re.search(r"[1-9][0-9]*", re.search(r"-[1-9][0-9]*", a.text).group()).group())
            urls = [None] * pages
            filenames = [None] * pages
            print("Totally {0} pages, processing...".format(pages))
            
            url1 = url[:-1]
            for i in range(1, pages+1):
                print("  Page {0}".format(i))
                self.browser.get(url1+"-p"+str(i))
                urls[i - 1] = self.browser.find_element_by_id("cp_image").get_attribute("src")
                _format = re.search(r"\..*\?", re.search(r"com.*\?",urls[i-1]).group()).group()[:-1]
                filenames[i-1] = "{0:03d}".format(i) + _format
                pass

            self.download(urls, filenames, "./download/"+title+"_ongoing")
            os.rename("./download/"+title+"_ongoing", "./download/"+title)
        else:
            print("  File exists")

        pass


class tencentcomicspider(spider):
    def start_browser(self):
        print("Tencent Spider v 1.0")
        self.boot_up_browser()

    def get_url(self, url):
        print("Getting url...")
        self.browser.get(url)
        soup = BeautifulSoup(self.browser.page_source, "lxml")
        try:
            name = soup.find("span", attrs={"class":"title-comicHeading"}).contents[0]
        except:
            print("Access denied. Accessing from a banned ip")
            return -1

        self.browser.find_element_by_id("crossPage").click()

        soup = BeautifulSoup(self.browser.page_source, "lxml")
        imgs = soup.find_all(self.img_tag)
        # imgs contains urls for imgs

        print("Getting imgs...")
        urls = []
        for img in imgs:
            try:
                urls.append(img.attrs["data-src"])
            except:
                urls.append(img.attrs["src"])
        urls.reverse()

        self.dowoload(name, urls)

    @staticmethod
    def dowoload(name, urls):
        print("Creating ./download/{0}...".format(name))
        if not os.path.exists("./download/"+name):
            os.mkdir("./download/"+name)

        # print(urls)
        
        print("  Totally {0} images".format(len(urls)))
        for i in range(len(urls)):
            print("    Img {0}/{1}".format(i+1, len(urls)))
            file_name = str(i+1)
            if len(file_name) == 1:
                file_name = "0" + file_name
            file_name = file_name + ".jpg" 
            if not os.path.exists("./download/"+name+"/"+file_name):
                print("      Downloading...")
                urllib.request.urlretrieve(urls[i], "./download/"+name+"/"+file_name)
            else:
                print("      File exists")
        pass

    @staticmethod
    def img_tag(tag):
        return tag.name == "img" and tag.has_attr("data-h") and not tag.has_attr("class")

if __name__ == "__main__":
    # a = mangabzspider(headless=False, dtLoadPicture=True)
    # url = "http://www.mangabz.com/m66436/"
    # url = "http://www.mangabz.com/m45177/"
    # a.get_url(url)
    b = pufeispider(headless=False, dtLoadPicture=True)
    url = "http://m.pufei.net/manhua/351/117476.html"
    b.get_url(url)
    pass