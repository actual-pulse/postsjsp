import re
from datetime import date
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HASHTAGS = "#JanaSenaParty #PawanKalyan"
BIRTHDAY_HASHTAG = "#HBDPawanKalyan"
MAX_TOTAL_CHARS = 260
BODY_JOIN_OVERHEAD = len("\n \n")  # separators between body, spacer, hashtags

BIRTHDAY_MONTH = 9
BIRTHDAY_DAY = 2

# Suggested starting angles for the monthly "works done" tweets
# (1..total-1), used only to nudge topic variety across the 4 messages.
# The model is told to override these with whatever real developments
# actually happened, since a party's work is not limited to these areas.
# The final tweet in the series is always an appreciation message.
WORK_FOCUS_AREAS = [
    "infrastructure and roads",
    "welfare and social schemes",
    "youth, education and employment",
    "agriculture and farmer welfare",
]


def _max_body_chars(hashtags):
    return MAX_TOTAL_CHARS - len(hashtags) - BODY_JOIN_OVERHEAD


def _clean_body(text, max_body_chars):
    body = text
    body = body.replace("—", ",").replace("–", ",")
    body = re.sub(r"\(\s*\[[^\]]*\]\([^)]*\)\s*\)", "", body)  # (citation) wrapper
    body = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", body)  # remaining markdown links -> label text
    body = re.sub(r"https?://\S+", "", body)  # bare urls
    body = re.sub(r"#\w+", "", body).strip()
    body = re.sub(r"[ \t]{2,}", " ", body).strip()

    if len(body) > max_body_chars:
        ellipsis = "..."
        trimmed = body[:max_body_chars - len(ellipsis)].rsplit(" ", 1)[0]
        body = trimmed.rstrip(",.!") + ellipsis

    return body


def _call_model(prompt):
    client = OpenAI()

    response = client.responses.create(
        model="gpt-5.2",
        tools=[{"type": "web_search"}],
        input=prompt,
        max_output_tokens=500
    )

    return response.output_text


def _build_tweet(body, hashtags):
    out_text = "\n".join([body, " ", hashtags])
    print(out_text)
    return out_text


def _is_birthday(today=None):
    today = today or date.today()
    return today.month == BIRTHDAY_MONTH and today.day == BIRTHDAY_DAY


def getContentAPI():
    if _is_birthday():
        return getBirthdayContentAPI()

    max_body_chars = _max_body_chars(HASHTAGS)

    PROMPT = f"""
    Search for the latest verified work, initiatives, or announcements by
    Pawan Kalyan in his role as Deputy Chief Minister of Andhra Pradesh,
    and/or recent constructive activities of the JanaSena Party.

    Write a short, factual, positive update about this in under
    {max_body_chars} characters.

    If a recent development is widely known, mention it briefly and
    specifically (what was done, and its benefit to people). Otherwise,
    describe a well-known positive contribution or principle demonstrated
    by Pawan Kalyan or JanaSena Party as Deputy CM.

    Include the ✊ emoji somewhere in the message to represent strength and
    the party's growing position. Also choose 1 additional emoji that
    specifically matches the content of THIS message (e.g. education,
    roads, welfare, youth, agriculture, governance) rather than reusing
    the same generic emoji every time.

    Do NOT include any hashtags in your response, they will be added
    separately.

    Do NOT include any URLs, links, citations, or source references in
    your response. Plain text and emojis only.

    Do NOT use the em dash character (—) or en dash character (–)
    anywhere in your response. Use a comma or period instead.

    You MUST return one short paragraph of text only, with no hashtags.
    If no recent verified news exists, you MUST return a well-known
    positive contribution instead. Do not return empty output.
    """

    body = _clean_body(_call_model(PROMPT), max_body_chars)
    return _build_tweet(body, HASHTAGS)


