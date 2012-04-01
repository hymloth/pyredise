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



import index_base
import math
    

class IndexHandler(index_base.IndexBase):
    '''
    This class provides basic methods for INDEX manipulation
    '''
    
    def __init__(self, **kwargs):
        index_base.IndexBase.__init__(self, **kwargs)
        
    
    def update_cardinality(self, value = 1):
        self.pipe.incr( self._cardinality_key ,value )

        
    def term_add_doc_id(self, term, value, score):
        '''
	    value is "doc_id + ! + posting
	    score is tf
	    '''
        self.pipe.zadd(term, value, score)   
        
        
    def term_remove_doc_id(self, term, value):
        self.pipe.zrem(term, value) 
        
          
    def term_add_doc_id_posting(self, term, doc_id, posting):
        self.pipe.hset("&%s"%term, doc_id, posting)      
        
            
    def term_remove_doc_id_posting(self, term, doc_id):
        self.pipe.hdel("&%s"%term, doc_id)               


    def term_add_doc_id_title_posting(self, term, doc_id, posting):
        self.pipe.hset("&T%s"%term, doc_id, posting)      
        
            
    def term_remove_doc_id_title_posting(self, term, doc_id):
        self.pipe.hdel("&T%s"%term, doc_id)    


    def term_add_doc_id_title(self, term, doc_id):
        self.pipe.sadd("T%s"%term, doc_id)      
        
        
    def term_remove_doc_id_title(self, term, doc_id):
        self.pipe.srem("T%s"%term, doc_id)  


    def add_doc_id(self, doc_id):
        self.pipe.sadd(self._set_key, doc_id)   
        
        
    def remove_doc_id(self, doc_id):
        self.pipe.srem(self._set_key, doc_id)    


    def doc_id_exists(self, doc_id):
        return self.db.sismember(self._set_key, doc_id) 
        
                
    def get_term_df(self, term): 
        try: return math.log(  float(self.db.get(self._cardinality_key)) / (float(self.db.zcard(term))) )
        except: return False
    
      
    def get_dfs(self, term_list):
        self.pipe.get(self._cardinality_key)
        for term in term_list:  
            self.pipe.zcard(term)
        
        res = self.flush()
        # res[0] is cardinality and the rest are the dfs of every term   
        s = []
        cardinality = float(res[0])
        for i, item in enumerate(res[1:]):
            if item not in [None,0] : s.append( (term_list[i], math.log( cardinality/float(item))  ) )
 
        return s    

    
    
    def get_postings(self, term_list, docids_list):
        for term in term_list:  
            self.pipe.hmget("&%s"%term, docids_list)
        
        return self.flush()
    
  
    
    def get_title_hit(self, term_list, doc_ids_list):     
        _len = len(doc_ids_list)
        _sub_len = len(term_list)
        
        for term in term_list:
            for did in doc_ids_list:
                self.pipe.sismember("T%s"%term, did)

        res = self.flush()

        rank = []
        for i , v in enumerate(doc_ids_list):
            cnt = i
            sum = 0
            for i in xrange(_sub_len):
                sum += int(res[cnt])
                cnt += _len
            rank.append(sum)
            
        return rank    
            
            
            
            
            
            
            
            
            
            
            
            
            