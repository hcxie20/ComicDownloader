from Spiders.spider import ShouManhuaSpider as spider
import re
import os


if __name__ == "__main__":
    if not os.path.exists("./download"):
        os.mkdir("./download")

    a = spider(headless=True)

    while 1:
        # url = input("Url (exit to exit):")
        url = "http://www.shoumanhua.com/maoxian/14711/"

        if url == "exit":
            break

        if len(url.split('/')) == 4:
            a.get_url(url)

        else:
            a.browser.get(url)

            urls = a.browser.find_elements_by_css_selector('#mh-chapter-list-ol-0 > li > a')[:193]

            print("Totally {0} comics".format(len(urls)))
            for i in range(len(urls)):
                urls[i]= urls[i].get_attribute("href")
            urls.reverse()

            for i, url in enumerate(urls):
                print("No. {0}:".format(i + 1))
                a.get_url(url)
            print("Done")
            pass
