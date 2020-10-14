# PTT alert
爬取限定時間內 PTT 上的熱門文章。(推、噓皆算)


![alt text](https://img.ltn.com.tw/Upload/liveNews/BigPic/600_php7CYMfK.jpg)

## ptt_alert.py
* 以 `PTT 論壇名稱`、`限定時間(分鐘)` 為參數爬取限定時間內 PTT 特定論壇的熱門文章。
* 回傳值為內含 dic 的 list，key 分別是 `reaction (爆/噓)`、`title 文章標題`、`href 文章連結`、`author 作者`、`rising_speed 推文上升速度`、`post_time 發文時間`。

## Requirements
python 3

## Usage
* 以爬取 `NBA` 板 `5` 分鐘以內到達 `16` 推以及`Gossiping` 板 `10` 分鐘以內到達 `50` 推的文章為例。
```
initialize.py

def article_sender():
    last_5_min_articles = (get_articles("NBA", -5, 16))
    last_10_min_articles = (get_articles("Gossiping", -10, 50))
    return last_5_min_articles+"\n"+last_10_min_articles

if __name__ == "__main__":
    print(article_sender())

```
## Installation
`pip install -r requriements.txt`。
若要使用 `airflow` 則需要額外安裝相關套件。

