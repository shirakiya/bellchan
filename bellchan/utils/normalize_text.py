import mojimoji


def zen_to_han(text, kana=True, digit=True, ascii=True):
    return mojimoji.zen_to_han(text, kana=kana, digit=digit, ascii=ascii)
