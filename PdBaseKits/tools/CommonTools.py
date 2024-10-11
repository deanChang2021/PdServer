import hashlib
import os
import string
import sys
import time
import unicodedata
import re

def getSys() -> str:
    if "win32" in sys.platform or "win64" in sys.platform:
        return "win"
    else:
        return "unix"

def getSaveUploadFilePath():
    if getSys() == "win":
        path = "c:/portunid/task/image/"
    else:
        path = "/Users/admin/portunid/image/"

    if not os.path.exists(path):
        os.mkdir(path)

    return path


def nonceId():
    """生成唯一的 19 位数字"""
    int1 = int(hashlib.sha256(str(time.time()).encode("utf-8")).hexdigest(), 16) % 10 ** 10
    int2 = int(hashlib.sha256(str(time.time()).encode("utf-8")).hexdigest(), 16) % 9 ** 9

    nonceid = str(int1) + str(int2)
    return nonceid

def getFileName(type:str):
    """生成唯一的 10 位数字"""
    int1 = int(hashlib.sha256(str(time.time()).encode("utf-8")).hexdigest(), 16) % 10 ** 10
    fileName = str(int1) + "." + type
    return fileName


def is_chinese(char):
    return unicodedata.name(char, None) in ['CJK UNIFIED IDEOGRAPH-20000', 'CJK UNIFIED IDEOGRAPH']


def is_alphanum(char):
    return char.isalpha() or char.isdigit()


def is_punctuation(char):
    return char in string.punctuation


def is_chinese_english_alnum_punct(char):
    return is_chinese(char) or is_alphanum(char) or is_punctuation(char)

