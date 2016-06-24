"""
collection of semantic distance metrics...
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import collections

from cytoolz import itertoolz
from fuzzywuzzy import fuzz
from Levenshtein import hamming as _hamming, distance as _levenshtein
import numpy as np
from pyemd import emd
from sklearn.metrics import pairwise_distances
from spacy.strings import StringStore

from textacy.compat import str


def word_movers_distance(doc1, doc2, metric='cosine'):
    """
    Measure the semantic distance between two documents using Word Movers Distance.

    Args:
        doc1 (`TextDoc`)
        doc2 (`TextDoc`)
        metric ({'cosine', 'euclidean', 'l1', 'l2', 'manhattan'})

    Returns:
        float: distance between `doc1` and `doc2` in [0.0, 1.0], where smaller
            values correspond to more similar documents
    """
    stringstore = StringStore()

    n = 0
    word_vecs = []
    for word in itertoolz.concatv(doc1.words(), doc2.words()):
        if word.has_vector:
            if stringstore[word.text] - 1 == n:
                word_vecs.append(word.vector)
                n += 1
    distance_mat = pairwise_distances(np.array(word_vecs), metric=metric).astype(np.double)
    distance_mat /= distance_mat.max()

    vec1 = collections.Counter(
        stringstore[word.text] - 1
        for word in doc1.words()
        if word.has_vector)
    vec1 = np.array([vec1[word_idx] for word_idx in range(len(stringstore))]).astype(np.double)
    vec1 /= vec1.sum()  # normalize word counts

    vec2 = collections.Counter(
        stringstore[word.text] - 1
        for word in doc2.words()
        if word.has_vector)
    vec2 = np.array([vec2[word_idx] for word_idx in range(len(stringstore))]).astype(np.double)
    vec2 /= vec2.sum()  # normalize word counts

    return emd(vec1, vec2, distance_mat)


def jaccard_distance(str1, str2, fuzzy_match=False, match_threshold=80):
    """
    Measure the semantic distance between two strings or sequences of strings
    using Jaccard distance, with optional fuzzy matching of not-identical pairs
    when `str1` and `str2` are sequences of strings.

    Args:
        str1 (str or sequence(str))
        str2 (str or sequence(str)): if str, both inputs are treated as sequences
            of *characters*, in which case fuzzy matching is not permitted
        fuzzy_match (bool): if True, allow for fuzzy matching in addition to the
            usual identical matching of pairs between input vectors
        match_threshold (int): value in the interval [0, 100]; fuzzy comparisons
            with a score >= this value will be considered matches

    Returns:
        float: distance between `str1` and `str2` in [0.0, 1.0], where smaller
            values correspond to more similar strings or sequences of strings
    """
    set1 = set(str1)
    set2 = set(str2)
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    if fuzzy_match is True and not isinstance(str1, str) and not isinstance(str2, str):
        for item1 in set1.difference(set2):
            if max(fuzz.token_sort_ratio(item1, item2) for item2 in set2) >= match_threshold:
                intersection += 1
        for item2 in set2.difference(set1):
            if max(fuzz.token_sort_ratio(item2, item1) for item1 in set1) >= match_threshold:
                intersection += 1

    return 1.0 - (intersection / union)


def hamming_distance(str1, str2, normalize=False):
    """
    Measure the distance between two strings using Hamming distance, which simply
    gives the number of characters in the strings that are different, i.e. the
    number of substitution edits needed to change one string into the other.

    Args:
        str1 (str)
        str2 (str)
        normalize (bool): if True, divide Hamming distance by the total number of
            characters in the longest string; otherwise leave the distance as-is

    Returns:
        int or float: if `normalize` is False, return an int, otherwise return
            a float in the interval [0.0, 1.0], where smaller values correspond
            to more similar strings

    .. note:: This is a *modified* Hamming distance in that it permits strings of
        different lengths to be compared,
    """
    len_str1 = len(str1)
    len_str2 = len(str2)
    if len_str1 == len_str2:
        distance = _hamming(str1, str2)
    else:
        # make sure str1 is as long as or longer than str2
        if len_str2 > len_str1:
            str1, str2 = str2, str1
            len_str1, len_str2 = len_str2, len_str1
        # distance is # of different chars + difference in str lengths
        distance = len_str1 - len_str2
        distance += _hamming(str1[:len_str2], str2)
    if normalize is True:
        distance /= len_str1
    return distance


def levenshtein_distance(str1, str2, normalize=False):
    """
    Measure the distance between two strings using Levenshtein distance, which
    gives the minimum number of character insertions, deletions, and substitutions
    needed to change one string into the other.

    Args:
        str1 (str)
        str2 (str)
        normalize (bool): if True, divide Levenshtein distance by the total number
            of characters in the longest string; otherwise leave the distance as-is

    Returns:
        int or float: if `normalize` is False, return an int, otherwise return
            a float in the interval [0.0, 1.0], where smaller values correspond
            to more similar strings
    """
    distance = _levenshtein(str1, str2)
    if normalize is True:
        distance /= max(len(str1), len(str2))
    return distance
