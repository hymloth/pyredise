# -*- coding: utf-8 -*-

# code from http://misja.posterous.com/language-detection-with-python-nltk

from nltk.util import trigrams as nltk_trigrams
from nltk.tokenize import word_tokenize as nltk_word_tokenize
from nltk.probability import FreqDist
from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader.api import CorpusReader
from nltk.corpus.reader.util import StreamBackedCorpusView, concat



l_map = {"en": "english",
         "de": "german",
         "fr": "french",
         "es": "spanish",
         "nl": "dutch",
         "ru": "russian"
         }


class LangIdCorpusReader(CorpusReader):
    '''
    LangID corpus reader
    '''
    CorpusView = StreamBackedCorpusView

    def _get_trigram_weight(self, line):
        '''
        Split a line in a trigram and its frequency count
        '''
        data = line.strip().split(' ')
        if len(data) == 2:
            return (data[1], int(data[0]))

    def _read_trigram_block(self, stream):
        '''
        Read a block of trigram frequencies
        '''
        freqs = []
        for i in range(20): # Read 20 lines at a time.
            freqs.append(self._get_trigram_weight(stream.readline()))
        return filter(lambda x: x != None, freqs)

    def freqs(self, fileids=None):
        '''
        Return trigram frequencies for a language from the corpus        
        '''
        return concat([self.CorpusView(path, self._read_trigram_block) 
                       for path in self.abspaths(fileids=fileids)])

class LangDetect(object):
    language_trigrams = {}
    langid            = LazyCorpusLoader('langid', LangIdCorpusReader, r'(?!\.).*\.txt')

    def __init__(self, languages=['nl', 'en', 'fr', 'de', 'es']):
        for lang in languages:
            self.language_trigrams[lang] = FreqDist()
            for f in self.langid.freqs(fileids=lang+"-3grams.txt"):
                self.language_trigrams[lang].inc(f[0], f[1])

    def detect(self, text):
        '''
        Detect the text's language
        '''
        words    = nltk_word_tokenize(text.lower())
        trigrams = {}
        scores   = dict([(lang, 0) for lang in self.language_trigrams.keys()])

        for match in words:
            for trigram in self.get_word_trigrams(match):
                if not trigram in trigrams.keys():
                    trigrams[trigram] = 0
                trigrams[trigram] += 1

        total = sum(trigrams.values())

        for trigram, count in trigrams.items():
            for lang, frequencies in self.language_trigrams.items():
                # normalize and add to the total score
                scores[lang] += (float(frequencies[trigram]) / float(frequencies.N())) * (float(count) / float(total))
        
        
        # special case
        # if all scores are 0.0 we return None
        s = 0.0
        for score in scores.itervalues():
            s += score
        
        if s == 0.0:
            return None

        return l_map[ sorted(scores.items(), key=lambda x: x[1], reverse=True)[0][0] ]
    
    

    def get_word_trigrams(self, match):
        return [''.join(trigram) for trigram in nltk_trigrams(match) if trigram != None]
    
    
    
    
    
    
    
    
    
    
    
if __name__=="__main__":
    import time
    
    texts = [
             "θα πας και θα γαμηθεις μωρη γαμημενη",
     "De snelle bruine vos springt over de luie hond",
     "The quick brown fox jumps over the lazy dog",
     "Le renard brun rapide saute par-dessus le chien paresseux",
     "Der schnelle braune Fuchs springt über den faulen Hund",
     "El rápido zorro marrón salta sobre el perro perezoso",
     "организовывал забастовки и демонстрации, поднимал рабочих на бакинских предприятия",
   ]

    ld = LangDetect()
    
    for text in texts:
        t = time.time()
        print text, "=>", ld.detect(text) , time.time() - t