import os
import sys
from src.getContentAPI import getMonthlyWorksAPI
from src.postTweet import postTweet

TOTAL_MONTHLY_TWEETS = 5

tweet_number = int(os.getenv("TWEET_NUMBER", "1"))

result_text = getMonthlyWorksAPI(tweet_number, total=TOTAL_MONTHLY_TWEETS)

result = postTweet(result_text)

if not result:
    sys.exit(0)
