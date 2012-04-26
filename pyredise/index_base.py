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



class IndexBase(object):
    '''
    A base class representing a "connection" with a redis server ( db )
    
    Attributes:
    
       _max_id : a special key of _dict_key denoting the current maximum docID number
       _set_key : a special key holding our unique docIDs currently present in the corpus
       _docid_map : a special key holding a mapping between docIDs and physical numbers, starting from one
       _slots : a special key denoting some available ids for use ( < _max_id )
       db : the name of redis database (server)
       pipe : redis pipeline object
       

    NOTE: this class (and its descendants) is not thread-safe, thus create a new object every time you need its functionality, per process/thread.
          DO NOT EVER SHARE SUCH AN OBJECT !!!
    

    '''
    
    def __init__(self, **kwargs):
        self._max_id = "$MAXID$"
        self._set_key = "$DOCIDS$"
        self._docid_map = "$DOCIDMAP$"
        self._slots = "$SLOTS$"
        self.db = kwargs.get('db',"") 
        self.pipe = self.db.pipeline()
        
        
    def flush(self):
        ''' executes the pipeline, returns a list of results '''
        return self.pipe.execute()
    
    
    def drop(self):
        ''' drops the entire index '''
        return self.db.flushdb()   
    
    
    def get_cardinality(self, piped=True):
        if piped: self.pipe.scard(self._set_key)
        else: return self.db.scard(self._set_key)
        
        
    def set_max_id(self, value=1, piped=True):
        if piped: self.pipe.incr( self._max_id , value)
        self.db.incr( self._max_id , value)
        
        
    def get_max_id(self, piped=True):
        if piped: self.pipe.get(self._max_id)
        return self.db.get(self._max_id)   
    
    
    def set_slot(self, id, piped=True):
        if piped: self.pipe.sadd(self._slots, id)
        self.db.sadd(self._slots, id)
        
    
    def get_slot(self, piped=True):
        if piped: self.pipe.spop(self._slots)
        return self.db.spop(self._slots)     

    
    def store_doc_id(self, internal_doc_id, external_doc_id, piped=True):
        if piped: 
            self.pipe.hset(self._docid_map, internal_doc_id, external_doc_id)
            self.pipe.hset(self._docid_map, external_doc_id, internal_doc_id)
        else:    
            self.db.hset(self._docid_map, internal_doc_id, external_doc_id)
            self.db.hset(self._docid_map, external_doc_id, internal_doc_id)


    def purge_doc_id(self, internal_doc_id, piped=True):
        external_doc_id = self.db.hget(self._docid_map, internal_doc_id)
        if piped: 
            self.pipe.hdel(self._docid_map, internal_doc_id)
            self.pipe.hdel(self._docid_map, external_doc_id)
        else:    
            self.db.hdel(self._docid_map, internal_doc_id)  
            self.db.hdel(self._docid_map, external_doc_id)  
        self.set_slot(internal_doc_id, piped=piped)    


    def get_next_id(self):
        ''' 
        Decides which is the next id to use. This is either the (_max_id + 1) or an available slot.
        Note that an available slot is always preferred
        '''
        self.get_max_id(piped=True)
        self.get_slot(piped=True)
        res = self.flush()
        if res[1] and res[1] is not None: 
            return res[1]
        else:
            self.set_max_id(value=1,piped=False)
            try:return (int(res[0])+1)
            except: return 1    


    def resolve_external_id(self, doc_id):
        return self.db.hget(self._docid_map, doc_id) 


    def resolve_external_ids(self, doc_ids):
        return self.db.hmget(self._docid_map, doc_ids) 