import os
import os.path
import urllib.parse
import twitter

storage_path = 'tweets/'

if os.path.exists(storage_path):
    users_path = storage_path + 'users/'
    if os.path.exists(users_path):
        for user in os.listdir(users_path):
            if not user.startswith('.'):
                twitter.store_user_tweets(user)

    searches_path = storage_path + 'searches/'
    if os.path.exists(searches_path):
        for search in os.listdir(searches_path):
            if not search.startswith('.'):
                twitter.store_search_tweets(urllib.parse.unquote_plus(search))
