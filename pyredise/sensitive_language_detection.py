#!/usr/bin/python2.6.5
# -*- coding: utf-8 -*-
#
# Copyright 2011 Christos Spiliopoulos.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



__authors__ = [
  '"Christos Spiliopoulos" <santos.koniordos@gmail.com>',
]




from collections import defaultdict
from operator import itemgetter
import re


# Simple (non-strict) rule to identify a language
# We keep a dictionary of the form {language_name: set([letters_of_this_language])}
# if the sum of the num of letters in some text are greater than 1>2 of the text's length, we declare it to be of this language

langs = { "english" : set(["a", "b", "c", "d" , "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x","y", "z"]),
          "greek" : set([i.decode("utf-8") for i in ["α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι", "κ", "λ", "μ", "ν", "ξ", "ο", "π", "ρ", "σ", "τ", "υ", "φ" ,"χ", "ψ" ,"ω"]]),
          "russian" : set(["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я"]),
         }


from lang import LangDetect


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
    
    
    
    
'''def check_lang(text, max_len=2000):
    t = strip_tags(text[:max_len])
    ld = LangDetect()
    lang = ld.detect(t)
    if not lang:
        lang = _check_lang(t)
        
    return lang'''
    
def check_lang(text, max_len=2000):
    t = strip_tags(text[:max_len])
    lang = _check_lang(t)

    if lang == "english":
        ld = LangDetect()
        lang = ld.detect(t)
        
        
    return lang
    
    
if __name__=="__main__":
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
        
        
    '''import feedparser
    
    a = feedparser.parse("http://www.koutipandoras.gr/feed")
    
    t = a["entries"][6]
    print check_lang(t["content"][0]["value"])'''