<p>A simple and fast search engine based on python and redis</p>

<p>
<em>Features:</em>
<ul>
	<li>Dynamic insertion, deletion and inspection of documents in corpus, with automatic tf-idf handling</li>
	<li>Vector space model document retrieval with a simple proximity ranking</li>	
	<li>Boolean queries interface</li>
</ul>	
</p>

<p>
<em>Dependencies:</em>
<ul>
	<li>redis 2.2.12</li>
	<li>redis-py (https://github.com/andymccurdy/redis-py)</li>
	<li>nltk (Natural Language Toolkit)</li>
</ul>	
</p>	

<p>
<em>TODO:</em>
<ul>
	<li>add more filters for more specialized queries (by date, by external ranking etc..)</li>
</ul>	
</p>
	
<em>Instructions:</em>

<p>	
<ul>

	<li>You must have redis installed and configured properly</li>

	<li>As a starting point, take a look at corpus_handler.py</li>
	
	<li>Initialize it with a python-redis instance:</li>
</ul>

<pre><code>	
import redis
import corpus_handler

db=redis.Redis(host='localhost', port=6379, db=0)
kwargs = {}
kwargs["db"] = redis.Redis(host='localhost', port=6379, db=0)
    	
cp = corpus_handler.CorpusHandler(**kwargs)
</code></pre>


<ul>	
	<li>Somehow, you must have some documents to feed the INDEX. Assuming that you solved this problem ( use simple files or an SQL server or xml feeds or...), you only need a document's id (doc_id) and its content to index a document</li>
</ul>


<pre><code>
cp.add_document( doc_id , content.split() )
</code></pre>
		
</p>		


<p>
<em>Filters:</em>
<ul>
	<li>/pure_tfidf : ranking based only on tf-idf scheme </li>
</ul>	

<pre><code>
import query_handler
QH = query_handler.QueryHandler(**kwargs) # for kwargs see above or in __init__

# issue some queries
print QH.process_query("google security data /pure_tfidf") # ranking only according to tf-idf

print QH.process_query("google security data") # tf-idf plus proximity ranking

print QH.process_query("google and security or data") # a boolean query

</code></pre>
</p>	