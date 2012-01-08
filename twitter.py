import os
import os.path
import sys
import json
import time
import urllib.parse
import urllib.request

API_ROOT = 'http://api.twitter.com/1/'
API_USER = 'statuses/user_timeline'
API_SEARCH_QUERY = ''

def store_user_tweets(screen_name, include_rts=True, store_path='tweets/'):
    store_path += 'users/%s/' % screen_name
    os.makedirs(store_path, exist_ok=True)
    tweet_ids = (os.path.splitext(t) for t in os.listdir(store_path))
    tweet_ids = {int(t[0]) for t in tweet_ids if t[1] == '.json'}
    # should we look for new tweets since last time?
    update_tweets = True if tweet_ids else False

    url = API_ROOT + API_USER + '.json'
    query = {'screen_name': screen_name,
             'count': 200}
    if include_rts:
        query['include_rts'] = 't'

    for _ in range(20): # try at most 20 calls
        if update_tweets:
            query['since_id'] = max(tweet_ids)
        elif tweet_ids:
            query['max_id'] = min(tweet_ids) - 1
        print(url + '?' + urllib.parse.urlencode(query), file=sys.stderr)
        with urllib.request.urlopen(url + '?' + urllib.parse.urlencode(query)) as f:
            data = f.read().decode('utf-8')
        data = json.loads(data)
        print('  got %d tweets' % len(data), file=sys.stderr)

        if not data:
            if update_tweets: # no more recent tweets, try old tweets
                update_tweets = False
                del query['since_id']
            else: # no more old tweets, so we're done
                break

        for t in data:
            with open(store_path + '%d.json' % t['id'], 'w') as f:
                json.dump(t, f)
            tweet_ids.add(t['id'])
        print('%d total tweets' % len(tweet_ids), file=sys.stderr)

        time.sleep(24) # twitter rate-limit is 150 calls per hour i.e. 1 call per 24 seconds
