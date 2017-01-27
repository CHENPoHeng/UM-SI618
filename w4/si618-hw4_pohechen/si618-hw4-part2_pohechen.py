import mrjob
from mrjob.job import MRJob
from mrjob.step import MRJobStep
import re

class MRMostUsedWord(MRJob):
    def mapper_get_words(self, _, line):
        words = re.findall(r"[\w\']+", line)
        for i in words:
            yield (i.lower(), 1)
    
    def combiner_count_words(self, word, count):
        yield (word, sum(count))
    
    def reducer_count_words(self, word, count):
        yield None, (word, sum(count))

    def reducer_find_max_word(self, _, word_count_pairs):
        yield sorted(word_count_pairs, key = lambda x:x[1], reverse=True)[0]

    def steps(self):
        return [
            MRJobStep(mapper = self.mapper_get_words,
                   combiner = self.combiner_count_words,
                   reducer = self.reducer_count_words),
            MRJobStep(reducer = self.reducer_find_max_word) 
            ]    

if __name__ == '__main__':
    MRMostUsedWord.run()