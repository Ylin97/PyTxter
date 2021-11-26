# coding=utf-8

"""
# Usage: python ./txtebook_format.py
"""

import re
import os
import sys
from shutil import copy2

from chardet.universaldetector import UniversalDetector


def run():
    """删除文本文件中的多余换行符"""
    # 获取文件名
    filename = get_filename()
    # filename = '111.txt'
    # 转换编码
    file_to_utf8(filename)
    # 处理文件
    remove_extra_line_break(filename)


def get_filename():
    """从用户输入中获取文件名"""
    filename = input("请输入文件名或文件路径(例如：111.txt or ~/111.txt)：\n")
    return filename


def remove_extra_line_break(filename):
    """删除文件中多余的换行符"""
    tmp_file = filename[:-4] + '_tmp' + filename[-4:]
    with open(tmp_file, "r", encoding="utf-8") as origin_file:
        with open(filename, "w", encoding="utf-8") as new_file:
            text_str1 = origin_file.readline()
            # 处理开头的空行
            while text_str1.isspace():
                text_str1 = origin_file.readline()
            text_str1 = deal_chapter_name(new_file, "", text_str1, True)[1].strip()
            text_str2 = origin_file.readline()
            while text_str2:
                text_str1, text_str2 = deal_chapter_name(new_file, text_str1, text_str2)
                text_str1 = deal_line(new_file, text_str1, text_str2)
                text_str2 = origin_file.readline()
            # 写入最后一行
            if text_str1:
                # split_paragraph(new_file, text_str1)
                new_file.write('    ' + text_str1 + '\n')
    # 移除临时文件
    os.remove(tmp_file)


def deal_line(new_file, text_str1, text_str2):
    """行合并和段落拆分"""
    text_str2 = text_str2.strip()
    len_text_str2 = len(text_str2)

    if len_text_str2 > 3 and len(set(text_str2)) == 1:  # 处理 ***** 这类分割线
        st = list(set(text_str2))[0]
        new_file.write('    ' + st * 24 + '\n')
        return ""

    if len_text_str2 > 3 and str(text_str2[0:3]) == str(text_str2[-3:]):  # 处理 ***Text*** 这类分割线
        new_file.write('    ' + text_str1 + '\n')
        new_file.write('    ' + text_str2 + '\n')
        return ""
    else:
        if isparagraph_break(text_str1):
            new_file.write('    ' + text_str1 + '\n')
            text_str1 = text_str2
        else:
            text_str1 += text_str2

        return split_paragraph(new_file, text_str1)


def deal_chapter_name(new_file, text_str1, text_str2, ishead=False):
    """判断和写入章节名"""
    tmp_str = text_str2.strip()
    if ischapter_name(tmp_str):
        if text_str1:
            new_file.write('    ' + text_str1 + '\n')
            text_str1 = ""
        # 第一章章节名
        if ishead:
            write_chapter_name(new_file, tmp_str, True)
            # ishead = False
        else:
            write_chapter_name(new_file, tmp_str)
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
    if re.match(r'^第(.{1,9})([章节回卷集部篇])(\s*)(.*)', text_str):
        return True
    else:
        return False


def write_chapter_name(new_file, chapter_name, ishead=False):
    """处理章节名"""
    if not ishead:
        new_file.write('\n')

    new_file.write(chapter_name + '\n')


def split_paragraph(new_file, text_str):
    """将长度超过100的段落拆分并写入文件"""
    temp_str = ""
    len_text_str = len(text_str)
    if len_text_str <= 100:
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
            elif re.match(re_punctuations1, st) and len(temp_str) > 100:
                if count == len_text_str and re.match(re_punctuations3, st):
                    new_file.write('    ' + temp_str + st + '\n')
                    temp_str = ""
                elif count < len_text_str:
                    # 处理不属于引号的情况
                    if re.match(re_punctuations2, st) and not re.match(re_punctuations3, text_str[count]):
                        new_file.write('    ' + temp_str + st + '\n')
                        temp_str = ""
                    # 处理属于引号的情况，如 ....愿我如星君如月，夜夜流光相皎洁。”
                    elif re.match(re_punctuations2, st) and re.match(re_punctuations3, text_str[count]):
                        temp_str += st
                    elif re.match(re_punctuations3, st) and not re.match(re_punctuations4, text_str[count]):
                        new_file.write('    ' + temp_str + st + '\n')
                        temp_str = ""
                    # 处理 ...当时年少青衫薄”，他惆怅着说道，... 这种情况
                    elif re.match(re_punctuations3, st) and re.match(re_punctuations4, text_str[count]):
                        temp_str += st
                        flag = 1
                    elif flag == 1:
                        new_file.write('    ' + temp_str + st + '\n')
                        temp_str = ""
                        flag = 0
                    else:
                        temp_str += st
                else:
                    temp_str += st
            else:
                temp_str += st
    return temp_str


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


def file_to_utf8(filename):
    """将文件编码转为utf-8"""
    tmp_file = filename[:-4] + '_tmp' + filename[-4:]
    copy2(filename, tmp_file)
    old_file = filename[:-4] + '_old' + filename[-4:]
    os.rename(filename, old_file)

    # with open(tmp_file, 'r') as file:
    file_encoding, confidence = detect_encoding(tmp_file)

    if (file_encoding != 'unknown') and (confidence > 0.75):
        if file_encoding != 'utf-8':
            with open(tmp_file, 'r', encoding=file_encoding, errors='replace') as file:
                text = file.read()
            # with open('u' + filename, 'w', encoding='utf-8', errors='replace') as file:
            with open(tmp_file, 'w', encoding='utf-8', errors='replace') as file:
                file.write(text)


if __name__ == "__main__":
    sys.exit(run())