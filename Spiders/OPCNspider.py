from spider import spider

class OPCNspider(spider):
    def start_browser(self):
        print("OPCN v 0.1")
        self.boot_up_browser()

    def get_img(self):
        imgs = self.browser.find_element_by_css_selector("div.container").find_elements_by_tag_name("img")

        urls = [None] * len(imgs)
        filenames = urls[:]

        for i in range(len(imgs)):
            urls[i] = imgs[i].get_attribute("src")
            filenames[i] = "{0:03}.jpg".format(i+1)

        return urls, filenames

if __name__ == "__main__":
    b = OPCNspider(headless=False, dtLoadPicture=False)
    url = "https://one-piece.cn/post/10970/"
    b.get_url(url)
    pass