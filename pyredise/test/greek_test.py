# -*- coding: utf-8 -*-

import random
import redis , time, json
import re

from pyredise.corpus_handler import CorpusHandler
from pyredise.query_handler import QueryHandler

if __name__=='__main__':

	db = redis.Redis(host='192.168.1.3', port=6666, db=3)


	f = open("greek_text.txt", "r")
	text = f.read()
	f.close()

	text = re.sub(' +', ' ', text)

	data = []
	cnt = 0

	l = len(text)

	while cnt < l:
		r = random.randint(400, 1200)

		try:
			data.append({"content":text[cnt:cnt+r], "title":text[cnt:cnt+random.randint(40, 130)], "id":cnt})
			cnt += r
		except:
			break


	cp = CorpusHandler(debug=False, db=db)
	cp.drop()

	s = time.time()
	for a in data:
		try:
			cp.index(a)
		except:
			pass


	print "indexing: " , time.time() - s


	q = QueryHandler(debug=False, db=db, use_lua=True)
	q2 = QueryHandler(debug=False, db=db, use_lua=False)

	
	qs = ["ακόρεστο θηλυκό", "ευάλωτη παρθένα", "ξέσπασα ολόλευκος", "κάμπος ανθισμένος"] # lol

	s = time.time()
	'''for i in qs:
		q.process_query(i)
	print "q " , time.time() - s

	s = time.time()
	for i in qs:
		q2.process_query(i)
	print "q2 " , time.time() - s'''



	for i in qs:
		a = q.process_query(i)
		b = q2.process_query(i)
		print a, b
