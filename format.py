import re


def chapter_name_normalize(lines: list)->list:
    """标准化章节名"""
    CHAPTER_NAME_RE = re.compile(r'第(.{1,9})[章节回卷集部篇]\s*.{0,24}\s')

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


def clean_line(lines: list)->list:
    """清除空白行"""
    return [line for line in lines if line.strip()]


def sub_punctuation(text: str)->str:
    """中英标点纠正"""
    pass


if __name__ == "__main__":
    s = "第一章 开始  这是一个测试，测试正则表达式是否正确。第二章关于 开始位置匹配是否正确，正确就放回一个对象。"
    lines = chapter_name_normalize(s.split('\n'))
    print(lines)
