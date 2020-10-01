import time
import requests

from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup


class PTT_alert():
    def __init__(self, forum, minutes):
        self.base_url = f"https://www.ptt.cc/bbs/{forum}/index.html"
        session = requests.Session()
        payload ={
            "from":f"/bbs/Gossiping/index.html",
            "yes":"yes"
        }
        post_over18 = session.post(f"https://www.ptt.cc/ask/over18?from=%2Fbbs%2FGossiping%2Findex.html",payload)
        self.session = session
        self.minutes = minutes
        
    def all_articles_collector(self):
        url = self.base_url
        all_articles = []
        time_exceed = False
        for article_info in self.single_page_articles_collector(url):
            all_articles.append(article_info)
        while time_exceed == False:
            req = self.session.get(url)
            soup = BeautifulSoup(req.text,"html.parser")
            btn = soup.select('div.btn-group > a')
            up_page_href = btn[3]['href']
            next_page_url = 'https://www.ptt.cc' + up_page_href
            url = next_page_url
            for article_info in self.single_page_articles_collector(url):
                all_articles.append(article_info)
                try:
                    if self.is_in_recent(article_info["post_time"], self.minutes) == False:
                        time_exceed = True
                except:
                    pass
        return all_articles

    def single_page_articles_collector(self, url):
        page_articles_info = []
        req = self.session.get(url)
        soup = BeautifulSoup(req.text, "html.parser")
        results = soup.select("div.r-ent")
        for item in results:
            article_info = {}
            a_item = item.select_one("a")
            if a_item:
                title = item.select_one("a").text
                reaction = item.select_one("div.nrec").text
                href = "https://www.ptt.cc"+ a_item.get("href")
                article_info["reaction"] = reaction
                article_info["title"] = title
                article_info["href"] = href
                article_info["post_time"] = self.get_article_time(href)
                page_articles_info.append(article_info)
        return page_articles_info

    def get_article_time(self, article_url):
        content = self.session.get(article_url).content
        soup = BeautifulSoup(content, "html.parser")
        if soup.select("span.article-meta-value"):
            post_time_str = soup.select("span.article-meta-value")[-1].text
            post_time = datetime.strptime(post_time_str, "%a %b %d %H:%M:%S %Y")
            return post_time
        else:
            pass

    def is_in_recent(self, post_time, minutes_ago):
        last_check_point = datetime.now() + timedelta(minutes = minutes_ago)
        return post_time >= last_check_point

    def hot_article_collector(self):
        hot_articles = []
        all_articles = self.all_articles_collector()
        for article in all_articles:
            if self.is_hot_article(article["reaction"]):
                hot_articles.append(article)
        return hot_articles

    def is_hot_article(self, reaction):
        if reaction == "爆" or reaction == "XX":
            return True
        return False
        
if __name__ == "__main__":
    ptt_alert = PTT_alert("NBA", -60)
    print(ptt_alert.hot_article_collector())