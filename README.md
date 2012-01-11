To run:

    python3 store_user.py <username>
    python3 store_seach.py "<query>"

This will crawl up to 3,200 tweets from the user, or about a week of tweets from the search, and store each one as a JSON file in:

    tweets/users/<username>/
    tweets/searches/<query>/

You can re-run the program at any time and it will attempt to update the archive with any new tweets, as well as try to find older tweets if it hasn't crawled them all yet.

You can also update all users and searches by simply running:

    python3 update.py
