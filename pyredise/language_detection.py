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
          "greek" : set([i.decode("utf-8") for i in ["α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι", "κ", "λ", "μ", "ν", "ξ", "ο", "π", "ρ", "σ", "τ", "υ", "φ" ,"χ", "ψ" ,"ω"]])
         }


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



def check_lang(text, max_len=2000):
    
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

