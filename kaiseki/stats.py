"""TODO:
module docstring
"""


from collections import defaultdict
import math
# import statistics

from sudachipy import Dictionary, SplitMode

import utils


# TODO: vocab_local_freq stores occ not freq
class Analyzer():
    """TODO
    docstring
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
        #self.avg_vocab_freq = 0
        #self.p90_vocab_freq = 0
        self.p90_kanji_freq = 0
        self.avg_sentence_len = 0
        self.kanji_density = 0
        self.difficulty = 0

        self._tokenizer = Dictionary().create()
        self._analyze_file(path)
        self._finalize_stats()
    

    def _analyze_file(self, path):
        """TODO: docstring"""
        for line in utils.file_to_string(path).splitlines():
            for sentence in utils.split(line):
                sentence = utils.filter_japanese(sentence)
                if sentence == '':
                    continue
                self._analyze_sentence(sentence)
    

    def _analyze_sentence(self, sentence):
        """TODO: docstring"""
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
        """TODO: docstring"""
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
        #self.avg_vocab_freq = round(sum(utils.get_vocab_freq(v) for v in self.vocab_chrono) / self.unique_vocab)
        #self.p90_vocab_freq = self._calc_percentile_vocab_freq(90)
        self.p90_kanji_freq = self._calc_percentile_kanji_freq(90)
        self.avg_sentence_len = round(self.char_count / self.sentence_count, 1)
        self.kanji_density = round(self.kanji_count / self.char_count, 2)
        self.difficulty = self._calc_difficulty()


    def _sort_freq(self, rev, dic):
        """Returns a version of the dictionary sorted in ascending order of its values."""
        return dict(sorted(dic, key=lambda item: item[1], reverse=rev))


    def _calc_percentile_vocab_freq(self, percentile):
        """TODO: docstring"""
        freq_values = list(self.vocab_global_freq.values())
        index = math.ceil(len(freq_values) * percentile / 100) - 1
        return freq_values[index]
    

    def _calc_percentile_kanji_freq(self, percentile):
        """TODO: docstring"""
        if self.kanji_count == 0:
            return 0
        freq_values = list(self.kanji_global_freq.values())
        index = math.ceil(len(freq_values) * percentile / 100) - 1
        return freq_values[index]


    def _calc_difficulty(self):
        """TODO: docstring"""
        def f(x):
            res = -(0.00168 * x - 4)
            res = 1 + math.exp(res)
            return 10.272 / res

        return round(max(f(self.p90_kanji_freq), 1), 1)
        # s = max(1, 0.7339 + 0.2094 * self.avg_sentence_len)
        # v = max(1, 0.00023 * self.avg_vocab_freq)
        # k = max(1, -2.586 + 30.62 * self.kanji_density)
        # return round(statistics.geometric_mean([s, v, k]), 1)


    def display_stats(self):
        """TODO: docstring"""
        print(f"{"Character count":24} {self.char_count:>10,}")
        print(f"{"Word count":24} {self.vocab_count:>10,}")
        print(f"{"Kanji count":24} {self.kanji_count:>10,}")
        print(f"{"Sentence count":24} {self.sentence_count:>10,}")
        print(f"{"Unique words":24} {self.unique_vocab:>10,}")
        print(f"{"Unique words used once":24} {self.unique_vocab_once:>10,}")
        print(f"{"Unique kanji":24} {self.unique_kanji:>10,}")
        print(f"{"Unique kanji used once":24} {self.unique_kanji_once:>10,}")
        #print(f"{"Average word frequency":24} {self.avg_vocab_freq:>10,}")
        #print(f"{"Top 90% word frequency":24} {self.p90_vocab_freq:>10,}")
        print(f"{"Top 90% kanji frequency":24} {self.p90_kanji_freq:>10,}")
        print(f"{"Average sentence length":24} {self.avg_sentence_len:>10,}")
        print(f"{"Kanji density":24} {self.kanji_density:>10.0%}")
        print(f"{"Difficulty":24} {self.difficulty:>10,}")

