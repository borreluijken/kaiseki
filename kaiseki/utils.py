"""Utility functions for Kaiseki.

This module provides functions to load vocabulary and kanji frequency data,
clean Japanese text, and extract text from .epub and .txt files.

Typical usage example:

  text = filter_japanese("English 日本語 Русский العربية 한국어 हिन्दी")
  # >> "日本語"

  text = remove_furigana("これは〈振り仮名〉《ふりがな》です")
  # >> "これは振り仮名です"

  is_kanji('字')
  # >> True

  freq = get_vocab_freq("言葉")
  # >> 124

  utils.get_kanji_freq("字")
  # >> 386

  text = file_to_string("novel.epub")
"""


import csv
import re

from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
VOCAB_FREQ_CSV = BASE_DIR / 'data' / 'vocab_freq.csv'
KANJI_FREQ_CSV = BASE_DIR / 'data' / 'kanji_freq.csv'


vocab_freq_dict = None
kanji_freq_dict = None


def load_vocab_freq():
    """Loads vocab frequncy data from kaiseki/data/vocab_freq.csv."""
    global vocab_freq_dict
    vocab_freq_dict = {}
    with open(VOCAB_FREQ_CSV, encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            vocab_freq_dict[row[0]] = int(row[1])


def load_kanji_freq():
    """Loads kanji frequncy data from kaiseki/data/kanji_freq.csv."""
    global kanji_freq_dict
    kanji_freq_dict = {}
    with open(KANJI_FREQ_CSV, encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            kanji_freq_dict[row[0]] = int(row[1])


def filter_japanese(string):
    """Removes any characters that aren't hiragana, katakana or kanji."""
    japanese_re = re.compile(r'[\u3040-\u30FF\u4E00-\u9FFF]')
    return ''.join(japanese_re.findall(string))


def remove_furigana(string):
    """Removes furigana from a string."""
    string = re.sub(r'《.*?》', '', string)
    string = re.sub(r'[〈〉]', '', string)
    return string


def is_kanji(char):
    """Determines whether a character is kanji or not."""
    return bool(re.search(r'[\u4E00-\u9FFF]', char))


def get_vocab_freq(vocab):
    """Returns the vocab's global frequency."""
    global vocab_freq_dict
    if vocab_freq_dict is None:
        load_vocab_freq()
    return vocab_freq_dict.get(vocab, 317300)


def get_kanji_freq(kanji):
    """Returns the kanji's global frequency."""
    global kanji_freq_dict
    if kanji_freq_dict is None:
        load_kanji_freq()
    return kanji_freq_dict.get(kanji, 5526)


def epub_to_string(path):
    """Extracts and returns all text from an .epub file as a string."""
    book = epub.read_epub(path)
    texts = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_body_content(), 'html.parser')
            texts.append(soup.get_text())
    return '\n'.join(texts)


def txt_to_string(path):
    """Extracts and returns all text from a .txt file as a string."""
    with open(path, encoding='utf-8') as f:
        return f.read()


def file_to_string(path):
    """Extracts and returns all text from the file as a string."""
    path_obj = Path(path)
    ext = path_obj.suffix.lower()
    if ext == '.epub':
        return epub_to_string(path_obj)
    if ext == '.txt':
        return txt_to_string(path_obj)
    raise ValueError(f"Unsupported file extension: {ext}")