def getBirthdayContentAPI():
    """Special-cased content for September 2nd, Pawan Kalyan's birthday."""
    hashtags = f"{HASHTAGS} {BIRTHDAY_HASHTAG}"
    max_body_chars = _max_body_chars(hashtags)

    PROMPT = f"""
    Today, September 2nd, is the birthday of Pawan Kalyan, Deputy Chief
    Minister of Andhra Pradesh and leader of the JanaSena Party.

    Write a short, warm birthday wish for Pawan Kalyan in under
    {max_body_chars} characters, celebrating his leadership and service
    to Andhra Pradesh as Deputy CM.

    Include the ✊ emoji to represent strength and the party's growing
    position, plus 1 celebratory emoji (e.g. 🎉🎂🙏) that fits a birthday
    wish.

    Do NOT include any hashtags in your response, they will be added
    separately.

    Do NOT include any URLs, links, citations, or source references in
    your response. Plain text and emojis only.

    Do NOT use the em dash character (—) or en dash character (–)
    anywhere in your response. Use a comma or period instead.

    You MUST return one short paragraph of text only, with no hashtags.
    Do not return empty output.
    """

    body = _clean_body(_call_model(PROMPT), max_body_chars)
    return _build_tweet(body, hashtags)


def getMonthlyWorksAPI(tweet_number, total=5):
    """
    Content for the monthly "works done in the last 30 days" series posted
    on the 10th of every month. tweet_number is 1-indexed; the final
    tweet in the series (tweet_number == total) is an appreciation
    message instead of a specific work update.
    """
    if tweet_number < 1 or tweet_number > total:
        raise ValueError(f"tweet_number must be between 1 and {total}")

    max_body_chars = _max_body_chars(HASHTAGS)

    if tweet_number == total:
        PROMPT = f"""
        Write a short, warm appreciation message thanking and appreciating
        the work done by the JanaSena Party and Deputy CM Pawan Kalyan
        over the past 30 days, in under {max_body_chars} characters.

        Keep it general and appreciative in tone rather than listing a
        specific event.

        Include the ✊ emoji to represent strength and the party's
        growing position, plus 1 additional emoji that fits an
        appreciation or thank-you message.

        Do NOT include any hashtags, URLs, links, or citations in your
        response. Plain text and emojis only.

        Do NOT use the em dash character (—) or en dash character (–)
        anywhere in your response. Use a comma or period instead.

        You MUST return one short paragraph of text only, with no
        hashtags. Do not return empty output.
        """
    else:
        suggested_focus = WORK_FOCUS_AREAS[(tweet_number - 1) % len(WORK_FOCUS_AREAS)]

        PROMPT = f"""
        Search for verified work, initiatives, or announcements by Pawan
        Kalyan as Deputy Chief Minister of Andhra Pradesh, and/or the
        JanaSena Party, from the last 30 days.

        This is message {tweet_number} of {total} in a monthly summary
        series covering different areas of work. As a starting point,
        consider {suggested_focus}, but JanaSena's work is not limited to
        this area. If a different area (e.g. governance, health,
        women's welfare, industries and jobs, disaster relief, urban
        development, law and order, or anything else) had a more
        significant or more recent real development in the last 30 days,
        cover that instead. Prioritize real, verifiable developments over
        sticking to the suggested topic.

        Write a short, factual, positive update about whichever specific
        development you choose, in under {max_body_chars} characters,
        mentioning what was done and its benefit to people. Avoid generic
        statements that could apply to any topic.

        Include the ✊ emoji to represent strength and the party's
        growing position, plus 1 additional emoji that specifically
        matches the topic of THIS message.

        Do NOT include any hashtags, URLs, links, or citations in your
        response. Plain text and emojis only.

        Do NOT use the em dash character (—) or en dash character (–)
        anywhere in your response. Use a comma or period instead.

        If no recent verified news exists, you MUST return a well-known
        positive contribution instead. Do not return empty output.

        You MUST return one short paragraph of text only, with no
        hashtags.
        """

    body = _clean_body(_call_model(PROMPT), max_body_chars)
    return _build_tweet(body, HASHTAGS)


def extract_text(response):
    texts = []

    for item in response.output:
        # Some items (like web_search) don't have content
        if not hasattr(item, "content"):
            continue

        for c in item.content:
            if c.type == "output_text":
                texts.append(c.text)

    return "\n".join(texts).strip()
