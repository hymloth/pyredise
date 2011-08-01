#!/usr/bin/python2.6.5
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



class QueryHandler(index_base.IndexBase):
    '''
    A class that handles queries upon our INDEX.
    
    Attributes :
    
        limit : at most results to return
        query_dict : helper dict containing terms : terms-idf
        temporary_keys : list holding temporary keys to delete later
        debug : whether to print messages for debugging purposes
        
    '''
    
    def __init__(self, **kwargs):
        index_base.IndexBase.__init__(self,  **kwargs)    
        self.limit = kwargs.get('limit',10) 
        self.query_dict = {} 
        self.temporary_keys = []
        self.debug = kwargs.get('debug',True) 

    
    def process_query(self, query):
        ''' entry point for query processing '''
       
        if len(query.split()) == 1: return self.exec_single_query(query)    # first case, single query
        
        query = self.transform_into_boolean_query(query)
        self.query_dict = self.filter_query(query)   
        try:
            # we can now parse the query
            # SEE pyparser.py to understand more
            evalStack = (searchExpr + stringEnd).parseString(query)[0]
            if self.debug: print "Eval stack:", evalStack, type(evalStack)
            evalExpr = evalStack.generateSetExpression()    # GENERATE QUERY
            if self.debug: print "Eval expr:", evalExpr
            
            result_key = eval(evalExpr)

            # REAP THE RESULTS
            self.pipe.zrevrange(result_key, 0, self.limit -1, withscores=True) # bring by index, at most "limit" of them, in descending order
            res =  self.flush() 
            self.remove_temp_keys() # REMOVE TEMPORARY KEYS FROM THE INDEX ( involves flush() )            
                  
            return res[-1] # the result lies in the last item !!
        except ParseException, pe:
            if self.debug: print "Search string with no boolean stuff"
            return None


    def transform_into_boolean_query(self, query):
        ''' adds an AND to terms if not any'''
        def add_and(term1, term2):
            if term1.split()[-1] not in ["and", "or", "not"] and term2 not in ["and", "or", "not"]:
                return term1 + " and " + term2
            else:
                return term1 + " " + term2
            
        if self.debug: print "transform_into_boolean_query -->", reduce(add_and,query.split()) 
        return reduce(add_and,query.split())     

 
    def exec_single_query(self, query):
        ''' optimized for a single query '''
        if self.debug: print "In exec single query"
        return self.db.zrevrange(query, 0, self.limit - 1 , withscores=True)
    

    def filter_query(self,query):
        ''' 
            Returns a dictionary like term: term:{idf:0.34} or term:None if term not in our INDEX
        '''
        # first, remove all boolean operator and fix whitespaces and parenthesis
        filtered_query_list = [i.strip().replace("(","").replace(")","") for i in re.split(' +and +| +or +|not +', query) if i]
        if self.debug: print "FILTERED QUERY LIST : " , filtered_query_list
        
        # let the pipelining begin
        self.pipe.hget(self._dict_key, "CCAARRDDIINNAALLIITTYY")
        for term in filtered_query_list:  
            self.pipe.hget(self._dict_key, term) 
        
        res = self.flush()  # gather every result of the pipeline
        # res[0] is cardinality and the rest the idfs of every term
        for i in range(1, len(res)):
            if res[i]: self.query_dict[filtered_query_list[i-1]] = math.log( float(res[0])/float(res[i])) #dict( ( ("idf", math.log( float(res[0])/float(res[i])) ), ) ) 
            else: self.query_dict[filtered_query_list[i-1]] = None
        if self.debug: print "QUERY DICT :" , self.query_dict
        return self.query_dict   


    def intersect(self, term_list):
        ''' 
        Intersects all sorted sets for every term in kwargs
        NOTE: no need for optimization, redis takes care of this
        '''
        if self.debug: print "performing intersection on " , term_list
        # TODO dangerous, must ensure no duplicate query_keys , idea, every object has a unique id, append it on the query key
        query_key = "".join([term for term in term_list])   # construct a temporary key for zunionstore 
        self.temporary_keys.append(query_key)   # append it for deletion later
        # also add it to self.query_dict for possible later use
        self.query_dict[query_key] = 1#dict( ( ("idf", 1), ("action", "delete_from_cache")   )  )
        # check to see if any term does not exist in our INDEX
        # in such a case, return the query_key without performing any intersections
        for key in term_list:
            if self.query_dict[key] == None:
                if self.debug: print "empty set"
                return query_key
            
        temp_dict = dict((k,self.query_dict[k]) for k in term_list if k in self.query_dict) # construct a sub-set of self.query_dict for the terms in term_list 
        self.pipe.zinterstore(query_key, temp_dict) # intersect all the sorted sets for every query term, with weight multiplication (tf-idf on the fly)
        
        return query_key    # return query_key, it might be used for another operation
            


    def union(self, term_list):
        ''' 
        Unions all sorted sets for every term in kwargs
        '''
        if self.debug: print "performing union on " , term_list
        
        query_key = "".join([term for term in term_list])   # construct a temporary key for zunionstore
        self.temporary_keys.append(query_key)
        self.query_dict[query_key] = 1   # also add it to self.query_dict for possible later use
        temp_dict = dict((k,self.query_dict[k]) for k in term_list if k in self.query_dict) # construct a sub-set of self.query_dict for the terms in term_list
        
        self.pipe.zunionstore(query_key, temp_dict) # union all the sorted sets for every query term, with weight multiplication (tf-idf on the fly)
        
        return query_key    # return query_key, it might be used for another operation


    def diff(self, term):
        ''' 
        Here, we must calculate the difference of two sorted sets. THIS IS NOT SUPPORTED DIRECTLY BY REDIS, so let the hack begin..
        '''
        if self.debug: print "performing difference on " , term
        diff_key = term + "diffkey"
        members = self.db.zrange(term, 0, -1, withscores=False)
        print "members : " , members
        for m in members:
            self.db.sadd(diff_key, m)
            
        difference = self.db.sdiff("DDOOCCIIDDSS", diff_key)    
        print "difference " ,     difference
        self.db.delete(diff_key)
        for diff in difference:
            self.db.zadd(diff_key, diff, 1)    
            
        self.temporary_keys.append(diff_key)
        self.query_dict[diff_key] = 1      
               
        return diff_key    


    def remove_temp_keys(self):
        ''' deletes those temporary keys so far '''
        for key in self.temporary_keys:
            if self.debug : print "deleting key: " , key
            self.pipe.delete(key)
        self.flush()
