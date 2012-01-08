To run:

    python3 store_user.py <username>

This will crawl up to 3,200 tweets from the user, and store each one as a JSON file in:

    tweets/user/<username>/

You can re-run the program at any time and it will attempt to update the archive with any new tweets, as well as try to find older tweets if it hasn't crawled them all yet.
