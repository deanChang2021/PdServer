# !/usr/bin/env python
# -*-coding:utf-8 -*-
import os
import sys
from configparser import ConfigParser  # configparser第三方库，用来解析ini配置文件的解析器

class IniConfig:

    def __init__(self, filepath):
        """获取文件路径和表单名"""
        # self.filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.ini')
        self.filepath = filepath
        self.conf = ConfigParser()

    def get_sections(self):
        self.conf.read(self.filepath, encoding='UTF-8')  # 读取ini文件
        return self.conf.sections()

    def get_section(self, section):
        """
        读取到指定section中的所有数据，返回一个字典
        :param section:指定section名
        :return:
        """
        self.conf.read(self.filepath, encoding='UTF-8')  # 读取ini文件
        return dict(self.conf.items(section))

    def get_value(self, section, key):
        """以string类型返回section中key的值,不存在则返回None"""
        try:
            self.conf.read(self.filepath, encoding='UTF-8')  # 读取ini文件
            value = self.conf.get(section, key)
            # value = self.conf[section][key]
            # value = self.conf.getint(section,key) # 返回int型
            # value = self.conf.getfloat(section,key) # 返回float型
            # value = self.conf.getboolean(section,key) # 返回bool型
            return value
        except:
            # print(f"读取{section}-{key}的值失败")
            pass

    def set_value(self, section, key, value):
        """设置section-key-value
        :param section:指定section名
        :param key:
        :param value:
        :return:
        """
        try:
            print("self.filepath:" + self.filepath)
            self.conf.read(self.filepath, encoding='UTF-8')  # 读取ini文件
            print(self.conf.has_section(section))
            if not self.conf.has_section(section):  # 判断是否包含指定section
                self.conf.add_section(section)  # 添加section到配置文件
            self.conf.set(section, key, str(value))  # 添加section的key-value
            with open(self.filepath, "w") as f:
                self.conf.write(f)  # 将configparser对象写入.ini类型的文件
        except:
            print(f"修改{section}-{key}的值失败，{value}")
            pass

    def add_section(self, section, option: dict):
        """
        新增section，option项
        :param section:新增section
        :param option:option项，字典key-value形式
        :return:
        """
        try:
            self.conf[section] = option
            with open(self.filepath, "w") as f:
                self.conf.write(f)  # 将configparser对象写入.ini类型的文件
        except:
            pass

    def remove_option(self, section, option):
        self.conf.read(self.filepath, encoding='UTF-8')  # 读取ini文件
        self.conf.remove_option(section, option)
        with open(self.filepath, "w") as f:
            self.conf.write(f)  # 将configparser对象写入.ini类型的文件

    def remove_section(self, section):
        self.conf.read(self.filepath, encoding='UTF-8')  # 读取ini文件
        self.conf.remove_section(section)
        with open(self.filepath, "w") as f:
            self.conf.write(f)  # 将configparser对象写入.ini类型的文件


if __name__ == "__main__":
    logPath=""
    if "win32" in sys.platform or "win64" in sys.platform:
        logPath = "c:/portunid/task/config"
    else:
        logPath = "/Users/admin/config"

    configpath = logPath + "/config.ini"
    #configpath = os.path.join(os.getcwd(), 'setting.ini')  # config.ini文件路径
    conf = IniConfig(configpath)
    conf.set_value("user", "name", "zyy")
    # conf.set_value("user", "name", "ccy")
    # conf.set_value("user", "age", 24)
    # print( conf.get_sections())
    # print( conf.get_section("user"))
    # user_name = conf.get_value("user", "name")
    # user_age = conf.get_value("user", "age")
    # user_class = conf.get_value("user", "class")
    # print(user_name, user_age, user_class)
    #
    # test = {
    #     'url': '0.0.0.0',
    #     'username': 6000,
    #     'password': 1.3,
    #     'toekn': 'ASDFGHJKLwertyuio3456789sdfgh'
    # }
    # conf.add_section("test", test)
    # print(conf.get_section("default"))
    # print(conf.get_value("default", "image_folder"))

    # conf.remove_option("test", "url")
    #
    # conf.remove_section("test")