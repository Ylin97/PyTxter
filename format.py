import re

from chardet.universaldetector import UniversalDetector


# 常量
HEAD_SPACE = ' ' * 4
CHAPTER_NAME_RE = re.compile(r'第(.{1,9})[章节回卷集部篇]\s*.{0,24}\s')

# 全局变量
result_text = ''

def detect_encoding(filepath):
    """检测文件编码
    Args:
        detector: UniversalDetector 对象
        filepath: 文件路径
    Return:
        file_encoding: 文件编码
        confidence: 检测结果的置信度，百分比
    """
    chinese_codings = ['GBK', 'GB2312', 'GB18030']  # 字符集 GB2312 < GBK < GB18030
    detector = UniversalDetector()
    detector.reset()
    for each in open(filepath, 'rb'):
        detector.feed(each)
        if detector.done:
            break
    detector.close()
    file_encoding = detector.result['encoding']
    confidence = detector.result['confidence']
    if file_encoding is None:
        file_encoding = 'unknown'
        confidence = 0.99
    elif file_encoding in chinese_codings:
        file_encoding = 'GB18030'
    return file_encoding, confidence

def chapter_name_normalize(lines: list) ->list:
    """标准化章节名"""
    for i, line in enumerate(lines):
        parts = []
        positions = [(m.start(), m.end()) for m in re.finditer(CHAPTER_NAME_RE, line)]
        chapter_name = ''
        if positions:
            p = 0
            for start, end in positions:
                parts.append(line[p:start])
                # chapter_name = ('' if start == 0 else '\n\n') + line[start:end].strip()
                chapter_name = ('' if i == 0 else '\n\n') + line[start:end].strip()
                if end < len(line):
                    chapter_name += '\n\n'
                elif end == len(line) and i + 1 < len(lines) and lines[i + 1].strip():
                    chapter_name += '\n\n'
                else:
                    chapter_name += '\n'
                # if i + 1 < len(lines) and lines[i + 1].isspace():  # 保持章节名下面的空行不增加
                #     parts.append(chapter_name)
                #     p = end
                #     continue
                parts.append(chapter_name)
                p = end
            parts.append(line[p:])
            res = ''
            for part in parts:
                res += part
            lines[i] = res
    return lines


def clean_line(lines: list) ->list:
    """清除空白行"""
    return [line for line in lines if line.strip()]


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


def auto_format(lines: list, para_bound=None) ->str:
    """自动格式化"""
    global result_text
    result_text = ''
    tmp = ''
    for item in chapter_name_normalize(correct_punctuation(lines)):
        tmp += item
    lines = tmp.split('\n')
    # lines = clean_line(chapter_name_normalize(lines))
    text_str1 = lines[0]
    # 处理开头的空行
    pos = 1
    while text_str1.isspace():
        text_str1 = lines[pos]
        pos += 1
    text_str1 = deal_chapter_name("", text_str1, True)[1].strip()
    for line in lines[pos:]:
        if line.isspace():
            continue
        # while text_str1.isspace():
        text_str2 = line
        text_str1, text_str2 = deal_chapter_name(text_str1, text_str2)
        text_str1 = deal_line(text_str1, text_str2, para_bound)
        # 写入最后一行
    if text_str1:
        result_text += HEAD_SPACE + text_str1 + '\n'
    
    return result_text


def deal_line(text_str1, text_str2, para_bound=None):
    """行合并和段落拆分"""
    global result_text

    text_str2 = text_str2.strip()
    len_text_str2 = len(text_str2)

    if len_text_str2 > 3 and len(set(text_str2)) == 1:  # 处理 ***** 这类分割线
        st = list(set(text_str2))[0]
        # new_file.write('    ' + st * 24 + '\n')
        result_text += HEAD_SPACE + st * 24 + '\n'
        return ""

    if len_text_str2 > 3 and str(text_str2[0:3]) == str(text_str2[-3:]):  # 处理 ***Text*** 这类分割线
        # new_file.write('    ' + text_str1 + '\n')
        # new_file.write('    ' + text_str2 + '\n')
        result_text += HEAD_SPACE + text_str1 + '\n'
        result_text += HEAD_SPACE + text_str2 + '\n'
        return ""
    else:
        if isparagraph_break(text_str1):
            # new_file.write('    ' + text_str1 + '\n')
            result_text += HEAD_SPACE + text_str1 + '\n'
            text_str1 = text_str2
        else:
            text_str1 += text_str2

        if para_bound:
            return split_paragraph(text_str1, para_bound)
        else:
            return text_str1


