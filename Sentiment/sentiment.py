# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 11:22:17 2017

@author: Dieter Erben
"""
import pandas as pd, re, collections

comments = pd.read_csv('Comments.csv')
comments = comments.dropna(how='all')

def removeStopwords(wordlist, stopwords):
    return [w for w in wordlist if w not in stopwords]

strengths = comments.top_3_strengths.str.cat()
improv = comments.top_3_improve.str.cat()
other = comments.other_feedback.str.cat()

word_strengths = re.findall('\w+', strengths.lower())
word_improv = re.findall('\w+', improv.lower())
word_other = re.findall('\w+', other.lower())

words_3 = word_strengths + word_improv + word_other

words_3 = removeStopwords(words_3,stopwords)

freqs = collections.Counter(words_3)
word_fre = pd.DataFrame.from_dict(freqs, orient='index').reset_index()
word_fre = word_fre.rename(index=str,columns={'index':'word',0:'freq'})