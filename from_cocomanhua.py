from Spiders.spider import CocoSpider as spider
import re
import os


if __name__ == "__main__":
    if not os.path.exists("./download"):
        os.mkdir("./download")

    a = spider(headless=True)

    while 1:
        url = input("Url (exit to exit):")
        # url = "https://www.cocomanhua.com/10285/"
        # url = 'https://www.cocomanhua.com/14311/'

        if url == "exit":
            break

        if len(url.split('/')) == 6:
            a.get_url(url)

        else:
            a.browser.get(url)

            urls = a.browser.find_elements_by_css_selector('div.all_data_list > ul > li > a')

            print("Totally {0} comics".format(len(urls)))
            for i in range(len(urls)):
                urls[i]= urls[i].get_attribute("href")
            urls.reverse()

            for i, url in enumerate(urls):
                print("No. {0}:".format(i + 1))
                a.get_url(url)
            print("Done")
            pass
