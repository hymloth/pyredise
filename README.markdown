<p>A simple and fast search engine based on python and redis</p>

<p>
Features:

	<li>Dynamic insertion, deletion and inspection of documents in corpus, with automatic tf-idf handling</li>
	<li>Boolean queries interface for tf-idf weighted document retrieval</li>
</p>

<p>
Dependencies:

	<li>redis 2.2.12</li>
	<li>redis-py (https://github.com/andymccurdy/redis-py)</li>
</p>	
	
Instructions:

<p>	
	<li>You must have redis installed and configured properly</li>

	<li>As a starting point, take a look at corpus_handler.py</li>
	
	<li>Initialize it with a python-redis instance:</li>

<pre><code>	
import redis
import corpus_handler

db=redis.Redis(host='localhost', port=6379, db=0)
kwargs = {}
kwargs["db"] = redis.Redis(host='localhost', port=6379, db=0)
    	
cp = corpus_handler.CorpusHandler(**kwargs)
</code></pre>


	
	<li>Somehow, you must have some documents to feed the INDEX. Assuming that you solved this problem ( use simple files or an SQL server or xml feeds or...), you only need a document's id (doc_id) and its content to index a document</li>

<pre><code>
cp.add_document( doc_id , content.split() )
</code></pre>
		
</p>		
	