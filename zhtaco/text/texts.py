#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: KDD
# @time: 2018-11-10
"""
"""
import os
import re
import json
import collections as clt
from pypinyin import pinyin
from text.symbols import biao_list, non_list, symbol2index, diao_list

BIAO_PATT = re.compile(r"[{}]".format("".join(biao_list)))
DIAO_PATT = re.compile(r"([{}]$)".format("".join(diao_list)))


def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring


def strB2Q(ustring):
    """半角转全角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 32:  # 半角空格直接转化
            inside_code = 12288
        elif inside_code >= 32 and inside_code <= 126:  # 半角字符（除空格）根据关系转化
            inside_code += 65248

        rstring += chr(inside_code)
    return rstring


def pinyin_errors(text="", repatt=BIAO_PATT):
    out = repatt.findall(text)
    return out if out else non_list[-1]


def text2pintext(text=""):
    pin_list = pinyin(text, style=3, errors=pinyin_errors, strict=False)
    yin_list = pinyin(text, style=9, errors=pinyin_errors, strict=False)
    assert len(pin_list) == len(yin_list)
    ys_list = []
    for fu, yuan in zip(pin_list, yin_list):
        if fu == yuan:
            ys_list.extend(fu)
        else:
            ys_list.append(non_list[0] if fu[0] not in symbol2index else fu[0])
            yuan_diao = [w for w in DIAO_PATT.split(yuan[0]) if w]
            ys_list.append(non_list[1] if yuan_diao[0] not in symbol2index else yuan_diao[0])
            ys_list.append(non_list[2] if len(yuan_diao) < 2 or yuan_diao[1] not in symbol2index else yuan_diao[1])
        ys_list.append(biao_list[0])
    text = " ".join(ys_list)
    return text


if __name__ == "__main__":
    print(__file__)
    b = strQ2B("ｍｎ123abc 博客园,.!?/\;，。！？、、；_")
    print(b)

    c = strB2Q("ｍｎ123abc 博客园,.!?/\;，。！？、、；_")
    print(c)

    out = text2pintext("你abc是谁？语音合成还是识别。")
    print(out)
    # n i3 nob sh i4 sh ei2 ？ nop v3 nop in1 h e2 ch eng2 h ai2 sh i4 sh i2 b ie2 。
