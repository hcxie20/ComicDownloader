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

def img_tag(tag):
    return tag.name == "img" and tag.has_attr("data-h") and not tag.has_attr("class")
    

if __name__ == "__main__":
    if not os.path.exists("./download"):
        os.mkdir("./download")

    url = "http://www.hanhuazu.cc/comics/detail/11759"
    url = "https://ac.qq.com/ComicView/index/id/505430/cid/982"
    url = input("URL: ")


    chrome_option = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_option.add_experimental_option("prefs",prefs)
    chrome_option.add_argument("--headless")
    chrome_option.add_argument("--disable-gpu")
    browser = webdriver.Chrome(options=chrome_option)
    chrome_option.add_argument('user-agent="Mozilla/5.0(X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"')
    browser.implicitly_wait(10)

    if re.search(r"hanhuazu", url):
        print("This is a shuhui url")
        print("Getting url...")
        browser.get(url)
        # time.sleep(5)
        WebDriverWait(browser,10).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR,'h1')))
        # print(browser.page_source)
        # soup = BeautifulSoup(browser.page_source, "lxml")
        # print(soup.prettify())

        # time.sleep(0.5)
        soup = BeautifulSoup(browser.page_source, "lxml")
        name = soup.find("h1").contents[0]
        print("The name is {0}".format(name))
        # element = browser.find_element_by_css_selector("h1")
        # name = element.text

        print("Into page mode...")
        pattern = re.compile(".?z-page")
        # a = soup.find("span", attrs={"class":pattern})
        # print(soup.prettify())
        while soup.find("span", attrs={"class":pattern}):
            # print(soup.prettify())
            browser.find_element_by_css_selector("span.tips.z-page").click()
            time.sleep(1)
            soup = BeautifulSoup(browser.page_source, "lxml")
        browser.execute_script("window.scrollTo(0,100000)")
        # too slow
        # WebDriverWait(browser,10).until_not(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'span.u-comics-img')))
        time.sleep(1)

        soup = BeautifulSoup(browser.page_source, "lxml")
        # print(soup.prettify())

        print("Getting sources...")
        imgs = soup.find_all("img", attrs={"class":"u-comics-img"})
        if len(imgs)==0:
            print(soup.prettify())
            print("Something went wrong!")
            exit(1)

        print("Creating foulder")
        if not os.path.exists("./download/"+name):
            os.mkdir("./download/"+name)

        print("Start downloading...")
        for img in imgs:
            file_name = img.attrs["alt"]
            file_src = img.attrs["src"]
            if not (re.match(r"00", file_name) or re.match(r"sp", file_name)):
                print("  Downloading {0}".format(file_name))
                urllib.request.urlretrieve(file_src, "./download/"+name+"/"+file_name)

    elif re.search(r"ac.qq.com", url):
        print("This is a Tencent url")
        print("Getting url...")
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, "lxml")
        name = soup.find("span", attrs={"class":"title-comicHeading"}).contents[0]

        browser.find_element_by_id("crossPage").click()


        soup = BeautifulSoup(browser.page_source, "lxml")
        imgs = soup.find_all(img_tag)

        print("Creating ./download/{0}...".format(name))
        if not os.path.exists("./download/"+name):
            os.mkdir("./download/"+name)
        print("Getting imgs...")
        urls = []
        for img in imgs:
            try:
                urls.append(img.attrs["data-src"])
            except:
                urls.append(img.attrs["src"])
        # print(urls)
        urls.reverse()
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
    else:
        print("What the hell is this?")
    pass

