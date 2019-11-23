'''
Defines the set of symbols used in text input to the model.

The default is a set of ASCII characters that works well for English or text that has been run
through Unidecode. For other data, you can modify _characters. See TRAINING_DATA.md for details.
'''
from text import cmudict

_pad = '_'
_eos = '~'
_characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!\'(),-.:;? '

# Prepend "@" to ARPAbet symbols to ensure uniqueness (some are the same as uppercase letters):
_arpabet = ['@' + s for s in cmudict.valid_symbols]

# Export all symbols:
# symbols = [_pad, _eos] + list(_characters) + _arpabet


def get_pinyin():
    from pypinyin.constants import PINYIN_DICT
    from pypinyin.style import convert

    pinyin_set_raw = {p for pin in PINYIN_DICT.values() for p in pin.split(",") if p.strip()}
    pinyin_set = {convert(p, 8, True) for p in pinyin_set_raw}
    pin_set = {convert(p, 3, True) for p in pinyin_set_raw}
    yin_set = {convert(p, 9, True) for p in pinyin_set_raw}
    # oov
    # 0x6B38:欸: 'āi,ǎi,xiè,ế,éi,ê̌,ěi,ề,èi,ê̄,ēi',
    # 0x8A92:誒: 'éi,xī,yì,ê̄,ế,ê̌,ěi,ề,èi,ēi',
    # 0x5677:噷: 'hm,xīn,hēn',
    # 0x5535:唵: 'ǎn,ng,n',


# 辅音：24
fu_list = ['b', 'c', 'ch', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n',
           'p', 'q', 'r', 's', 'sh', 't', 'w', 'x', 'y', 'z', 'zh']

# 元音：185
yuandiao_list = [
    'a', 'a1', 'a2', 'a3', 'a4', 'ai', 'ai1', 'ai2', 'ai3', 'ai4', 'an', 'an1', 'an2', 'an3', 'an4', 'ang', 'ang1',
    'ang2', 'ang3', 'ang4', 'ao', 'ao1', 'ao2', 'ao3', 'ao4', 'e', 'e1', 'e2', 'e3', 'e4', 'ei', 'ei1', 'ei2', 'ei3',
    'ei4', 'en', 'en1', 'en2', 'en3', 'en4', 'eng', 'eng1', 'eng2', 'eng3', 'eng4', 'er2', 'er3', 'er4', 'i', 'i1',
    'i2', 'i3', 'i4', 'ia', 'ia1', 'ia2', 'ia3', 'ia4', 'ian', 'ian1', 'ian2', 'ian3', 'ian4', 'iang', 'iang1', 'iang2',
    'iang3', 'iang4', 'iao', 'iao1', 'iao2', 'iao3', 'iao4', 'ie', 'ie1', 'ie2', 'ie3', 'ie4', 'in', 'in1', 'in2',
    'in3', 'in4', 'ing', 'ing1', 'ing2', 'ing3', 'ing4', 'io', 'io1', 'iong1', 'iong2', 'iong3', 'iong4', 'iou', 'iou1',
    'iou2', 'iou3', 'iou4', 'm2', 'n2', 'n3', 'n4', 'ng', 'ng2', 'ng3', 'ng4', 'o', 'o1', 'o2', 'o3', 'o4', 'ong',
    'ong1', 'ong2', 'ong3', 'ong4', 'ou', 'ou1', 'ou2', 'ou3', 'ou4', 'u', 'u1', 'u2', 'u3', 'u4', 'ua', 'ua1', 'ua2',
    'ua3', 'ua4', 'uai', 'uai1', 'uai2', 'uai3', 'uai4', 'uan1', 'uan2', 'uan3', 'uan4', 'uang', 'uang1', 'uang2',
    'uang3', 'uang4', 'uei', 'uei1', 'uei2', 'uei3', 'uei4', 'uen', 'uen1', 'uen2', 'uen3', 'uen4', 'ueng1', 'ueng3',
    'ueng4', 'uo', 'uo1', 'uo2', 'uo3', 'uo4', 'uong4', 'v', 'v1', 'v2', 'v3', 'v4', 'van', 'van1', 'van2', 'van3',
    'van4', 've1', 've2', 've3', 've4', 'vn', 'vn1', 'vn2', 'vn3', 'vn4'
]

# 标点：8
biao_list = ['　', '、', '。', '！', '，', '：', '；', '？']

# 空白：3，无辅音，元音，其他
# non_list = ['^', '-', '*']

# 字母：24
en_list = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

# 元音无音调：39, 去除m,n
yuan_list = [
    'a', 'ai', 'an', 'ang', 'ao', 'e', 'ei', 'en', 'eng', 'er', 'i', 'ia', 'ian', 'iang', 'iao', 'ie', 'in', 'ing',
    'io', 'iong', 'iou', 'ng', 'o', 'ong', 'ou', 'u', 'ua', 'uai', 'uan', 'uang', 'uei', 'uen', 'ueng', 'uo',
    'uong', 'v', 'van', 've', 'vn'
]

# 音调：4
diao_list = ['1', '2', '3', '4']

# 空白：4，无辅音，元音，音调，其他
non_list = ['^', '-', '5', '*']

# 217
# symbols = fu_list + yuan_list + biao_list + non_list

# 77
symbols = [_pad, _eos] + fu_list + yuan_list + diao_list + biao_list + non_list

index2symbol = {i: w for i, w in enumerate(symbols)}
symbol2index = {w: i for i, w in enumerate(symbols)}


print(r"symbols number: {}".format(len(symbols)))
assert len(symbols) == len(set(symbols))
