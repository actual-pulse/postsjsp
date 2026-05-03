import os
import tweepy
import random
from datetime import date, datetime
import sys

today = date.today().isoformat()

# posts.py is inside /posts
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Go up ONE level to project root
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

last_run_path = os.path.join(PROJECT_ROOT, "parameters", "movie", "last_run.txt")
counter_path = os.path.join(PROJECT_ROOT, "parameters", "movie", "counter.txt")
media_path = os.path.join(PROJECT_ROOT, "images")

# Read last run date
with open(last_run_path, "r") as t:
    last_run = t.read().strip()

# Stop if already ran today
# if last_run == today:
#     print("Already ran today. Exiting.")
#     sys.exit(0)

# Read current day's counter
with open(counter_path, "r") as f:
    release_date_str = (
        f.read().strip()
    )  # Use int(f.read().strip()) to read only counter
    release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()
    today = date.today()
    days_left = (release_date - today).days


def get_random_image(folder=media_path):
    files = [
        f for f in os.listdir(folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]
    if not files:
        return None
    return os.path.join(folder, random.choice(files))


if days_left > 0:

    EMOJIS = ["🔥", "✨", "🎬", "🚀", "🎉", "⏳", "💥", "👍"]

    TEMPLATES = [
        # --------------------
        # Countdown (General)
        # --------------------
        "Only {days_left} days to witness the storm of Peddi {emoji}",
        "{days_left} days left for Peddi to roar on the big screen {emoji}",
        "The countdown tightens — just {days_left} days to Peddi {emoji}",
        "{days_left} days until Peddi takes over theatres {emoji}",
        "Mark the date. {days_left} days left for Peddi {emoji}",
        "The wait gets intense. {days_left} days remaining for Peddi {emoji}",
        "{days_left} days more for Peddi madness to begin {emoji}",
        "Not too far — {days_left} days to Peddi {emoji}",
        "{days_left} days until screens ignite with Peddi {emoji}",
        "The final stretch begins. {days_left} days to Peddi {emoji}",
        # --------------------
        # Mass Elevation Style
        # --------------------
        "{days_left} days for the rise of Peddi {emoji}",
        "Brace yourselves. Peddi arrives in {days_left} days {emoji}",
        "{days_left} days until the storm called Peddi hits {emoji}",
        "{days_left} days for the ultimate celebration — Peddi {emoji}",
        "{days_left} days until Peddi creates history {emoji}",
        # --------------------
        # Flexible (auto works for 0 or negative)
        # --------------------
        "In {days_left} days, Ram Charan unleashes a never-seen-before avatar 🔥",
        "{days_left} days to witness the raw mass transformation of Peddi 💥",
        "Rugged. Intense. Unstoppable. {days_left} days to Peddi ⚡",
        "{days_left} days until Ram Charan’s most powerful role hits the screen 🔥",
        "A storm is coming — {days_left} days to Peddi 🌪️",
        "{days_left} days until screens tremble with Peddi’s intensity 💣",
        "Mass elevation guaranteed — {days_left} days to go 🚀",
        "{days_left} days until Ram Charan redefines mass cinema 👊",
        "Brace yourself — Peddi mania begins in {days_left} days 🔥",
        "{days_left} days until every frame screams power and attitude ⚡",
        "Not just a film, it’s a phenomenon — {days_left} days to Peddi 🌟",
        "{days_left} days until the next big cinematic explosion 💥",
        "Rough. Raw. Real. {days_left} days to witness Peddi 🔥",
        "{days_left} days to experience Ram Charan like never before 👊",
        "The countdown to madness begins — {days_left} days to Peddi 🚨",
    ]

    HASHTAGS = ["#PEDDI 🔥"]

    SECOND_LINES = [
        "Excitement is building.",
        "The anticipation is real.",
        "Stay tuned.",
        "Something special is coming your way.",
        "The wait will be worth it.",
        "FDFS excitement is building up",
    ]

    emoji = random.choice(EMOJIS)
    hashtag = random.choice(HASHTAGS)
    template = random.choice(TEMPLATES)
    secondline = random.choice(SECOND_LINES)

    firstline = template.format(days_left=days_left, emoji=emoji)

    lines = [firstline, secondline, " ", "#RamCharan", hashtag]

    tweet_text = "\n".join(lines)

    print(tweet_text)

    # ---- Pick random image
    content = get_random_image(media_path)

    # Authenticate with X
    client = tweepy.Client(
        consumer_key=os.environ["API_KEY"],
        consumer_secret=os.environ["API_SECRET"],
        access_token=os.environ["ACCESS_TOKEN"],
        access_token_secret=os.environ["ACCESS_TOKEN_SECRET"],
    )

    # v1.1 auth for media upload
    auth = tweepy.OAuth1UserHandler(
        os.environ["API_KEY"],
        os.environ["API_SECRET"],
        os.environ["ACCESS_TOKEN"],
        os.environ["ACCESS_TOKEN_SECRET"],
    )
    api = tweepy.API(auth)

    media = api.media_upload(content)
    media_ids = [media.media_id]

    # # # Post tweet
    client.create_tweet(text=tweet_text, media_ids=media_ids)

    # Increment day
    # with open(counter_path, "w") as counter:
    #     counter.write(str(days_left - 1))

    # Update todays date in last run file
    with open(last_run_path, "w") as date:
        date.write(str(today))

    # TEMPLATES = [
    #     "Only {days_left} days to go {emoji}",
    #     "Countdown continues {days_left} days remaining {emoji}",
    #     "The wait is almost over. {days_left} days left {emoji}",
    #     "Mark the calendar. Just {days_left} days left {emoji}",
    #     "Getting closer! {days_left} days remaining {emoji}",

    #     "Just {days_left} days to go now {emoji}",
    #     "{days_left} days left and counting {emoji}",
    #     "The countdown is on, {days_left} days left {emoji}",
    #     "Not long to go. {days_left} days remaining {emoji}",
    #     "Time is ticking. {days_left} days left {emoji}",

    #     "{days_left} days until the moment arrives {emoji}",
    #     "Closer than ever {days_left} days to go {emoji}",
    #     "Almost there. {days_left} days remaining {emoji}",
    #     "The wait shortens. {days_left} days left {emoji}",
    #     "Anticipation builds with {days_left} days to go {emoji}",

    #     "{days_left} days more. The countdown continues {emoji}",
    #     "Every day gets you closer, just {days_left} days left {emoji}",
    #     "The final stretch begins. {days_left} days to go {emoji}",
    #     "All eyes on the date. {days_left} days left {emoji}",
    #     "The wait is counting down. {days_left} days remaining {emoji}"
    # ]
