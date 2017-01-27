import mrjob
from mrjob.job import MRJob
import re

class MRMostUsedWord(MRJob):
    def mapper(self, _, line):
        words = re.findall(r"[\w\']+", line)
        for i in words:
            yield (i.lower(), 1)
    
    def combiner(self, word, count):
        yield (word, sum(count))
    
    def reducer(self, word, count):
        yield (word, sum(count))

if __name__ == '__main__':
    MRMostUsedWord.run()