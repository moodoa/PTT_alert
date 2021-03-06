import os

from dags.ptt_trend_radar.feed.ptt_alert import PTT_alert

def get_articles(forum, minutes_ago, over_x_reaction):
    file_dir = os.path.dirname(__file__)
    message_path = os.path.join(file_dir, "used_article.txt")
    with open(message_path, "r", encoding="utf-8") as file:
        database = file.readlines()
    ptt_alert = PTT_alert(forum)
    all_articles = ptt_alert.hot_article_collector(minutes_ago, over_x_reaction)
    output = ""
    if all_articles:
        for article in all_articles:
            if (article["title"]+"\n") not in database:
                output+=article["title"]+"\n"
                output+=article["href"]
                database.append(article["title"]+"\n")
        with open(message_path, "w", encoding="utf-8") as file:
            file.writelines(database)
    return output

def article_sender(crawl_infos):
    articles = ""
    for crawl_info in crawl_infos:
        articles += (get_articles(crawl_info[0], crawl_info[1], crawl_info[2]))
    return articles

if __name__ == "__main__":
    print(article_sender([("NBA", -5, 16),("Gossiping", -10, 50)]))