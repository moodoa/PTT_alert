# PTT alert
爬取限定時間內 PTT 上的熱門文章(推、噓皆算)，並透過 airflow 自動化傳送訊息至 LINE/Slack。


![alt text](https://cdn-images-1.medium.com/max/1000/1*a4MkwodUgFf-wXzIEAtoGw.png)

## ptt_alert.py
* 以 `PTT 論壇名稱`、`限定時間(分鐘)` 為參數爬取限定時間內 PTT 特定論壇的熱門文章。
* 回傳值為內含 dic 的 list，key 分別是 `reaction (爆/噓)`、`title 文章標題`、`href 文章連結`、`author 作者`、`rising_speed 推文上升速度`、`post_time 發文時間`。

## Requirements
python 3

## Usage
* 以爬取 `NBA` 板 `5` 分鐘以內到達 `16` 推以及`Gossiping` 板 `10` 分鐘以內到達 `50` 推的文章為例。
```
initialize.py

if __name__ == "__main__":
    print(article_sender([("NBA", -5, 16),("Gossiping", -10, 50)]))

```
## Installation
`pip install -r requriements.txt`。
若要使用 `airflow` 則需要額外安裝相關套件。

