
import requests
from kafka import KafkaProducer
import json
import feedparser

print("hello")


def get_response_from_feedparser(url):
    feed = feedparser.parse(url)

    posts = feed.entries
    # print(posts)
    post_list = []

    for post in posts:
        # print(post)
        temp = {}

        try:
            temp["title"] = post.title
            temp["link"] = post.link
            temp["description"] = post.description
            temp["pubdate"] = post.published
        except:
            print("Exception")
        print(temp)
        post_list.append(temp)

    return post_list

        


producer = KafkaProducer(bootstrap_servers=['localhost:29092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
print("Connected to Kafka!!")


times_rss = {"Top-Stories": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms", 
        "India": "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
        "World" :"https://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
        "Business": "https://timesofindia.indiatimes.com/rssfeeds/1898055.cms",
        "Cricket": "https://timesofindia.indiatimes.com/rssfeeds/54829575.cms",
        "Sports": "https://timesofindia.indiatimes.com/rssfeeds/4719148.cms",
        "Science": "https://timesofindia.indiatimes.com/rssfeeds/-2128672765.cms",
        "Environment": "https://timesofindia.indiatimes.com/rssfeeds/2647163.cms",
        "Tech": "https://timesofindia.indiatimes.com/rssfeeds/66949542.cms",
        "Education": "https://timesofindia.indiatimes.com/rssfeeds/913168846.cms",
        "Entertainment": "https://timesofindia.indiatimes.com/rssfeeds/1081479906.cms",
        "Life_style": "https://timesofindia.indiatimes.com/rssfeeds/2886704.cms"}

hindu_rss = {"Business": "https://www.thehindu.com/business/feeder/default.rss",
            "Agriculture": "https://www.thehindu.com/business/agri-business/feeder/default.rss",
            "Economy": "https://www.thehindu.com/business/Economy/feeder/default.rss",
            "Sports": "https://www.thehindu.com/sport/feeder/default.rss",
            "Cricket": "https://www.thehindu.com/sport/cricket/feeder/default.rss",
            "Football": "https://www.thehindu.com/sport/football/feeder/default.rss",
            "Hockey": "https://www.thehindu.com/sport/hockey/feeder/default.rss",
            "Tennis": "https://www.thehindu.com/sport/tennis/feeder/default.rss",
            "Atheletics": "https://www.thehindu.com/sport/athletics/feeder/default.rss",
            "Races": "https://www.thehindu.com/sport/races/feeder/default.rss",
            "Entertainment": "https://www.thehindu.com/entertainment/feeder/default.rss",
            "Movies": "https://www.thehindu.com/entertainment/movies/feeder/default.rss",
            "Life_style": "https://www.thehindu.com/life-and-style/feeder/default.rss",
            "Fashion": "https://www.thehindu.com/life-and-style/fashion/feeder/default.rss",
            "Travel": "https://www.thehindu.com/life-and-style/travel/feeder/default.rss"
            }

for topic, url in times_rss.items():
    article_dict = get_response_from_feedparser(url)
    
    for article in article_dict:
        article["topic"] = topic
        article["source"] = "Times"
        print(article)

for topic, url in hindu_rss.items():
    article_dict = get_response_from_feedparser(url)
    
    for article in article_dict:
        article["topic"] = topic
        article["source"] = "Hindu"
        print(article)
        producer.send(topic='news', value=article)