def deal_chapter_name(text_str1, text_str2, ishead=False):
    """判断和写入章节名"""
    global result_text
    tmp_str = text_str2.strip()
    if ischapter_name(tmp_str):
        if text_str1:
            # new_file.write('    ' + text_str1 + '\n')
            result_text += HEAD_SPACE + text_str1 + '\n'
            text_str1 = ""
        # 第一章章节名
        if ishead:
            write_chapter_name(tmp_str, True)
            # ishead = False
        else:
            write_chapter_name( tmp_str)
        text_str2 = ""

    return text_str1, text_str2        


def isparagraph_break(text_str):
    """判断结尾标点是否为中英句号、感叹号、反引号和省略号"""
    text_str = text_str.strip()
    if not text_str:
        return False
    else:
        st = text_str[-1:]
        if len(text_str) >= 2 and text_str[-2:] == "……":
            return True
        elif re.match(r'[\.\。\"\”\」\』\!\！\?\？\:\:]', st):
            return True
        else:
            return False


def ischapter_name(text_str):
    """判断是否是章节名"""
    if re.match(CHAPTER_NAME_RE, text_str):
        return True
    else:
        return False


def write_chapter_name(chapter_name, ishead=False):
    """处理章节名"""
    global result_text
    if not ishead:
        # new_file.write('\n')
        result_text += '\n'
    # new_file.write(chapter_name + '\n')
    result_text += chapter_name + '\n'


def split_paragraph(text_str, para_bound):
    """将长度超过100的段落拆分并写入文件"""
    global result_text
    temp_str = ""
    len_text_str = len(text_str)
    if len_text_str <= para_bound:
        return text_str
    else:
        count = 0
        re_punctuations1 = re.compile(r'[\.\。\"\”\」\』\!\！\…\?\？\,\，\:\：]')
        re_punctuations2 = re.compile(r'[\.\。\!\！\…\?\？]')
        re_punctuations3 = re.compile(r'[\"\”\」\』\:\：]')
        re_punctuations4 = re.compile(r'[\,\，]')
        flag = 0
        for st in text_str:
            count += 1
            # 处理 …… 。。 ...!!!???这类符号序列
            if re.match(re_punctuations2, st) and count < len_text_str \
                    and re.match(re_punctuations2, text_str[count]):
                temp_str += st
            # 处理可能的分段符号
            elif re.match(re_punctuations1, st) and len(temp_str) > para_bound:
                if count == len_text_str and re.match(re_punctuations3, st):
                    # new_file.write('    ' + temp_str + st + '\n')
                    result_text += HEAD_SPACE + temp_str + st + '\n'
                    temp_str = ""
                elif count < len_text_str:
                    # 处理不属于引号的情况
                    if re.match(re_punctuations2, st) and not re.match(re_punctuations3, text_str[count]):
                        # new_file.write('    ' + temp_str + st + '\n')
                        result_text += HEAD_SPACE + temp_str + st + '\n'
                        temp_str = ""
                    # 处理属于引号的情况，如 ....愿我如星君如月，夜夜流光相皎洁。”
                    elif re.match(re_punctuations2, st) and re.match(re_punctuations3, text_str[count]):
                        temp_str += st
                    elif re.match(re_punctuations3, st) and not re.match(re_punctuations4, text_str[count]):
                        # new_file.write('    ' + temp_str + st + '\n')
                        result_text += HEAD_SPACE + temp_str + st + '\n'
                        temp_str = ""
                    # 处理 ...当时年少青衫薄”，他惆怅着说道，... 这种情况
                    elif re.match(re_punctuations3, st) and re.match(re_punctuations4, text_str[count]):
                        temp_str += st
                        flag = 1
                    elif flag == 1:
                        # new_file.write('    ' + temp_str + st + '\n')
                        result_text += HEAD_SPACE + temp_str + st + '\n'
                        temp_str = ""
                        flag = 0
                    else:
                        temp_str += st
                else:
                    temp_str += st
            else:
                temp_str += st
    return temp_str


def get_all_chapter_name(lines: list) -> dict:
    """获取所有的章节名"""
    chapter_names = {}
    for num, line in enumerate(lines):
        if ischapter_name(line):
            chapter_names[line.strip()] = num + 1
    return chapter_names


if __name__ == "__main__":
    s = "第一章 开始  这是一个测试，测试正则表达式是否正确。第二章关于 开始位置匹配是否正确，正确就放回一个对象。"
    lines = chapter_name_normalize(s.split('\n'))
    print(lines)
