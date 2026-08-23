import unicodedata, re, num2words

def romaji2katakana(text: str) -> str:
    import re
    from e2k import C2K
    def to_katakana(match):
        c2k = C2K()
        return c2k(match.group().lower())
    return re.sub(r'[a-zA-Z]{2,}', to_katakana, text)

def convert2kansuuji(num_str: str) -> str:
    trans = str.maketrans('0123456789', '〇一二三四五六七八九')
    return num_str.translate(trans)

def convert2kansuuji_matched_digits(match) -> str:
    nonnumber_part = match.group(1)
    number_part = match.group(2)
    kansuuji = convert2kansuuji(number_part)
    return nonnumber_part+kansuuji

def convert2kansuuji_matched_syosuu(match) -> str:
    number_part = match.group(1)
    kansuuji = convert2kansuuji(number_part)
    return f"テン{kansuuji}"

def convert2kansuuji_matched_number(match) -> str:
    number_part = match.group()
    # お金のカンマは消す
    number_part = number_part.replace(',', '')
    return num2words.num2words(int(number_part), lang='ja')

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
    # normalizeでascii文字は半角、カナなどは全角に
    text = unicodedata.normalize('NFKC', text)

    # 英語をカタカナ読みに
    text = romaji2katakana(text)

    # マイナス読み
    text = re.sub(r'-([1-9][0-9,]+)', r'マイナス\1', text)

    # 数値ではない数字(0始まりの値や小数点以下)は単純に漢数字に
    # ゼロはじまり
    text = re.sub(r'([^0-9])(0[0-9]+)', convert2kansuuji_matched_digits, text)
    # 小数点以下
    text = re.sub(r'\.([0-9]+)', convert2kansuuji_matched_syosuu, text)

    # 数値は漢数字に
    # (2026 -> 二千二十六)
    text = re.sub(r'[1-9][0-9,]+', convert2kansuuji_matched_number, text)

    # 残したい文字以外を消す
    # \u3040-\u309F: ひらがな, \u30A0-\u30FF: カタカナ, \u4E00-\u9FFF: cjk統合漢字
    # そのまま渡すとエラーになる文字も含むかもしれないので、消すか後で読みに変換するか調整する
    pattern = r"[^a-zA-Z_\s\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF〇一二三四五六七八九.?!_…、。．@#$%^&*（)(）_+=\[「」\]></\~～―ー\"]"
    text = re.sub(pattern, "", text)

    # 読めない記号を読める形に変換
    # 固定の変換ルールなので場面によっては不自然になってしまう
    table = {
        '_': '、',
        '…': '、',
        ', ': '、',
        '. ': '。',
        '#': 'ナンバー',
        '$': 'ドル',
        '%': 'パーセント',
        '&': 'アンド',
        '+': 'プラス',
        '/': 'スラッシュ',
        '^': 'キャレット',
        '<': 'ショウナリ',
        '=': 'イコール',
        '>': 'ダイナリ',
        '@': 'アット',
        '|': '',
        '~': 'チルダ',
        '―': '.',
        '`': '',
    }
    for k, v in table.items():
        text = text.replace(k, v)

    return text
