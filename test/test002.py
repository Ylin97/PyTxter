import re


def correct_punctuation(lines: list) ->list:
    """中英标点纠正"""
    for num, line in enumerate(lines):
        # EN to CN
        if len(re.findall(r'[\u4e00-\u9fa5]', line)) / len(line) > 0.4:
            lines = punction_replace(lines, num, 1)
        # CN to EN
        else:
            lines = punction_replace(lines, num, 0)
    return lines


def punction_replace(lines: list, num: int, lang: int) ->list:
    """中英标点替换"""
    # EN_CN_PUNC = [('\'', '’'), ('\'', '‘'), ('!', '！'), ('"', "“"), ('"', '”'), (':', '：'),
    #             (',', '，'), ('.', '。'), ('?', '？')]
    EN_CN_PUNC = [ ('!', '！'), (':', '：'), (',', '，'), ('.', '。'), ('?', '？')]
    for c in lines[num]:
        i = 0
        for punc in (x[~lang] for x in EN_CN_PUNC):
            if c == punc:
                lines[num] = lines[num].replace(c, EN_CN_PUNC[i][lang])
                break
            i += 1
    return lines

lines = ['A test。to Python.', '测试,测试。', '正是一个测试"hello".']

print(correct_punctuation(lines))
# print('a apple。string'.replace('。', '.'))