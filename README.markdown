<p>A simple and fast search engine based on python and redis</p>

<p>
Features:

	- Dynamic insertion, deletion and inspection of documents in corpus, with automatic tf-idf handling
	- Boolean queries interface for tf-idf weighted document retrieval
</p>

<p>
Dependencies:

	--- redis 2.2.12
	--- redis-py (https://github.com/andymccurdy/redis-py)
</p>	
	
Instructions:

<p>	
	--- You must have redis installed and configured properly.

	--- As a starting point, take a look at corpus_handler.py
	
	--- Initialize it with a python-redis instance:

<pre><code>	
db=redis.Redis(host='localhost', port=6379, db=0)
kwargs = {}
kwargs["db"] = redis.Redis(host='localhost', port=6379, db=0)
    	
cp = corpus_handler.CorpusHandler(**kwargs)
</code></pre>


	
	--- Somehow, you must have some documents to feed the INDEX. Assuming that you solved this problem ( use simple files or an SQL server or xml feeds or...), you only need a document's id (doc_id) and its content to index a document

<pre><code>
cp.add_document( doc_id , content.split() )
</code></pre>
		
</p>		
	