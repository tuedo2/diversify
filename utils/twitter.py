import tweepy
import pickle

# YOU MAY RUN INTO A RATE LIMIT TESTING THESE FUNCTIONS OUT!
# If you think the error is a rate limit, wait 15 minutes and try again.
# If the error persists, it's not because of the rate limit :P

BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAALmvfQEAAAAAmOqOxjkagp35nYD4oL7QpsXxWUg%3DY7ZsHb7K7Wyi1VZT7yf29wfSVfrpesCqXbtBsUC0jA8Z8ZhzXu'
client = tweepy.Client(BEARER_TOKEN)

sources = ['axios', 'bbc', 'csmonitor', 'Forbes', 'MarketWatch', 'NewsNation', 'Newsweek',
           'RealClearNews', 'Reuters', 'TheHill', 'WSJ']
source_ids = (19701628, 14857525, 91478624, 624413, 1217198127591186437,
              800707492346925056, 2884771, 1652541, 20094138, 1917731, 3108351)

sets_dict = dict()
for source in sources:
    edge_path = 'network/' + source + '.pickle'
    f = open(edge_path, 'rb')
    edge_set = pickle.load(f)
    sets_dict[source] = edge_set

def is_twitter_status(url):
    if "twitter.com/" in url and "/status/" in url:
        return True
    else:
        return False

# presumes that we have already checked url using is_twitter_status
def get_tweet_id_from_url(url):
    tweet_id = url.split('/status/')[1]

    return tweet_id

def get_text_from_tweet_id(tweet_id):
    res = client.get_tweet(id=tweet_id)

    return res.data.text

def get_following(user_id, next_token=None):
    try:
        res = client.get_users_following(user_id, max_results=1000, pagination_token=next_token)
        return res
    except tweepy.errors.TooManyRequests:
        print('sleep 15 minutes')
        time.sleep(15*60+1)
        return get_following(user_id, next_token)
    except tweepy.errors.TwitterServerError:
        print('Twitter Server Error')
        time.sleep(60)
        return get_following(user_id, next_token)

def get_full_following(username, max_iter = 10):
    user_id = client.get_user(id=None,username=username).data.id

    res = get_following(user_id)
    following_set = set([user.id for user in res.data])

    next_token = None

    meta = res.meta
    counter = 0

    while 'next_token' in meta and counter < max_iter:
        next_token = meta['next_token']

        res = get_following(user_id, next_token)
        following_set.update([user.id for user in res.data])

        meta = res.meta
        counter += 1

    return following_set

def get_intersections(username):
    intersection_dict = dict()

    following_set = get_full_following(username)

    for key in sets_dict:
        intersection_dict[key] = len(following_set.intersection(sets_dict[key]))

    return intersection_dict

def get_source_list(username):
    intersection_dict = get_intersections(username)

    source_list = []

    for key in intersection_dict:
        if intersection_dict[key] == 0:
            source_list.append(key)

    return source_list

def search_with_keywords(keywords):
    q_str = '('
    for i in range(len(keywords) - 1):
        q_str += keywords[i] + ' '
    q_str += keywords[-1] + ')'
    q_str += ' has:links is:verified lang:en -is:retweet'

    res = client.search_recent_tweets(q_str)

    return res.data
