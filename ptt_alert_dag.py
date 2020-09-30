from ptt_alert import PTT_alert

def article_sender():
    ptt_alert = PTT_alert("NBA", -60)
    all_articles = ptt_alert.hot_article_collector()
    for article in all_articles:
        print(article["reaction"])
        print(article["title"])
        print(article["href"])
        print(article["post_time"])
        print("-"*50)
article_sender()