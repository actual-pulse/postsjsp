from src.getContentAPI import getContentAPI
from src.postTweet import postTweet
from src.parameters import Parameters
import sys

params = Parameters()

check = params.isValid()
if not check:
    sys.exit(0)

result_text = getContentAPI()

result = postTweet(result_text)

if result:
    params.updateParameters()
else:
    sys.exit(0)