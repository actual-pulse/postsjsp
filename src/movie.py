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
if last_run == today:
    print("Already ran today. Exiting.")
    sys.exit(0)

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
        "Not long now — {days_left} days to Peddi {emoji}",
        "{days_left} days until screens ignite with Peddi {emoji}",
        "The final stretch begins. {days_left} days to Peddi {emoji}",
        # --------------------
        # Mass Elevation Style
        # --------------------
        "{days_left} days for the rise of Peddi {emoji}",
        "Power. Fire. Peddi. {days_left} days left {emoji}",
        "{days_left} days until Peddi shakes the box office {emoji}",
        "Brace yourselves. Peddi arrives in {days_left} days {emoji}",
        "{days_left} days until the storm called Peddi hits {emoji}",
        "The roar begins in {days_left} days — Peddi {emoji}",
        "{days_left} days for the ultimate celebration — Peddi {emoji}",
        "{days_left} days until Peddi creates history {emoji}",
        "Get ready. Peddi lands in {days_left} days {emoji}",
        "The fire begins in {days_left} days — Peddi {emoji}",
        # --------------------
        # Short Punchy
        # --------------------
        "{days_left} days to Peddi {emoji}",
        "Peddi in {days_left} days {emoji}",
        "{days_left} days left. Peddi loading {emoji}",
        "Peddi countdown: {days_left} {emoji}",
        "{days_left} days. That’s it. Peddi {emoji}",
        "Just {days_left} days more — Peddi {emoji}",
        "{days_left} days remaining. Peddi {emoji}",
        # --------------------
        # Flexible (auto works for 0 or negative)
        # --------------------
        "Peddi arrives in {days_left} days {emoji}",
        "The moment is almost here — {days_left} days to Peddi {emoji}",
        "Every second counts. {days_left} days to Peddi {emoji}",
        "{days_left} days until Ram Charan unleashes pure intensity on screen {emoji}",
        "In {days_left} days, witness Ram Charan’s firepower in full force {emoji}",
        "{days_left} days left to experience Ram Charan’s powerful screen presence {emoji}",
        "The intensity rises — just {days_left} days for Ram Charan {emoji}",
        "{days_left} days until Ram Charan dominates every frame {emoji}",
        "Eyes that speak. Presence that roars. {days_left} days to Ram Charan {emoji}",
        "{days_left} days until Ram Charan sets the screen ablaze {emoji}",
        "{days_left} days until Ram Charan sets the floor on fire {emoji}",
        "In {days_left} days, get ready for Ram Charan’s explosive dance moves {emoji}",
        "{days_left} days to witness next-level moves from Ram Charan {emoji}",
        "Grace. Power. Rhythm. {days_left} days to Ram Charan {emoji}",
        "{days_left} days left for dance steps that will trend worldwide {emoji}",
        "When Ram Charan moves, the world watches — {days_left} days to go {emoji}",
        "{days_left} days until the internet replays every step {emoji}",
        "{days_left} days until another chartbuster takes over {emoji}",
        "In {days_left} days, expect songs that shake the internet {emoji}",
        "{days_left} days left for music that trends everywhere {emoji}",
        "Blockbuster vibes loading — {days_left} days to go {emoji}",
        "{days_left} days until the next viral update drops {emoji}",
        "From theatres to cinema lovers — {days_left} days for magic {emoji}",
        "{days_left} days until songs dominate every playlist {emoji}",
        # --------------------
        # Release-day friendly (still safe with days_left=0)
        # --------------------
        # "The wait ends today. Peddi is here {emoji}",
        # "It’s time. Peddi hits the big screen today {emoji}",
        # "Today we celebrate Peddi {emoji}",
        # "Peddi is now in theatres {emoji}",
        # --------------------
        # Post-release friendly
        # --------------------
        # "Peddi is now roaring in theatres {emoji}",
        # "Have you watched Peddi yet? {emoji}",
        # "The storm has started — Peddi {emoji}",
        # "Experience Peddi on the big screen {emoji}",
        # "Peddi mania begins now {emoji}",
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
