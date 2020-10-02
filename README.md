# PTT alert
爬取限定時間內 PTT 上的熱門文章。(推、噓皆算)


![alt text](https://img.ltn.com.tw/Upload/liveNews/BigPic/600_php7CYMfK.jpg)

## ptt_alert.py
* 以 `PTT 論壇名稱`、`限定時間(分鐘)` 為參數爬取限定時間內 PTT 特定論壇的熱門文章。
* 回傳值為內含 dic 的 list，key 分別是 `reaction (爆/噓)`、`title 文章標題`、`href 文章連結`、`post_time 發文時間`。

## Requirements
python 3

## Usage
* 以爬取 `NBA` 板 `60` 分鐘以內的爆文為例。
```
if __name__ == "__main__":
    ptt_alert = PTT_alert("NBA", -60)
    print(ptt_alert.hot_article_collector())
```
## Installation
`pip install -r requriements.txt`

