#!/usr/bin/python

'''
An old version was created by Dr. Yuhang Wang

'''

import mrjob
from mrjob.job import MRJob
import re

WORD_RE = re.compile(r"\b[\w']+\b")#regular expression

class BigramCount(MRJob):
    OUTPUT_PROTOCOL = mrjob.protocol.RawProtocol

    def mapper(self, _, line):
        words = WORD_RE.findall(line)
        for i in xrange(len(words) - 1):
            bigram = words[i] + ' ' + words[i + 1]
            counts = 1
            yield (bigram.lower(), counts)
 
    def combiner(self, bigram, counts):
        yield (bigram, sum(counts))
 
    def reducer(self, bigram, counts):
        yield (bigram, str(sum(counts)))

if __name__ == '__main__':
    BigramCount.run()