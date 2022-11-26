import tweepy

BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAALmvfQEAAAAAmOqOxjkagp35nYD4oL7QpsXxWUg%3DY7ZsHb7K7Wyi1VZT7yf29wfSVfrpesCqXbtBsUC0jA8Z8ZhzXu'
client = tweepy.Client(BEARER_TOKEN)

def is_twitter_status(url):
    if "twitter.com/" in url and "/status/" in url:
        return True
    else:
        return False

# presumes that we have already checked url using is_twitter_status
def get_tweet_id_from_url(url):
    tweet_id = url.split('/status/')[1]

    return tweet_id

def get_source_scores(username):
    print('calling function on', username)
    sample_sources = [
        "axios", "bbc", "csmonitor", "Forbes", "MarketWatch", "NewsNation",
        "Newsweek", "RealClearNews", "Reuters", "TheHill", "WSJ"
    ]

    return sample_sources
