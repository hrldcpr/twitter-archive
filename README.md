To run:

    python3 store_user.py <username>

This will crawl up to 3,200 tweets from the user, and store them in:

    tweets/user/<username>/

The entire JSON of the tweets is stored, so you can do further processing later / no information is lost.

You can run the program again on a user and it will attempt to update the archive with any new tweets, as well as try to find older tweets if it hasn't crawled them all yet.
