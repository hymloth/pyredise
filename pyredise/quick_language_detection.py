# -*- coding: utf-8 -*-

try:
    from nltk.corpus import stopwords
except ImportError:
    print '[!] You need to install nltk (http://nltk.org/index.html)'
    
from HTMLParser import HTMLParser



class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
    
    

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()



#----------------------------------------------------------------------
def _calculate_languages_ratios(words):
    """
    Calculate probability of given text to be written in several languages and
    return a dictionary that looks like {'french': 2, 'spanish': 4, 'english': 0}
    
    @param text: Text whose language want to be detected
    @type text: str
    
    @return: Dictionary with languages and unique stopwords seen in analyzed text
    @rtype: dict
    """

    languages_ratios = {}


    # Compute per language included in nltk number of unique stopwords appearing in analyzed text
    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        languages_ratios[language] = len(common_elements) # language "score"

    return languages_ratios


#----------------------------------------------------------------------
def detect_language(words):
    """
    Calculate probability of given text to be written in several languages and
    return the highest scored.
    
    It uses a stopwords based approach, counting how many unique stopwords
    are seen in analyzed text.
    
    @param text: Text whose language want to be detected
    @type text: str
    
    @return: Most scored language guessed
    @rtype: str
    """

    ratios = _calculate_languages_ratios(words)
    most_rated_language = max(ratios, key=ratios.get)
    return most_rated_language


langs = { "english" : set(["a", "b", "c", "d" , "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x","y", "z"]),
          "greek" : set([i.decode("utf-8") for i in ["α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι", "κ", "λ", "μ", "ν", "ξ", "ο", "π", "ρ", "σ", "τ", "υ", "φ" ,"χ", "ψ" ,"ω"]]),
          "russian" : set(["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я"]),
         }
from operator import itemgetter
from collections import defaultdict
def _check_lang(text, max_len=2000):
    
    cnt = defaultdict(int)
    t = strip_tags(text[:max_len])
    if type(t) is str:
        t = t.decode("utf-8","replace")

    
    for lang, letters in langs.iteritems():
        for i in t:
            if i != " " and i in letters:
                cnt[lang] += 1
                
            if cnt[lang] > len(text) / 2:
                return lang
            
    
    for key, v in sorted(cnt.iteritems(), key=itemgetter(1), reverse=True):
        return key


def check_lang(text, max_len=2000):
    t = strip_tags(text[:max_len])
    lang = _check_lang(t)

    if lang == "english":
        words = [i.encode("utf-8","ignore") for i in t.split()]
        lang = detect_language(words)
        
    return lang




if __name__=='__main__':


    
    import time
    
    texts = [
     "The quick brown fox jumps over the lazy dog and fucks the hell out of it",
     "Den raske brune reven hopper over den late hunden og knuller i helvete ut av det",
     "Den hurtige brune ræv hopper over den dovne hund og knepper fanden ud af det",
     "Быстрая коричневая лиса прыгает через ленивую собаку и трахает ад из этого",
     "De snelle bruine vos springt over de luie hond en neukt de hel van te maken",
     "Nopea ruskea kettu hyppää laiskan koiran yli ja vittuile helvettiin siitä",
     "Le rapide renard brun saute par dessus le chien paresseux et baise l'enfer hors de lui",
     "Der schnelle braune Fuchs springt über den faulen Hund und fickt die Hölle aus ihm heraus",
     "A gyors barna róka átugorja a lusta kutyát, és baszik a fenébe is",
     "La volpe veloce salta sul cane pigro e scopa l'inferno fuori di esso",
     "A ligeira raposa marrom ataca o cão preguiçoso e fode o inferno fora dele",
     "El rápido zorro marrón salta sobre el perro perezoso y folla el infierno fuera de él",
     "En snabb brun räv hoppar över den lata hunden och knullar skiten ur det",
     "Hızlı kahverengi tilki tembel köpeğin üstünden atlar ve bunun cehenneme sikikleri",
     "Η γρήγορη καφέ αλεπού πηδάει πάνω από το μεσημέρι και πηδάει την κόλαση έξω από αυτό"
     ]


    
    for text in texts:
        t = time.time()
        print check_lang(text), "=>", text, time.time() - t