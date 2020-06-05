# -*- coding: utf-8 -*-
"""
Lipsum generator

"""

import numpy
import pickle
import re

import nltk
from spellchecker import SpellChecker

# %%
# Extract abstracts from document
articles = open('dgen/all.xml', 'r', encoding='utf8', errors='ignore').read()
# remove all newline characters
abstracts = re.sub(r'\n', '', articles, flags=re.DOTALL)
abstracts = re.sub(r'</p>\s+</abstract>.+?<abstract>\s+<p>', r'\n', articles,
                   flags=re.DOTALL)  # remove everything in the middle of the document
abstracts = re.sub(r'\A.+?<abstract>\s+<p>', r'\n', abstracts,
                   flags=re.DOTALL)  # extra care for begining of string
abstracts = re.sub(r'</p>\s+</abstract>.+?\Z', r'\n', abstracts,
                   flags=re.DOTALL)  # extra care for end of string

# Remove <tex-math> stuff </tex-math>
abstracts = re.sub(r'&lt;[a-z-]+&gt;.+?&lt;/[a-z-]+&gt;', r' ', abstracts)
abstracts = re.sub(r'<[a-z-]+>.+?</[a-z-]+>', r' ', abstracts)
abstracts = re.sub(r'&lt;|&gt;', r' ', abstracts)

# Remove things like t1, y0, 1T2
abstracts = re.sub(r'\s[a-zA-Z]+\d+\s|\s\d[a-zA-Z]\d?\s', r' ', abstracts)

# Remove things inside parenthesis
abstracts = re.sub(r'\(.+?\)', r' ', abstracts)
abstracts = re.sub(r'\[.+?\]', r' ', abstracts)
abstracts = re.sub(r'\{.+?\}', r' ', abstracts)

# Remove non-ascii symbols
abstracts = abstracts.encode('ascii', errors='ignore')
abstracts = abstracts.decode("utf-8")

# Remove symbols '!"$#&\()*+/<=>?@[\\]^_`{|}~'
abstracts = abstracts.translate(str.maketrans(
    '', '', r'!"$#&\()*+/<=>?@[\\]^_`{|}~'))

# Remove french abstracts
abstracts = re.sub(r'[^\n]*\s[Ll]es\s[^\n]*', r'', abstracts)
# Remove i.e.
abstracts = abstracts.replace('i.e.', ' ')
abstracts = abstracts.replace('e.g.', ' ')

# Change common abbreviations with dots for without dots: US, UK, GDP
abstracts = re.sub(
    r'([A-Z])\.([A-Z])\.(?:([A-Z])\.)?(?:([A-Z])\.)?(?:([A-Z])\.)?', r'\1\2\3\4\5', abstracts)

# Remove abbreviated letters. Replace ' A. ' ' B. ' ' C. ' + capital letter for period, with no capital letter replace for space
# Delete things like 'A. K. '
abstracts = re.sub(r'\s([A-Z]\.\s){2,3}\s', r' ', abstracts)
abstracts = re.sub(r'\s+', r' ', abstracts)
abstracts = re.sub(r'\s[A-Za-z]\.\s([A-Z])', r'. \1', abstracts)
abstracts = re.sub(r'\s[A-Za-z]\.\s([a-z])', r' \1', abstracts)

# Leaving floats without generating problems
abstracts = re.sub(r'([0-9]+)\.([0-9]+)', r'\1*\2', abstracts)

# Remove standalone letters that are not a, A, i, I
# Delete standalone letters other than A, a, and I
abstracts = re.sub(r'\s[^aAI0-9\W]\s', r' ', abstracts)
# Delete standalone letters other than A, a, and I
abstracts = re.sub(r'\s[^aAI0-9\W]\s', r' ', abstracts)
# Delete standalone letters other than A, a, and I before comma
abstracts = re.sub(r'\s[^aAI0-9\W],', r',', abstracts)
# Delete standalone letters other than A, a, and I before comma
abstracts = re.sub(r'\s[^aAI0-9\W],', r',', abstracts)
abstracts = re.sub(r'\s+', r' ', abstracts)  # Remove double spaces
# Delete capital A if it does not start a sentence
abstracts = re.sub(r'([^.])\sA\s', r'\1 ', abstracts)

