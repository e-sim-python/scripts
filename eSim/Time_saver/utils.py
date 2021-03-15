import re


def fight395791_(r: str):
    fg_re = 'url: (\".*fight.*.html\")'
    return re.sub("[\"\']*", "", re.findall(fg_re, r)[0])
