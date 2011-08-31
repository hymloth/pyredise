# -*- coding: utf-8 -*-
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

from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords


boolean_pattern = re.compile(" +and +| +or +|not +")


class QueryBase(index_base.IndexBase):
    '''
    A base class that provides basic query preprocessing/functionality .
    
    Attributes :
    
        limit : at most results to return
        query_dict : helper dict containing terms : terms-idf
        temporary_keys : list holding temporary keys to delete later
	    filters : dictionary holding regexes to categorize query 
        debug : whether to print messages for debugging purposes
        stemmer : Porter stemmer for words preprocessing
        stopwords : common words to exclude from indexing
    '''
    
    def __init__(self, **kwargs):
        index_base.IndexBase.__init__(self,  **kwargs)    
        self.limit = kwargs.get('limit',10) 
        self.query_dict = {} 
        self.temporary_keys = []
        self.debug = kwargs.get('debug',True) 
        self.filters = self.init_filters()
        self.stemmer = PorterStemmer()
        
        _stopwords = stopwords.words('english')
        self.stopwords = [i for i in _stopwords if i not in ["and", "or", "not"]]


    def init_filters(self):
        ''' initializes filters for specialized queries '''
        
        adict = {}
        adict["pure_tfidf"] = re.compile("/pure_tfidf")
        return adict

    
    def process_query(self, query):
        ''' entry point for query processing '''
        
        self.clear()
        
        if self.debug: print "INITIAL QUERY:", query
        query = self.categorize_query(query)
        query = self.stem_query(query)
        if self.debug: print "STEMMED QUERY:", query
        if self.debug: print "QUERY DICT:", self.query_dict
           
        if len(query.split()) == 1: return self.exec_single_query(query)    # first case, single query
            
        expr = ""
        query = self.transform_into_boolean_query(query)    # needed anyway for filter_query
        
        if self.query_dict["$TYPE"] == "boolean_model":
            try:
                expr = self.generate_boolean_expression(query)
            except:
                return "MALFORMED BOOLEAN QUERY"
        else:
            self.query_dict = self.filter_query(query)   
            expr = self.generate_vector_expression(query)
        
        if self.debug: print "EXPRESSION: " , expr
        
        result = eval(expr)    
        
        return self.query_dict[result]



    def categorize_query(self, query):
        '''
        recognizes filters in the query (if any)
        it updates self.query_dict["$FILTER"] value, indicating the filter type to be used later
        also updates self.query_dict["$TYPE"], distinguishing between boolean and vector models
        returns the query itself without the filter special expression
        '''
        # determine basic type of query
        if re.search(boolean_pattern, query): self.query_dict["$TYPE"] = "boolean_model"	
        else: self.query_dict["$TYPE"] = "vector_model"
        
        # determine filters if any (notice that we can handle only a filter at a time)
        self.query_dict["$FILTER"] = "full_search"
        for i in self.filters:   
            if re.search(self.filters[i], query.split()[-1]):
                self.query_dict["$FILTER"] = i
                query = re.sub(self.filters[i]," ",query)    
                break
        
        return query


    def stem_query(self, query):
        '''
        Not to mention how vital stemming is :)
        '''
        return " ".join([self.stemmer.stem_word(i.lower()) for i in query.split() if i not in self.stopwords])


    def transform_into_boolean_query(self, query):
        ''' adds an AND to terms if not any'''
        def add_and(term1, term2):
            if term1.split()[-1] not in ["and", "or", "not"] and term2 not in ["and", "or", "not"]:
                return term1 + " and " + term2
            elif term2 == "not" and term1.split()[-1] not in ["and", "or", "not"]:
                return term1 + " and " + term2
            else:
                return term1 + " " + term2
            
        if self.debug: print "transform_into_boolean_query -->", reduce(add_and,query.split()) 
        return reduce(add_and,query.split())     
    
    
    def generate_boolean_expression(self, query):
        '''
        given a boolean query, this function parses it and generates a boolean
        expression to be evaluated
        '''

        # SEE pyparser.py to understand more
        evalStack = (searchExpr + stringEnd).parseString(query)[0]
        evalExpr = evalStack.generateSetExpression()
  
        return evalExpr


    def generate_vector_expression(self, query):
        '''
        Just generates a simple expression for the vector model
        '''
        return "self.vector_retrieval(%s)" % [ i for i in query.split() if i != "and"]


    def filter_query(self,query):
        ''' 
            Returns a dictionary like term: term:{idf:0.34} or term:None if term not in our INDEX
        '''
        # first, remove all boolean operators and fix whitespaces and parenthesis
        filtered_query_list = [i.strip().replace("(","").replace(")","") for i in re.split(' +and +| +or +|not +', query) if i]
        if self.debug: print "FILTERED QUERY LIST : " , filtered_query_list
        
        self.pipe.get(self._cardinality_key)
        for term in filtered_query_list:  
            self.pipe.hget(term, "DF") 
        
        res = self.flush()  
        # res[0] is cardinality and the rest the idfs of every term
        for i in range(1, len(res)):
            if res[i]: self.query_dict[filtered_query_list[i-1]] = math.log( float(res[0])/float(res[i])) 
            else: self.query_dict[filtered_query_list[i-1]] = None
        if self.debug: print "QUERY DICT :" , self.query_dict
        return self.query_dict   


    def clear(self):
        ''' clears self.query_dict and self.temporary_keys '''
        self.query_dict = {} 
        self.temporary_keys = []
        
