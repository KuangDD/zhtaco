from text import cleaners, symbols, text_to_sequence, sequence_to_text
from unidecode import unidecode
from datasets.ljspeech import build_from_path


def test_symbols():
    assert len(symbols) >= 3
    assert symbols[0] == '_'
    assert symbols[1] == '~'


def test_build_from_path():
    in_dir = r"D:\git\tacotron\data"
    out_dir = r"D:\git\tacotron\data\specs"
    build_from_path(in_dir=in_dir, out_dir=out_dir)
