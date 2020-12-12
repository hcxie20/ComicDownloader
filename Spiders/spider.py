import time
import urllib
import requests
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import os
import re
import threading
import queue
from concurrent.futures import ThreadPoolExecutor
import glob


class Downloader(threading.Thread):
    def __init__(self, max_workers=5):
        threading.Thread.__init__(self)

        self._queue = queue.Queue()
        self.pool = ThreadPoolExecutor(max_workers=max_workers)
        self._max_workers = max_workers
        self._current_workers = 0

        self._fail = queue.Queue()
        self._shutdown = False

    def shutdown(self):
        self._shutdown = True

    def add(self, args):
        self._queue.put(args)

    def run(self):
        while not self._shutdown:
            if self._queue.empty() or self._current_workers == self._max_workers:
                time.sleep(0.05)
                continue

            self.start_download()

        while not self._queue.empty():
            self.start_download()

        self.pool.shutdown(wait=True)

    def start_download(self):
        self._current_workers += 1
        args = self._queue.get()
        task = self.pool.submit(self.download, args)
        task.add_done_callback(self.download_end)

    def download_end(self, future):
        self._current_workers -= 1

    def download(self, args, retry=5):
        url, path, name = args[0], args[1], args[2]
        print('Start download {0}'.format(path + name))

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

        for i in range(retry):
            try:
                req = urllib.request.Request(url = url, headers=headers)
                img = urllib.request.urlopen(req).read()

            except:
                if i == retry - 1:
                    # out of tries
                    self._fail.put(args)
                    return

                continue

        with open(path + "/" + name, "wb") as f:
            f.write(img)
            f.close()

        return True

class spider(object):
    def __init__(self, headless=True, dtLoadPicture=True, disableGPU=True):
        self.downloader = Downloader()
        self.downloader.start()

        self.chrome_option = webdriver.ChromeOptions()
        self.mkdir("./download")

        if dtLoadPicture == True:
            prefs = {"profile.managed_default_content_settings.images":2}
            self.chrome_option.add_experimental_option("prefs",prefs)
        if headless == True:
            self.chrome_option.add_argument("--headless")
        if disableGPU == True:
            self.chrome_option.add_argument("--disable-gpu")

        self.chrome_option.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36')

        self.browser = None

        self.start_browser()

    def boot_up_browser(self):
        self.browser = webdriver.Chrome(options=self.chrome_option)
        self.browser.implicitly_wait(10)

    def start_browser(self):
        self.boot_up_browser()
        pass

    def get_url(self, url):
        print("Getting url...")
        self.browser.get(url)

        title = self.browser.title
        print(title)

        if not os.path.exists("./download/"+title):
            # not finished
            if not os.path.exists("./download/"+title+"_ongoing"):
                os.mkdir("./download/"+title+"_ongoing")

            urls, filenames = self.get_img()

            self.download(urls, filenames, "./download/"+title+"_ongoing")
            os.rename("./download/"+title+"_ongoing", "./download/"+title)
        else:
            print("  File exists")

        pass

    def exit(self):
        self.downloader.shutdown()
        self.browser.quit()

    def get_img(self):
        pass
        return [], []

    def img_tag(self):
        pass

    def add_to_download(self, args):
        self.downloader.add(args)

    def download(self, urls, filenames, path, headers=None):
        print("Start downloading...")
        l = len(urls)
        if headers == None:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
        for i in range(l):
            print("  Img NO. {0:03}".format(i+1))
            req = urllib.request.Request(url = urls[i], headers=headers)
            img = urllib.request.urlopen(req).read()
            # img = requests.get(urls[i], headers=headers)
            with open(path + "/" + filenames[i], "wb") as f:
                f.write(img)
                f.close()

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

class ShouManhuaSpider(spider):
    def start_browser(self):
        print("shoumanhua.com spider v 0.5")
        self.boot_up_browser()

    def get_url(self, url):
        print("Getting url...")
        self.browser.get(url)

        title = self.browser.title
        print(title)

        if not os.path.exists('./download/' + title):
            os.mkdir('./download/' + title)

        a = self.browser.find_element_by_css_selector('body > div.w996.title.pr > span').text
        pages = int(re.search(r'(/)([1-9][0-9]*)', a).group(0)[1:])
        print("Totally {0} pages, processing...".format(pages))

        if len(glob.glob(pathname='./download/' + title + '/*')) == pages:
            print('  File Exists')

        for i in range(pages):
            print("  Page {0}".format(i + 1))
            self.browser.get(url+"?p="+str(i + 1))
            img_url = self.browser.find_element_by_id("qTcms_pic").get_attribute("src")
            _format = re.search(r'\.[a-z]+', img_url.split('/')[-1]).group()
            filename = "{0:03d}".format(i + 1) + _format

            self.add_to_download((img_url, './download/' + title + '/', filename))


if __name__ == "__main__":
    # a = mangabzspider(headless=False, dtLoadPicture=True)
    # url = "http://www.mangabz.com/m66436/"
    # url = "http://www.mangabz.com/m45177/"
    # a.get_url(url)
    # b = CocoSpider(headless=False, dtLoadPicture=True)
    # url = "https://www.cocomanhua.com/10285/1/998.html"
    b = ShouManhuaSpider(headless=False, dtLoadPicture=True)
    url = "http://www.shoumanhua.com/maoxian/14711/455289.html"
    b.get_url(url)
    b.exit()
    pass