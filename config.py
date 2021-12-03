"""
# ---------------配置信息------------------
# DATA: 2021/12/03 11:02
# Author: yalin
# History: Create Config and Font class
"""

import os
import configparser

from PyQt5.QtGui import QFont

from qcodeeditor import QCodeEditor
from ui3 import MainWindow


# 常量
CONFIG_FILE_PATH = "notepad.ini"


class Config:
    """配置类"""
    def __init__(self, main_window: MainWindow, text_obj: QCodeEditor) -> None:
        self.editor = text_obj
        self.window = main_window
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_FILE_PATH, 'utf-8')

        # Font attribute
        self.font_family = 'Consolas'
        self.font_size = '16'
        self.font_bold = 'False'
        self.font_italic = 'False'
        self.font_strikeOut = 'False'
        self.font_underline = 'False'

    def judge_config(self):
        """如果配置文件不存在，则新建"""
        if not os.path.exists(CONFIG_FILE_PATH):
            f = open(CONFIG_FILE_PATH, 'w', encoding='utf-8')
            f.close()

    def read_settings(self):
        # 调节窗口大小
        width = self.get_config('Display', 'width', 1000)
        height = self.get_config('Display', 'height ', 800)
        px = self.get_config('Display', 'x', 0)
        py = self.get_config('Display', 'y', 0)
        self.window.move(int(px), int(py))
        self.window.resize(int(width), (height))

        self.default_dir = self.get_config('Setting', 'dir', '')

        self.font_family = self.get_config('Font', 'family', 'Consolas')
        self.font_size = self.get_config('Font', 'size', '10')
        self.font_bold = self.get_config('Font', 'bold', '0')
        self.font_italic = self.get_config('Font', 'italic', '0')
        self.font_strikeOut = self.get_config('Font', 'strikeOut', '0')
        self.font_underline = self.get_config('Font', 'underline', '0')
        font = QFont(self.font_family, int(self.font_size))
        font.setBold(int(self.font_bold))
        font.setItalic(int(self.font_italic))
        font.setStrikeOut(int(self.font_strikeOut))
        font.setUnderline(int(self.font_underline))
        self.editor.setFont(font)
        # self.window.font = font

    def write_setting(self):
        """写入用户自定义设置信息到配置文件"""
        # 窗口位置信息
        self.write_config('Display', 'width', str(self.window.size().width()))
        self.write_config('Display', 'height', str(self.window.size().height()))
        self.write_config('Display', 'x', str(self.window.pos().x()))
        self.write_config('Display', 'y', str(self.window.pos().y()))

        self.write_config('Setting', 'dir', self.default_dir)

        self.write_config('Font', 'family', self.editor.font().family())
        self.write_config('Font', 'size', str(self.editor.font().pointSize()))
        self.write_config('Font', 'bold', int(self.editor.font().bold()))
        self.write_config('Font', 'italic', int(self.editor.font().italic()))
        self.write_config('Font', 'strikeOut', int(
            self.editor.font().strikeOut()))
        self.write_config('Font', 'underline', int(
            self.editor.font().underline()))

        # 写入文件
        self.config.write(open(CONFIG_FILE_PATH, 'w', encoding='utf-8'))

    def get_config(self, section, key, default):
        # 返回配置信息，如果获取失败返回默认值
        try:
            return self.config[section][key]
        except:
            return default
    
    def write_config(self, section, key, value):
        # 向config写入信息
        if not self.config.has_section(section):
            self.config.add_section(section)
        # value必须是str，否则会抛TypeError
        self.config.set(section, key, str(value))


class MyFont:
    """字体类"""
    def __init__(self) -> None:
        self.family = 'Consolas'
        self.size = '16'
        self.bold = 'False'
        self.italic = 'False'
        self.strikeOut = 'False'
        self.underline = 'False'