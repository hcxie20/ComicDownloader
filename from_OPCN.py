from Spiders.OPCNspider import OPCNspider as spider
import re
import os


if __name__ == "__main__":
    if not os.path.exists("./download"):
        os.mkdir("./download")

    
    a = spider(headless=True)

    while 1:
        url = input("Url (exit to exit):")

        if url == "exit":
            break

        if re.search(r"https://one-piece.cn/", url):
            a.get_url(url)
        else:
            print("Not a valid url (https://www.177mh.net/)")
            pass