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
from nltk.corpus import stopwords



class CorpusHandler(dict, index_handler.IndexHandler):
    '''
    A class for dynamic manipulation of our corpus.
    
    It provides methods for document insertion, deletion, inspection, which, in turn, update all
    relevant INDEX stuff in the background.
    '''
    
    def __init__(self, **kwargs):
        index_handler.IndexHandler.__init__(self, **kwargs)
        self.cnt = 0 # keeps track of positions
        self.debug = kwargs.get('debug',True)
        self.stemmer = PorterStemmer()
        self.stopwords = stopwords.words('english')

    def __setitem__(self, key, value, update_index=False):
        '''
        Overrides the default dict method.
        Modified to update the INDEX, if update_index==True
        ( and acts as a Counter, see collections.Counter in STL )
        '''
        if key in self: # if already seen, just add position in document
            a = self[key]
            a.append(value)
            del self[key]
        else: # first time encountered, update INDEX
            a = []
            a.append(value)
            if update_index: self.update_term_idf(key,value=1) 
        dict.__setitem__(self, key, a)
        
        
    def add_document(self, doc_id, doc_list):
        ''' Updates INDEX with a (split) document, returns success of operation '''
         
        self.clear_all()

        if not self.doc_id_exists(doc_id):
            self.add_doc_id(doc_id) 
            for i in doc_list:
                if i.lower() not in self.stopwords: 
                    self.__setitem__(self.stemmer.stem_word(i.lower()), value = self.cnt, update_index=True) # remember, it involves redis pipelining
                self.cnt += 1
            # update posting list
            length = len(doc_list)    
            for term in self.keys(): 
                term_frequency = float(len(self.__getitem__(term)))/length
                value = str(term_frequency) + ", " +  ", ".join([str(i) for i in self.__getitem__(term)])
                self.term_add_doc_id(term, doc_id, value)

            self.update_cardinality()
            self.flush()
            return True
        else:
            if self.debug: print "This docID already exists in our corpus"       
            return False        
    
   
    def eat_document_spit(self, doc_list):
        '''
         given a split document it returns a string with format: term1:term1-tf-idf:term2:term2-tf_idf:.... 
         NOTE: update_index must be False ( AS TO NOT UPDATE THE "INDEX" )
        '''
        
        self.clear_all()
        
        for i in doc_list:
            if i.lower() not in self.stopwords:
                self.__setitem__(self.stemmer.stem_word(i.lower()), value = 1, update_index=False) # remember, it DOES NOT involve redis pipelining
        idfs = self.piped_get_idf(doc_list)

        length = len(doc_list)
        tf_idf_list = "".join( [(doc_list[i]+ ":" + str( idfs[i]*float( self.__getitem__(doc_list[i]) )/float(length) ) + ":") for i in range(length) ] ) 
        return tf_idf_list 
  
    
    def remove_document(self, doc_id, doc_list):
        ''' removes a document from INDEX , returns success of operation '''

        self.clear_all()

        if self.doc_id_exists(doc_id):        
            for i in set(doc_list): 
                if i.lower() not in self.stopwords:
                    self.term_remove_doc_id(self.stemmer.stem_word(i.lower()), doc_id) # remember, it involves redis pipelining
                    self.update_term_idf(value = -1)
            self.update_cardinality(value = -1) # adjust cardinality
            self.flush() # update all 
            return True
        else:
            if self.debug: print "Removal Failed: This docID does not exist in our corpus" 
            return False



    def clear_all(self):
        self.clear()
        self.cnt = 0


