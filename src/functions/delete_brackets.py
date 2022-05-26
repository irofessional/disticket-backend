import re

def delete_brackets(self, str_: str) -> str:
    # From https://qiita.com/s2hap/items/d6714b659a9f595bcac8
    table = {
           "(": "（",
            ")": "）",
            "<": "＜",
            ">": "＞",
            "{": "｛",
            "}": "｝",
            "[": "［",
            "]": "］"
           }
    for key in table.keys():
        str_ = str_.replace(key, table[key])
        l = ['（[^（|^）]*）', '【[^【|^】]*】', '＜[^＜|^＞]*＞', '［[^［|^］]*］',
             '「[^「|^」]*」', '｛[^｛|^｝]*｝', '〔[^〔|^〕]*〕', '〈[^〈|^〉]*〉']
        for l_ in l:
            str_ = re.sub(l_, "", str_)
        """ recursive processing """
        if sum([1 if re.search(l_, str_) else 0 for l_ in l]) > 0:
            str_ = self._delete_brackets(str_)

        return str_
