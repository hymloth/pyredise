# -*- coding: utf-8 -*-
import redis , time, json

from corpus_handler import CorpusHandler

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

    
    cp = CorpusHandler(debug=True, db=db)
    cp.drop()


    start = time.time()
    for n, i in enumerate(articles):
        print  i["id"]
        if not   cp.index(i):
            print "features:", cp.extract_features(doc = i["content"])