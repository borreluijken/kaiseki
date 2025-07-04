# Kaiseki
Kaiseki is a Python library / CLI tool that statistically analyzes Japanese text.

## Setup
```
$ pip install sudachipy sudachidict_core beautifulsoup4 ebooklib
$ git clone https://github.com/borreluijken/kaiseki.git
```

## Usage
CLI tool usage example:
```
$ python3 -m kaiseki data/youfunroku.epub
  Character count               4,667
  Word count                    3,235
  Kanji count                   1,861
  Sentence count                  189
  Unique words                    919
  Unique words used once          618
  Unique kanji                    659
  Unique kanji used once          340
  Top 90% kanji frequency       2,260
  Average sentence length        24.7
  Kanji density                   40%
```

Library usage example:
```
import kaiseki

text = kaiseki.Analyzer("data/youfunroku.epub")

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


import kaiseki.utils

text = kaiseki.utils.filter_japanese("English 日本語 Русский العربية 한국어 हिन्दी")
# >> "日本語"

text = kaiseki.utils.remove_furigana("これは〈振り仮名〉《ふりがな》です")
# >> "これは振り仮名です"

kaiseki.utils.is_kanji('字')
# >> True

freq = kaiseki.utils.get_vocab_freq("言葉")
# >> 124

kaiseki.utils.get_kanji_freq("字")
# >> 386

text = kaiseki.utils.file_to_string("data/youfunroku.epub")
```

## Credits
[SudachiPy](https://github.com/Tokamei/sudachipy) used as morphological analyzer  
vocab_freq.csv and kanji_freq.csv based on JPDB v2.2 data from https://github.com/Kuuuube/yomitan-dictionaries  
youfunroku.epub (provided as an example text) adapted from https://www.aozora.gr.jp/cards/000119/files/56243_53070.html  
