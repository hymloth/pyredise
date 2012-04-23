<p>A simple and fast search engine based on python and redis</p>
<br>
<p><b>Installation</b></p>
<pre><code>	
sudo pip install pyredise
</code></pre>

<br>
<p>
<b>Features:</b>
<ul>
	<li>Dynamic, fast indexing/removal of documents</li>
	<li>Vector space model document retrieval</li>	
	<li>Ranking with tf-idf scores, proximity, title</li>
</ul>	
</p>

<br>
<p>
<b>Dependencies:</b>
<ul>
	<li>redis</li>
	<li>redis-py (https://github.com/andymccurdy/redis-py)</li>
	<li>nltk (Natural Language Toolkit)</li>
</ul>	
</p>	


<br>	
<b>Instructions:</b>

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
doc = {"id":"a uuid is an excellent candidate", "title":"How dummy", "content":"bla bla bla"}

cp.index( doc )
</code></pre>
		
</p>		

<br>
<p>
<b>Filters:</b>
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

<br>


<b>HOW IS THE INDEX STRUCTURED?</b>
<p>
We keep sorted sets of the form ( term: [(doc_id, term_frequency_in_this_doc_id),...] ). 
This way, we can intersect those sets while calculating the tf-idf score on the fly,
by providing WEIGHTS (term document frequencies, which are actually the cardinality of each sorted set)
<br>
To do proximity ranking, we keep hashes of the form:
	term:{ 
		  doc_id: positions, 
		  doc_id: positions
		 }
<br> 
We also keep a similar hash for the terms' positions in the title, as well as simple sets (term:(doc_ids..)) to perform intersections. 		 

</p>

<br>

<p>
For those who haven't noticed, pyredise is named in honor of PY(thon)REDI(s)S(earch)E(ngine)
</p>