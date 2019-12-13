from Spiders.spider import mangabzspider as spider
import re
import os


if __name__ == "__main__":
    if not os.path.exists("./download"):
        os.mkdir("./download")

    
    a = spider(headless=False)

    while 1:
        url = input("Url (exit to exit):")
        # url = "http://www.mangabz.com/38bz/"

        if url == "exit":
            break

        if re.search(r"mangabz.com/m", url):
            a.get_url(url)
        else:
            a.browser.get(url)
            a.browser.find_element_by_class_name("detail-list-form-more").click()
            urls = a.browser.find_elements_by_class_name("detail-list-form-item")
            print("Totally {0} comics".format(len(urls)))
            for i in range(len(urls)):
                urls[i]= urls[i].get_attribute("href")
            urls.reverse()
            i = 1
            for url in urls:
                print("No. {0}:".format(i))
                a.get_url(url)
                i += 1
            print("Done")
            pass
    