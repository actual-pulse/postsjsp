import tweepy
from dotenv import load_dotenv
import os
import sys

load_dotenv()

def postTweet(text):
    try:
        client = tweepy.Client(
                consumer_key=os.environ["API_KEY"],
                consumer_secret=os.environ["API_SECRET"],
                access_token=os.environ["ACCESS_TOKEN"],
                access_token_secret=os.environ["ACCESS_TOKEN_SECRET"]
            )

        # Post tweet
        client.create_tweet(text=text)
        return True
    except tweepy.errors.Forbidden as e:
        print("❌ Forbidden error (likely duplicate content or permissions issue)")
        print(e)
        sys.exit(1)

    except tweepy.errors.TooManyRequests as e:
        print("⏳ Rate limit exceeded")
        print(e)
        sys.exit(1)

    except tweepy.errors.Unauthorized as e:
        print("🔑 Authentication error (check API keys)")
        print(e)
        sys.exit(1)

