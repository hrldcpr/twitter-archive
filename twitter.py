import os
import os.path
import sys
import json
import time
import urllib.parse
import urllib.request
import urllib.error

API_USER = 'http://api.twitter.com/1/statuses/user_timeline.json'
API_SEARCH = 'http://search.twitter.com/search.json'

DELAY = 24 # twitter rate-limit is 150 calls per hour i.e. 1 call per 24 seconds

def store_user_tweets(screen_name, include_rts=True, storage_path='tweets/'):
    storage_path += 'users/%s/' % screen_name
    os.makedirs(storage_path, exist_ok=True)
    tweet_ids = (os.path.splitext(t) for t in os.listdir(storage_path))
    tweet_ids = {int(t[0]) for t in tweet_ids if t[1] == '.json'}
    # should we look for new tweets since last time?
    updating = True if tweet_ids else False

    query = {'screen_name': screen_name,
             'count': 200}
    if include_rts:
        query['include_rts'] = 't'

    while True:
        if updating:
            query['since_id'] = max(tweet_ids)
        elif tweet_ids:
            query['max_id'] = min(tweet_ids) - 1

        tweets = _get_data(API_USER + '?' + urllib.parse.urlencode(query))
        _log('  got %d tweets' % len(tweets))

        if tweets:
            _store_tweets(storage_path, tweets)
            tweet_ids.update(t['id'] for t in tweets)
            _log('%d total tweets' % len(tweet_ids))
        else:
            if updating: # no more recent tweets, try old tweets
                updating = False
                del query['since_id']
            else: # no more old tweets, so we're done
                break

def store_search_tweets(q, storage_path='tweets/'):
    storage_path += 'searches/%s/' % q
    os.makedirs(storage_path, exist_ok=True)

    query = {'q': q, 'result_type': 'recent', 'rpp': 100, 'page': 0}

    while True:
        query['page'] += 1
        data = _get_data(API_SEARCH + '?' + urllib.parse.urlencode(query), delay=DELAY / 2)
        tweets = data['results']
        _log('  got %d tweets' % len(tweets))
        if tweets:
            _store_tweets(storage_path, tweets)
        else:
            break


def _log(s):
    print(s, file=sys.stderr)

def _get_data(url, delay=DELAY):
    _log(url)
    while True:
        _log('  ...')
        time.sleep(delay)
        try:
            with urllib.request.urlopen(url) as f:
                data = f.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            if e.code != 502: # ignore 502, which Twitter throws quite often
                raise e
        else:
            break
    return json.loads(data)

def _store_tweets(storage_path, tweets):
    for t in tweets:
        with open(storage_path + '%d.json' % t['id'], 'w') as f:
            json.dump(t, f)
