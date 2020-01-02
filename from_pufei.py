from Spiders.spider import pufeispider as spider
import re
import os


if __name__ == "__main__":
    if not os.path.exists("./download"):
        os.mkdir("./download")

    
    a = spider(headless=True)

    while 1:
        # url = input("Url (exit to exit):")
        url = "http://m.pufei.net/manhua/351/"

        if url == "exit":
            break

        if re.search(r"html", url):
            a.get_url(url)
        else:
            a.browser.get(url)
            chapters = a.browser.find_element_by_class_name("chapter-list").find_elements_by_tag_name("a")
            
            print("Totally {0} comics".format(len(chapters)))

            urls = [None] * len(chapters)
            for i in range(len(chapters)):
                urls[i] = chapters[i].get_attribute("href")
                chapters[i] = chapters[i].text
            
            for i in range(len(chapters)):
                print("No. {0:03}: {1}".format(i+1, chapters[i]))
                a.get_url(urls[i])
            print("Done")
            pass
    