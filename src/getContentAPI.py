import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def getContentAPI():
    client = OpenAI()

    PROMPT = """
    Write a short, factual, neutral update about JanaSena Party in under 250 characters.

    If a recent constructive activity is widely known, mention it briefly.
    Otherwise, describe a well-known positive contribution or principle
    demonstrated by the party over the past few years.

    Use relevant emojis. Avoid exaggeration.

    You MUST return one short paragraph of text.
    If no recent verified news exists, you MUST return a historical
    positive contribution instead. Do not return empty output.
    """

    key = os.getenv("OPENAI_API_KEY")
    # print("Key loaded:", bool(key))
    # print("Key prefix:", key[:7] if key else None)

    response = client.responses.create(
        model="gpt-5.2",
        # tools=[{"type": "web_search"}],
        input=PROMPT,
        max_output_tokens=120
    )

    out = [response.output_text, " ", "#JanaSenaParty #PawanKalyan"]

    out_text = "\n".join(out)

    print(out_text)

    return out_text


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


# print(extract_text(response))