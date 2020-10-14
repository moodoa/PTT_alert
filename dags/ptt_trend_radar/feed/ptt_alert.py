import os
import re
import time
import requests

from random import randint
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class PTT_alert():
    def __init__(self, forum):
        self.base_url = f"https://www.ptt.cc/bbs/{forum}/index.html"
        session = requests.Session()
        payload ={
            "from":f"/bbs/Gossiping/index.html",
            "yes":"yes"
        }
        post_over18 = session.post(f"https://www.ptt.cc/ask/over18?from=%2Fbbs%2FGossiping%2Findex.html",payload)
        self.session = session
        self.forum = forum

    def all_articles_collector(self, minutes_ago):
        url = self.base_url
        all_articles = []
        time_exceed = False
        for article_info in self.single_page_articles_collector(url):
            if self.is_in_recent(article_info["post_time"], minutes_ago) == True:
                all_articles.append(article_info)
        while time_exceed == False:
            req = self.session.get(url)
            soup = BeautifulSoup(req.text,"html.parser")
            btn = soup.select('div.btn-group > a')
            if btn:
                up_page_href = btn[3]['href']
                next_page_url = 'https://www.ptt.cc' + up_page_href
                url = next_page_url
                for article_info in self.single_page_articles_collector(url):
                    if self.is_in_recent(article_info["post_time"], minutes_ago) == True:
                        all_articles.append(article_info)
                    else:
                        time_exceed = True
            else:
                time_exceed = True
        return all_articles

    def single_page_articles_collector(self, url):
        page_articles_info = []
        txt = self.session.get(url).text
        if '<div class="r-list-sep">' in txt:
            txt = txt.split('<div class="r-list-sep">')[0]
        soup = BeautifulSoup(txt, "html.parser")
        results = soup.select("div.r-ent")
        for item in results:
            article_info = {}
            a_item = item.select_one("a")
            if a_item:
                title = item.select_one("a").text
                author = item.select_one("div.author").text
                reaction = self.get_reaction(item.select_one("div.nrec").text)
                href = "https://www.ptt.cc"+ a_item.get("href")
                article_info["reaction"] = reaction
                article_info["title"] = title
                article_info["href"] = href
                article_info["author"] = author
                article_info["post_time"] = self.get_article_time(href)
                article_info["rising_speed"] = self.get_rising_speed(article_info["post_time"], article_info["reaction"])
                page_articles_info.append(article_info)
        return page_articles_info
    
    def get_reaction(self, reaction_on_ptt):
        if reaction_on_ptt == "":
            return 0
        elif reaction_on_ptt == "爆":
            reaction_on_ptt = 100
        elif reaction_on_ptt == "XX":
            reaction_on_ptt = -100
        elif reaction_on_ptt[0] == "X":
            reaction_on_ptt = int(reaction_on_ptt[1])*-10
        else:
            reaction_on_ptt = int(reaction_on_ptt)
        return reaction_on_ptt

    def get_article_time(self, article_url):
        pattern = f"https://www.ptt.cc/bbs/{self.forum}/M.(\d+).+"
        epoch_time = re.findall(pattern, article_url)
        if epoch_time:
            post_time = datetime.fromtimestamp(int(epoch_time[0]))
            return post_time
        else:
            return datetime.now()+timedelta(days=-7)
    
    def get_rising_speed(self, post_time, reaction):
        now = datetime.now()
        through_time = (now - post_time).total_seconds()/60
        if reaction:
            rising_speed = str(reaction/through_time)[:4]
            return rising_speed
        else:
            return "0"

    def is_in_recent(self, post_time, minutes_ago):
        last_check_point = datetime.now() + timedelta(minutes = minutes_ago)
        return post_time >= last_check_point

    def hot_article_collector(self, minutes_ago, over_x_reaction):
        hot_articles = []
        all_articles = self.all_articles_collector(minutes_ago)
        for article in all_articles:
            if self.is_hot_article(article["reaction"], over_x_reaction):
                if article["title"] and self.remove_category(article["title"]):
                    hot_articles.append(article)
        return hot_articles
    
    def remove_category(self, title):
        unwanted_category = ["[公告]", "[問卦]"]
        pattern = r".*(\[.+\]).+"
        if re.findall(pattern, title)[0] in unwanted_category:
            return False
        return True

    def is_hot_article(self, reaction, over_x_reaction):
        if reaction >= over_x_reaction or reaction <= (over_x_reaction*-1):
            return True
        return False
        