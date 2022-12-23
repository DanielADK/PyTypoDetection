import string
import re
def process(text: string) -> string:
    pattern = "[^ěščřžýáíéóúůďťňĎŇŤŠČŘŽÝÁÍÉÚŮĚÓA-Za-z]"
    text = text.lower()
    text = re.sub(pattern, '', text)
    return text
