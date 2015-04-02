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


import index_handler


import re
import itertools
import operator
import math




try:
    import msgpack
    serializer = msgpack
except:
    import json
    serializer = json


from lua_scripts import *


FILTERS = {
           "complete": re.compile("/complete"),
           "pure_tfidf" : re.compile("/pure_tfidf"),
           "title_only" : re.compile("/title_only")
           }
           




class QueryHandler(index_handler.IndexHandler):
    '''
    A class that handles queries upon our INDEX.
    
    It provides functions to deal with boolean retrieval or vector space model retrieval.
        
    '''
    
    def __init__(self, **kwargs):
        index_handler.IndexHandler.__init__(self,  **kwargs)    
        self.limit = kwargs.get('limit',10) 
        self.query = "" 
        self.filters = set()
        self.known_filters = FILTERS
        self.debug = kwargs.get('debug',True)         
        self.res_cache_db = kwargs.get('res_cache_db',None)  
        self.res_cache_exp = kwargs.get('res_cache_exp',100)
        self.serializer = serializer
        self.tfidf_w = kwargs.get('tfidf_w',0.33)
        self.title_w = kwargs.get('title_w',0.33)
        self.posting_w = kwargs.get('posting_w',0.33)
        
        self.use_lua = kwargs.get('use_lua',False)
        if self.use_lua:
            self.exec_single_query_lua = self.db.register_script(exec_single_query_script)
            self.exec_multi_query_lua = self.db.register_script(exec_multi_query_script)
            



    def clear(self):
        self.filters = set()
        self.query = ""         
 
        
    def process_query(self, query, ids=[]):
        ''' entry point for query processing '''
        
        self.clear()
        self.identify_language(query)
        initial_query = query
        self.query = query
        
        if self.debug: print "INITIAL QUERY:", initial_query
        
        self.apply_filters()
        self.clean_stem_query()
                   
        if len(self.query.split()) == 1:             
            res = self.exec_single_query(self.query)    
        elif "title_only" in self.filters:             
            res = self.get_titles(self.query.split())                
        else:     
            if self.use_lua:
                args = self.query.split()
                args.append(self.limit)
                if not len(ids): 
                    return self.exec_multi_query_lua(args=args)
                else:
                    return self.exec_multi_query_lua(keys=ids, args=args)
            else:                                              
                weighted_terms = self.filter_query()  
                if not len(ids): 
                    res = self.vector_retrieval(weighted_terms)
                else:
                    res = self.limited_vector_retrieval(weighted_terms, ids)

        if res:   
            if not self.use_lua:
                external_ids = self.resolve_external_ids([i[0] for i in res])
                res = [(external_ids[i], res[i][1]) for i in xrange(len(res))]
            if self.res_cache_db:
                try:
                    self.res_cache_db.set(initial_query, self.serializer.dumps(res))
                except:
                    raise Exception, "CACHING SEARCH RESULT FAILED, UNREACHABLE DB"    
    
        return res
        



    def apply_filters(self):
        for i in self.known_filters:   
            if re.search(self.known_filters[i], self.query.split()[-1]):
                self.filters.add(i)
                self.query = re.sub(self.known_filters[i],"",self.query)   
                 
        if self.debug: print "WITH FILTERS:", self.filters        
        if not len(self.filters): self.filters.add("complete")
        
        

    def clean_stem_query(self):
        q = ""
        for token in re.sub(r"[.,:;\-!?\"']", " ", self.query).split():
            try: 
                lower = token.lower()
                if self.legal_token(lower):
                    item = self.stem(lower.decode("utf8", "ignore"))
                    if item:
                        q += item + " "      
            except: 
                if self.debug: print "Probable unicode error in stemming query"  , q
                
        self.query = q    
        if self.debug: print "STEMMED QUERY:", self.query



    def filter_query(self):
        ''' 
        Discovers document frequencies of query terms
        Returns a list of tuples of all terms that appear in the index
        Format = (term,df)
        '''
        return self.get_dfs(self.query.split())


    def exec_single_query(self, query):
        ''' optimized for a single query '''
        if self.debug: print "In exec single query"
        q = query.strip()
        if "title_only" in self.filters:
            return [(i,1) for i in self.db.smembers("T%s"%q)]
        elif "pure_tfidf" in self.filters:    
            return self.db.zrevrange(q, 0, self.limit - 1 , withscores=True)
        else:
            if self.use_lua:
                return self.exec_single_query_lua(args=[q,self.limit])
            else:
                res = self.db.zrevrange(q, 0, self.limit - 1 , withscores=True)
                dids = list([i[0] for i in res])
                title_rank = self.get_title_hit([q], dids)
                new_doc_ids = []
                for i, stuff in enumerate(res):
                    new_doc_ids.append( (stuff[0], self.weighted_ranking(tfidf=stuff[1], title=title_rank[i])) )    
                    
                if self.debug: print "RESULTS " ,   sorted(new_doc_ids, key=operator.itemgetter(1), reverse=True)
                
                return sorted(new_doc_ids, key=operator.itemgetter(1), reverse=True)
        

    def get_titles(self, term_list):
        docs = list(self.db.sinter(["T%s"%term for term in term_list]))
        if docs:
            for term in term_list:  
                self.pipe.hmget("&T%s"%term, docs)
                
                
            ranked = []    
            for i, v in enumerate(itertools.izip_longest(*self.flush())): 
                score = 0
                for j in xrange(len(v) - 1):
                    score += 1.0/(float(v[j+1]) - float(v[j]))
                ranked.append((docs[i], score))
                
            return sorted(ranked, key=operator.itemgetter(1), reverse=True)
        
        return []


    def vector_retrieval(self, weighted_terms):
        ''' 
        A function to start vector space model retrieval
        Intersects all docIDs for every term in term_list
        Returns sorted tfidf-weighted docids
        '''
        if self.debug: print "performing vector retrieval on " , weighted_terms
        terms = [i[0] for i in weighted_terms]
        query_key = "".join(terms)

        self.pipe.zinterstore(query_key, dict(weighted_terms))
        self.pipe.zrevrange(query_key, 0, self.limit - 1 , withscores=True)
        
        doc_ids = self.flush()[1]
        if not len(doc_ids):
            return None
        return self.rank_results(doc_ids, terms) 


            
    def limited_vector_retrieval(self, weighted_terms, ids):
        ''' 
        Performs only on specific ids
        '''

        if self.debug: print "performing limited vector retrieval on " , weighted_terms
        terms = [i[0] for i in weighted_terms]
        

        internal_ids = [i for i in self.resolve_external_ids(ids) if i]
        _len = len(internal_ids)
        _tlen = len(terms)

        self.get_cardinality(piped=True)
        for id in internal_ids:
            for term in terms:
                self.pipe.zscore(term, id)
                
        res = self.flush()
        print res
        cardinality = res[0]
        r = res[1:]
        doc_ids = []

        for i, id in enumerate(internal_ids):
            t = 0.0
            for tf in r[i*_tlen:(i*_tlen + _tlen)]:
                if tf is None:
                    continue
                t += tf * float(weighted_terms[i%_tlen][1])
            if t > 0.0:
                doc_ids.append((id, t))


        return self.rank_results(doc_ids, terms) 
            
        

    def rank_results(self, doc_ids, terms):

        if "pure_tfidf" in self.filters:
            if self.debug: print "RESULTS ", doc_ids
            return doc_ids

        elif "complete" in self.filters:
            
            dids = list([i[0] for i in doc_ids])
            
            # rank by title
            title_rank = self.get_title_hit(terms, dids)
            
            # must do proximity ranking
            # get the posting lists
            sh = self.get_postings(terms, dids) # actually, I wanted to name this "shit"


            posting_rank = []

            for v in itertools.izip_longest(*sh):      # decompose list of lists  
                
                try: posting_rank.append( ( self.proximity_rank( self.unfold_postings([ [int(k) for k in j.split(",")] for j in v]) ) ) )
                except: posting_rank.append(0)
                
            new_doc_ids = []
            
            for i, stuff in enumerate(doc_ids):
                new_doc_ids.append( (stuff[0], self.weighted_ranking(tfidf=stuff[1], title=title_rank[i], posting=posting_rank[i] )) )    
                
            if self.debug: print "RESULTS " ,   sorted(new_doc_ids, key=operator.itemgetter(1), reverse=True)
            
            return sorted(new_doc_ids, key=operator.itemgetter(1), reverse=True)
        

    
    


  
            
        

#############################################################################################################
# RANKING FUNCTIONS
#############################################################################################################  


    def weighted_ranking(self, **kwargs):
        '''
        kwargs carry the scores to be multiplied
        '''
        tfidf = kwargs.get('tfidf', 0)
        title = kwargs.get('title', 0)
        posting = kwargs.get('posting', 0)
        
        return tfidf*self.tfidf_w + title*self.title_w + posting*self.posting_w
        


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
        
        # add padding to shorter lists
        biggest = max([len(i) for i in list_of_lists])
        
        for i in list_of_lists:
            while len(i) != biggest:
                i.insert(0,i[0])
                
        
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

 
    def unfold_postings(self, list_of_lists):
        ''' reverses gap encoding '''
        new_list_of_lists = []
        
        for _list in list_of_lists:
            nlist = []
            pos = 0

            for p in _list:
                pos += p
                nlist.append(pos)
                
            new_list_of_lists.append(nlist)

        return new_list_of_lists      
   




    



