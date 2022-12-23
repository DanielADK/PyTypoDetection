import string
import re
def process(text: string) -> string:
    text = text.lower()
    pattern = "[^ěščřžýáíéóúůďťňa-z\-]"
    text = re.sub(pattern, '', text)
    return text
