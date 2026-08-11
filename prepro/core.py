def romaji2katakana(text: str) -> str:
    import re
    from e2k import C2K
    def to_katakana(match):
        c2k = C2K()
        return c2k(match.group().lower())
    return re.sub(r'[a-zA-Z]+', to_katakana, text)


def normalize_silence_sign(text: str) -> str:
    silence_sign = "、"
    text = text.replace("…", silence_sign)
    text = text.replace(".", silence_sign)
    text = text.replace(",", silence_sign)


#Example:
#```
#text = "今日も…君はcoolだね！"
#print(Prepro_text(text))
#```
#Outputs:
#```
#今日も、君はクールだね！
#```
def Prepro_text(text: str) -> str:
    text = romaji2katakana(text)
    return text
