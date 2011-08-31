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


import index_base
import math
import re
from pyparser import *
import query_base
from operator import itemgetter



def sort_by_attr(t, attr, reverse = True):
    '''sorts a list of dicts by given attribute, returns a list'''
    return sorted(t, key=itemgetter('%s'%attr), cmp = lambda x, y:cmp(int(x),int(y)), reverse=reverse)


class QueryHandler(query_base.QueryBase):
    '''
    A class that handles queries upon our INDEX.
    
    Attributes :
    
        limit : at most results to return
        query_dict : helper dict containing terms : terms-idf
        temporary_keys : list holding temporary keys to delete later
        debug : whether to print messages for debugging purposes
        
    '''
    
    def __init__(self, **kwargs):
        query_base.QueryBase.__init__(self,  **kwargs)  



    def exec_single_query(self, query):
        ''' optimized for a single query '''
        if self.debug: print "In exec single query"
        return self.db.zrevrange(query, 0, self.limit - 1 , withscores=True)
    
#############################################################################################################
# VECTOR RETRIEVAL 
#############################################################################################################

    def vector_retrieval(self, term_list):
        ''' 
        A function to perform vector space model retrieval
        Intersects all docIDs for every term in term_list
        Calculates and sums tf-idf for every such docID
        Performs an additional proximity ranking and sums it with tf-idf
        '''
        if self.debug: print "performing vector retrieval on " , term_list

        query_key = "".join([term for term in term_list]) 
        self.temporary_keys.append(query_key)
        
        term_dicts = self.get_terms_from_cache(term_list)  
        
        #to perform intersection we must sort term_dicts by length
        term_dicts_sorted = sort_by_attr(term_dicts, "DF", reverse=False)   
       
        mysets = (set(x.keys()) for x in term_dicts_sorted)
        
        doc_ids = reduce(lambda a,b: a.intersection(b), mysets)
        
        try: doc_ids.remove("DF")
        except: pass
        
        final_score_dict = dict((k,0.0) for k in doc_ids)
        

        # process dictionaries (redis hashes) and split tfs and positions    
        pos_dict = {}
        for j in xrange(0,len(term_dicts)):
            temp_dict = {}
            for k in term_dicts[j]:
                if k in doc_ids:
                    spl = term_dicts[j][k].split(",")
                    temp_dict[k] = float(spl[0]) * self.query_dict[term_list[j]]    # calculate tf-idf for doc_id k on the fly
                    final_score_dict[k] += temp_dict[k]    
                    try:
                        pos_dict[k].append([int(i) for i in spl[1:]])   # also screen positions
                    except: 
                        pos_dict[k] = [[int(i) for i in spl[1:]]]
  
        # do proximity ranking, if we must
        if self.query_dict["$FILTER"] == "full_search":
            for k in pos_dict:
                final_score_dict[k] *= self.proximity_rank(pos_dict[k])
                    
        self.query_dict[query_key] = sorted(final_score_dict.iteritems(), key=itemgetter(1), reverse=True)
            
        return query_key
    
       
#############################################################################################################
# BASIC BOOLEAN OPERATIONS , INTERSECTION, UNION, DIFFERENCE
#############################################################################################################

    def intersect(self, term_list):
        ''' 
        Intersects all docIDs for every term in term_list
        '''
        if self.debug: print "performing intersection on " , term_list
 
        doc_ids = reduce(lambda a,b: a.intersection(b), self.get_terms_sets(term_list, sorted = True))

        return self.manage_set_operation(term_list, doc_ids)


            
    def union(self, term_list):
        ''' 
        Unions all docIDs for every term in term_list
        '''
        if self.debug: print "performing union on " , term_list 

        doc_ids = reduce(lambda a,b: a.union(b), self.get_terms_sets(term_list))

        return self.manage_set_operation(term_list, doc_ids)



    def diff(self, term_list):
        ''' 
        Provides difference operation on all docIDs for every term in term_list
        '''
        if self.debug: print "performing difference on " , term_list          
        
        self.pipe.smembers(self._set_key)   # get all docIDs

        doc_ids = reduce(lambda a,b: a.union(b),  self.get_terms_sets(term_list))

        return self.manage_set_operation(term_list, doc_ids)
 



    def remove_temp_keys(self):
        ''' deletes those temporary keys so far '''
        for key in self.temporary_keys:
            if self.debug : print "deleting key: " , key
            self.pipe.delete(key)
        self.flush()
        

#############################################################################################################
# RANKING FUNCTIONS
#############################################################################################################  

     
    def proximity_rank(self, list_of_lists):  
        '''
        A ranking function that calculates a score for words' proximity.
        This score is defined as the sum of 1/Prox for every continuous matches of them.
        Prox is a number indicating how close the words are
        
        example: for words A and B, their postings are [1,4,10] and [2,6,17]
        
                 then score = 1/(2 - 1 + 1) + 1/(6 - 4 + 1) + 1/(17 - 10 + 1)
        '''
        def sub(*args):
            return reduce(lambda x, y: y-x, args )
        
        _len = len(list_of_lists) - 1
        
        score = 0
       
        while True: 
            
            try:
                # get all heads
                _tuple = [i.pop(0) for i in list_of_lists]
            
                for i in xrange(1,len(_tuple)):
                    # ensure we keep order of postings
                    while _tuple[i] - _tuple[i-1] < 0:
                        _tuple.pop(i)
                        _tuple.insert(i, list_of_lists[i].pop(0))
                
                score_vector =  [i - _len for i in map(sub, _tuple)]       
                #print _tuple  , score_vector[-1] - score_vector[0] - _len + 1
                score += 1.0/(score_vector[-1] - score_vector[0] - _len + 1) # ensure no division with 0

            except: break
        
        return score


#############################################################################################################
# HELPER FUNCTIONS
#############################################################################################################  

    def get_terms_from_cache(self, term_list):
        '''
        Helper piped function to fetch dictionaries of term stuff from cache
        '''
        for term in term_list:
            self.pipe.hgetall(self.stemmer.stem_word(term.lower()))
        #return self.flush()
        # hmmm, well , provide some fault tolerance, still seek through the rest if a term or more was not found
        return [ i for i in self.flush() if i!={}]
 

    def get_terms_sets(self, term_list, sorted=False):
        '''
        Helper piped function to fetch dictionaries of term stuff from cache
        However, sometimes term_list contains temporary query keys from previous calculations
        We have to resolve this issue, by additional checks
        Used only in the boolean model
        '''
        for term in term_list:
            self.pipe.hgetall(term)
        
        res = self.flush()
        set_list = []  
          
        for i in range(0,len(res)):
            if res[i] == []:     # either not present in cache or a mixed query key in self.query_dict
                try: set_list.append(self.query_dict[term_list[i]]) 
                except: set_list.append(set())      # boolean queries MUST BE strict
            else:
                try: 
                    _set = set()
                    _set.update(res[i].keys())     # from dict
                    set_list.append(_set)
                except:
                    set_list.append(res[i])       # from set      
                 
        if sorted:  set_list.sort(key=len)  # sort by length, yeah
                  
        return set_list 


    def manage_set_operation(self, term_list, doc_ids):
        '''
        Helper function that constructs a temporary key, updates self.temporary_keys,
        adds it in self.query_dict for further use and returns it
        '''
        try: doc_ids.remove("DF")
        except: pass
        
        query_key = "".join([term for term in term_list]) 
        self.temporary_keys.append(query_key)   
        # also add it to self.query_dict for possible later use
        self.query_dict[query_key] = doc_ids

        return query_key       