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


import index_handler
from nltk import PorterStemmer
from collections import defaultdict
import stringcheck # super fast, C extension, returns True for alphanumerics only and non stopwords

import re
import json



class CorpusHandler(index_handler.IndexHandler):
    '''    
    A class for dynamic manipulation of our corpus.
    
    It provides methods for document insertion and deletion which, in turn, update all
    relevant INDEX stuff in the background.
    
    '''
    

    
    def __init__(self, **kwargs):
        index_handler.IndexHandler.__init__(self, **kwargs)
        
        self.debug = kwargs.get('debug', False)
        self.stem = PorterStemmer().stem_word
        self.pos = defaultdict(list)
        self.sanitized_text = []
        self.doc_len = 0
        self.delimiter = "!"
        



    def update_pos(self, item, pos):
        try: gap = pos - self.pos[item][-1]
        except: gap = pos
        self.pos[item].append(str(gap))
        


    def content_indexer(self, doc, doc_id,  index=True):

        for i, token in enumerate(re.sub(r"[.,:;!\-?\"']", " ", doc).split()):
            lower = token.lower()
            try: # no encoding errors
                if stringcheck.check(lower):
                    item = self.stem(lower)
                    self.update_pos(item, i)
                    self.sanitized_text.append(item)
            except: 
                if self.debug: print "Probable unicode error"  
                
        self.doc_len = len(self.sanitized_text)  
        
        if index:
            for term, posting in self.pos.iteritems():     
                self.term_add_doc_id(term,  doc_id, float(len(posting))/self.doc_len )   
                self.term_add_doc_id_posting(term,  doc_id, ",".join(posting) )   
                
        else: # remove from index                  
            for term, posting in self.pos.iteritems():     
                self.term_remove_doc_id(term, doc_id)   
                self.term_remove_doc_id_posting(term, doc_id)          
 
              
    def title_indexer(self, title, doc_id, index=True):

        for i, token in enumerate(re.sub(r"[.,:;\-!?\"']", " ", title).split()):
            lower = token.lower()
            try: # no encoding errors
                if stringcheck.check(lower):
                    item = self.stem(lower)
                    
                    if index: 
                        self.term_add_doc_id_title(item, doc_id)
                        self.term_add_doc_id_title_posting(item, doc_id, i)
                    else: 
                        self.term_remove_doc_id_title(item, doc_id)
                        self.term_remove_doc_id_title_posting(item, doc_id)
                    
            except: 
                if self.debug: print "Probable unicode error"  
     
   
             
    def index(self, doc, **kwargs):

        doc_id = str(doc["id"])
        title = doc["title"]
        content = doc["content"]
        
        self.clear()
        
        if not self.doc_id_exists(doc_id):        
            self.add_doc_id(doc_id)
            self.content_indexer(content, doc_id, index=True)
            self.title_indexer(title, doc_id, index=True)
            self.update_cardinality()
            self.flush() # at this point, the INDEX has been updated
            return True                
        else:
            if self.debug: print "This docID already exists in our corpus!"      
            return False
    
    
    
    def extract_features(self, **kwargs):
        '''
        Extracts vital info from current document
        Up to features_limit in length
        Using a tfidf threshold to filter the top of them
        '''
        export_value = kwargs.get('export', json.dumps)
        tfidf_threshold_absolute = kwargs.get('tfidf_threshold_absolute', 0.0000001)
        features_limit = kwargs.get('features_limit', 500)
        rnd = kwargs.get('rnd', 4)
        doc = kwargs.get('doc', None)
        
        # just in case, we chech if we have to re-tokenize the doc

        if not len(self.sanitized_text):
            if doc is None: 
                raise Exception, " No document given !! "

            for i, token in enumerate(re.sub(r"[.,:;!\-?\"']", " ", doc).split()):
                lower = token.lower()
                try: 
                    if stringcheck.check(lower):
                        item = self.stem(lower)
                        self.update_pos(item, i)
                        self.sanitized_text.append(item)
                except: 
                    if self.debug: print "Probable unicode error"  
                                
            self.doc_len = len(self.sanitized_text)    
        
        idfs = [i[1] for i in self.get_dfs(self.sanitized_text)]

        tfidf_tuple_list = []
        adapt_features = []
        
        for i in xrange(min(self.doc_len, len(idfs), features_limit)):
            tfidf = len(self.pos[self.sanitized_text[i]]) * idfs[i] / self.doc_len
            tup = (self.sanitized_text[i], str(round(tfidf , rnd)), i)
            tfidf_tuple_list.append(tup)
            
            if tfidf > tfidf_threshold_absolute: adapt_features.append(tup)
        
        self.clear()
        return export_value(tfidf_tuple_list), export_value(adapt_features)        
        
        
        


    def remove_document(self, doc, **kwargs):
        
        doc_id = str(doc["id"])
        title = doc["title"]
        content = doc["content"]
        
        self.clear()

        if self.doc_id_exists(doc_id):  
            self.remove_doc_id(doc_id)
            self.content_indexer(content, doc_id , index=False) 
            self.title_indexer(title, doc_id, index=True)
            self.update_cardinality(value= -1) # adjust cardinality
            self.flush() # at this point, the INDEX has been updated 
            return True
        else:
            if self.debug: print "Removal Failed: This docID does not exist in our corpus!" 
            return False
 


    def clear(self):
        self.pos = defaultdict(list)
        self.sanitized_text = []
        self.doc_len = 0





    
    
