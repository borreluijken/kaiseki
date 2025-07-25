"""Statistical analysis for Kaiseki.

This module provides the `Analyzer` class, which can be used to extract
various statistics of Japanese text files (.txt, .epub).

Typical usage example:

  text = Analyzer("path/to/novel.epub")

  text.vocab_count
  # >> 3235

  text.vocab_local_freq[100:105]  # (vocab, occurrences)
  # >> [('主君', 4), ('等', 4), ('第', 4), ('夏', 4), ('二', 4)]

  text.display_stats()
  # >> Character count               4,667
  #    Word count                    3,235
  #    Kanji count                   1,861
  #    Sentence count                  189
  #    Unique words                    919
  #    Unique words used once          618
  #    Unique kanji                    659
  #    Unique kanji used once          340
  #    Top 90% kanji frequency       2,260
  #    Average sentence length        24.7
  #    Kanji density                   40%
"""


from collections import defaultdict
import math
import re

from sudachipy import Dictionary, SplitMode

from . import utils


class Analyzer():
    """Analyzes a Japanese text file to extract various statistics.
    """

    def __init__(self, path):
        self.vocab_chrono = defaultdict(int)
        self.vocab_local_freq = defaultdict(int)
        self.vocab_global_freq = defaultdict(int)
        self.kanji_chrono = defaultdict(int)
        self.kanji_local_freq = defaultdict(int)
        self.kanji_global_freq = defaultdict(int)
        self.char_count = 0
        self.vocab_count = 0
        self.kanji_count = 0
        self.sentence_count = 0
        self.unique_vocab = 0
        self.unique_vocab_once = 0
        self.unique_kanji = 0
        self.unique_kanji_once = 0
        self.p90_kanji_freq = 0
        self.avg_sentence_len = 0
        self.kanji_density = 0

        self._tokenizer = Dictionary().create()
        self._analyze_file(path)
        self._finalize_stats()
    

    def _analyze_file(self, path):
        """Analyzes the text file at the given path, extracting sentences and analyzing each one."""
        for sentence in re.split(r'[。！？「」『』«»〔〕\n]+', utils.file_to_string(path)):
            sentence = utils.remove_furigana(sentence)
            sentence = utils.filter_japanese(sentence)
            if sentence != '':
                self._analyze_sentence(sentence)


    def _analyze_sentence(self, sentence):
        """Analyzes a single sentence, updating various statistics such as character count,"""
        morphemes = self._tokenizer.tokenize(sentence, SplitMode.A)
        self.char_count += len(sentence)
        self.vocab_count += len(morphemes)
        self.sentence_count += 1

        for morpheme in morphemes:
            vocab = morpheme.dictionary_form()
            self.vocab_chrono[vocab] += 1
            for ch in vocab:
                if utils.is_kanji(ch):
                    self.kanji_chrono[ch] += 1
                    self.kanji_count += 1
    

    def _finalize_stats(self):
        """Calculates and finalizes various statistics based on the analyzed text."""
        if self.sentence_count == 0:
            return
        self.vocab_local_freq = self._sort_freq(True, self.vocab_chrono.items())
        self.kanji_local_freq = self._sort_freq(True, self.kanji_chrono.items())
        self.vocab_global_freq = self._sort_freq(False, ((v, utils.get_vocab_freq(v)) for v in self.vocab_chrono))
        self.kanji_global_freq = self._sort_freq(False, ((k, utils.get_kanji_freq(k)) for k in self.kanji_chrono))
        self.unique_vocab = len(self.vocab_chrono)
        self.unique_kanji = len(self.kanji_chrono)
        self.unique_vocab_once = sum(1 for v in self.vocab_chrono.values() if v == 1)
        self.unique_kanji_once = sum(1 for k in self.kanji_chrono.values() if k == 1)
        self.p90_kanji_freq = self._calc_percentile_kanji_freq(90)
        self.avg_sentence_len = round(self.char_count / self.sentence_count, 1)
        self.kanji_density = round(self.kanji_count / self.char_count, 2)


    def _sort_freq(self, rev, dic):
        """Returns a list version of the dictionary sorted in ascending order of its values."""
        return sorted(dic, key=lambda item: item[1], reverse=rev)


    def _calc_percentile_vocab_freq(self, percentile):
        """Returns the vocab frequency at the given percentile."""
        freq_values = [freq for _, freq in self.vocab_global_freq]
        index = math.ceil(len(freq_values) * percentile / 100) - 1
        return freq_values[index]


    def _calc_percentile_kanji_freq(self, percentile):
        """Returns the kanji frequency at the given percentile."""
        if self.kanji_count == 0:
            return 0
        freq_values = [freq for _, freq in self.kanji_global_freq]
        index = math.ceil(len(freq_values) * percentile / 100) - 1
        return freq_values[index]


    def display_stats(self):
        """Displays various statistics of the analyzed text."""
        print(f"{"Character count":24} {self.char_count:>10,}")
        print(f"{"Word count":24} {self.vocab_count:>10,}")
        print(f"{"Kanji count":24} {self.kanji_count:>10,}")
        print(f"{"Sentence count":24} {self.sentence_count:>10,}")
        print(f"{"Unique words":24} {self.unique_vocab:>10,}")
        print(f"{"Unique words used once":24} {self.unique_vocab_once:>10,}")
        print(f"{"Unique kanji":24} {self.unique_kanji:>10,}")
        print(f"{"Unique kanji used once":24} {self.unique_kanji_once:>10,}")
        print(f"{"Top 90% kanji frequency":24} {self.p90_kanji_freq:>10,}")
        print(f"{"Average sentence length":24} {self.avg_sentence_len:>10,}")
        print(f"{"Kanji density":24} {self.kanji_density:>10.0%}")
