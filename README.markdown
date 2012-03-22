<p>A simple and fast search engine based on python and redis</p>

<p>Installation</p>
<pre><code>	
$ git clone git@github.com:hymloth/pyredise.git
$ cd pyredise
$ sudo python setup.py install
</code></pre>


<p>
<em>Features:</em>
<ul>
	<li>Dynamic, fast indexing/removal of documents</li>
	<li>Vector space model document retrieval</li>	
	<li>Ranking with tf-idf scores, proximity, title</li>
</ul>	
</p>

<p>
<em>Dependencies:</em>
<ul>
	<li>redis</li>
	<li>redis-py (https://github.com/andymccurdy/redis-py)</li>
	<li>nltk (Natural Language Toolkit)</li>
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

db = = redis.Redis(host='localhost', port=6379, db=0)
    	
cp = corpus_handler.CorpusHandler(db=db)
</code></pre>


<ul>	
	<li>Somehow, you must have some documents to index. Then, 
	you only need a document's id (doc_id), its title and its content.
	</li>
</ul>


<pre><code>
#So you must provide a dictionary with the following format:
doc = {"id":doc_id, "title":doc_title, "content":doc_content}

cp.index( doc )
</code></pre>
		
</p>		


<p>
<em>Filters:</em>
<ul>
	<li>/pure_tfidf : ranking based only on tf-idf scheme </li>
	<li>/title_only : title matching </li>
	<li>/complete : ranking based on tf-idf scheme, proximity and title </li>
</ul>	

<pre><code>
import query_handler
import redis
db = = redis.Redis(host='localhost', port=6379, db=0)
QH = query_handler.QueryHandler(db=db)

# issue some queries, returning a list of tuples such as [(doc_id1, score1), (doc_id2, score2), ...]
print QH.process_query("google security data /pure_tfidf") # ranking only according to tf-idf

print QH.process_query("google security data /complete") # complete

print QH.process_query("google security data /title_only") # search in titles

</code></pre>
</p>	


<p>
For those who haven't noticed, pyredise is named in honor of PY(thon)REDI(s)S(earch)E(ngine)
</p>