# Remove multispaces
abstracts = re.sub(r'\s+', r' ', abstracts)
abstracts = re.sub(r'\s([,.-])', r'\1', abstracts)

# Remove dash not preceded by another dash that is followed by space
abstracts = re.sub(r'([^-])-\s', r'\1 ', abstracts)

# Spellchecker

check = re.findall(r"[\w']+", abstracts)
spell = SpellChecker()
misspelled = spell.unknown(check)

# open file and read the content in a list
with open('dgen/false_flag.txt', 'r') as filehandle:
    false_flag = [current_place.rstrip()
                  for current_place in filehandle.readlines()]

to_remove = [miss for miss in misspelled if miss not in false_flag]

for word in to_remove:
    abstracts = abstracts.replace(' '+word+' ', ' ')
    abstracts = abstracts.replace(' '+word+'.', '.')

abstracts = re.sub(r'\s+', r' ', abstracts)


# Remove multiple periods
abstracts = re.sub(r'\.{2,}(\s?[A-Z])', r'.\1', abstracts)
abstracts = re.sub(r'\.{2,}(\s?[a-z,])', r'\1', abstracts)
abstracts = re.sub(r'\s+', r' ', abstracts)

# Remove multiple commas
abstracts = re.sub(r',{2,3}', r',', abstracts)

# Remove ' ; '
abstracts = abstracts.replace(" ; ", "; ")
abstracts = abstracts.replace(" : ", " ")

# %% Merges

# Merge article with subsequent word
abstracts = re.sub(r'([\.\s]an?)\s|([\.\s]the)\s|([\.\s]this)\s',
                   r'\1\2\3#', abstracts, flags=re.IGNORECASE)

# Merge words with capital letters
abstracts = re.sub(
    r"([A-Z][a-z'-]+)\s([A-Z][a-z'-]+)[\s\.](?:([A-Z][a-z'-]+)[\s\.])?(?:([A-Z][a-z'-]+)[\s\.])?(?:([A-Z][a-z'-]+)[\s\.])?", r'\1#\2#\3#\4#\5', abstracts)
abstracts = re.sub(r'#{2,}', r' ', abstracts)
abstracts = re.sub(r'(#[A-Z][a-z]+)\sof\s', r'\1#of#', abstracts)


def merger(list, string):
    """
    Takes a list of n-grams to merge in a string using #
    """
    regex = re.compile('|'.join(list))
    return regex.sub(lambda match: match.group(0).replace(' ', '#'), string)


# List of things that should be kept together
merge_list = [
    'Nash equilibri', 'Nash bargain', 'least square', 'two stage', 'von Neumann', 'vis a vis'
]

tokens = [i for i in abstracts.replace('.', ' ').lower().split(' ') if i != ""]
grams = [" ".join(x[0]) for i in range(5, 2, -1)
         for x in nltk.FreqDist(nltk.ngrams(tokens, i)).most_common(int(600/(3+i)))]

gramed_abstracts = merger(grams + merge_list, abstracts)

# %% Generating dictionary

sc = gramed_abstracts.split(". ")


def Fil(s):
    if len(s) > 25 and s[0].isupper():
        return True
    else:
        return False


fsc = list(filter(Fil, sc))

maxlen = 40


dictionary = [[] for i in range(maxlen+2)]

for s in fsc:
    wordz = [i for i in s.split(' ') if i != ""]
    dictionary[-1].append(wordz[-1].replace('#', ' ').replace('*', '.'))
    dictionary[-2].append(wordz[-2].replace('#', ' ').replace('*', '.'))
    for i, w in enumerate(wordz):
        if i < maxlen:
            dictionary[i].append(w.replace('#', ' ').replace('*', '.'))


pickle.dump(dictionary, open("dictionary.p", "wb"))
