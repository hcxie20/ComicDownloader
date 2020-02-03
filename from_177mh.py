from Spiders.xinxinmhspider import xinxin_spider as spider
import re
import os


if __name__ == "__main__":
    if not os.path.exists("./download"):
        os.mkdir("./download")

    
    a = spider(headless=True)

    while 1:
        url = input("Url (exit to exit):")
        # url = "http://www.mangabz.com/38bz/"

        if url == "exit":
            break

        if re.search(r"https://www.177mh.net/", url):
            a.get_url(url)
        else:
            print("Not a valid url (https://www.177mh.net/)")
            pass
    