# -*- coding: utf-8 -*-
import redis , time, json

from pyredise.corpus_handler import CorpusHandler
from pyredise.query_handler import QueryHandler

if __name__=='__main__':



	texts = [
	 "The quick brown fox jumps over the lazy dog and fucks the hell out of it",
	 "Den raske brune reven hopper over den late hunden og knuller i helvete ut av det",
	 "Den hurtige brune ræv hopper over den dovne hund og knepper fanden ud af det",
	 "Быстрая коричневая лиса прыгает через ленивую собаку и трахает ад из этого",
	 "De snelle bruine vos springt over de luie hond en neukt de hel van te maken",
	 "Nopea ruskea kettu hyppää laiskan koiran yli ja vittuile helvettiin siitä",
	 "Le rapide renard brun saute par dessus le chien paresseux et baise l'enfer hors de lui",
	 "Der schnelle braune Fuchs springt über den faulen Hund und fickt die Hölle aus ihm heraus",
	 "A gyors barna róka átugorja a lusta kutyát, és baszik a fenébe is",
	 "La volpe veloce salta sul cane pigro e scopa l'inferno fuori di esso",
	 "A ligeira raposa marrom ataca o cão preguiçoso e fode o inferno fora dele",
	 "El rápido zorro marrón salta sobre el perro perezoso y folla el infierno fuera de él",
	 "En snabb brun räv hoppar över den lata hunden och knullar skiten ur det",
	 "Hızlı kahverengi tilki tembel köpeğin üstünden atlar ve bunun cehenneme sikikleri",
	 "Η γρήγορη καφέ αλεπού πηδάει πάνω από το μεσημέρι και τρέχει έξω από αυτό γιαγιάδες γιαγιαδες",
	 #"Idź prosto i skręć w lewo/prawo Poczekaj chwilę Chodź ze mną Szukam John’a już"
	 ]


	articles = []
	for i, text in enumerate(texts):
	    articles.append({"content" : text, "title" : text[:15], "id":i+1})


	db = redis.Redis(host='192.168.1.3', port=6666, db=3)


	cp = CorpusHandler(debug=False, db=db)
	cp.drop()


	s = time.time()
	for a in articles:

		cp.index(a)


	print "indexing: " , time.time() - s

	
	q = QueryHandler(debug=False, db=db, use_lua=True)
	q2 = QueryHandler(debug=False, db=db, use_lua=False)

	s = time.time()

	q.process_query("the brown")
	q.process_query("Den raske brune")
	q.process_query("Den hurtige brune ræv")
	q.process_query("Быстрая коричневая лиса")
	q.process_query("Den raske brune")
	q.process_query("De snelle bruine")
	q.process_query("Nopea ruskea kettu hyppää")

	q.process_query("Le rapide renard brun saute")
	q.process_query("Der schnelle braune Fuchs")
	q.process_query("A gyors barna róka átugorja a lusta kutyát")
	q.process_query("veloce salta sul")
	q.process_query("raposa marrom ataca")
	q.process_query("zorro marrón salta")
	q.process_query("brun räv hoppar över")
	q.process_query("kahverengi tilki tembel köpeğin")
	q.process_query("πηδάει πάνω από το μεσημέρι")

	q.process_query("brune"), 

	print "q: " , time.time() - s


	s = time.time()

	q2.process_query("the brown")
	q2.process_query("Den raske brune")
	q2.process_query("Den hurtige brune ræv")
	q2.process_query("Быстрая коричневая лиса")
	q2.process_query("Den raske brune")
	q2.process_query("De snelle bruine")
	q2.process_query("Nopea ruskea kettu hyppää")

	q2.process_query("Le rapide renard brun saute")
	q2.process_query("Der schnelle braune Fuchs")
	q2.process_query("A gyors barna róka átugorja a lusta kutyát")
	q2.process_query("veloce salta sul")
	q2.process_query("raposa marrom ataca")
	q2.process_query("zorro marrón salta")
	q2.process_query("brun räv hoppar över")
	q2.process_query("kahverengi tilki tembel köpeğin")
	q2.process_query("πηδάει πάνω από το μεσημέρι")

	q2.process_query("brune"), 

	print "q2: " , time.time() - s