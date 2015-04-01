# -*- coding: utf-8 -*-
from pyredise import query_handler, corpus_handler, quick_language_detection, sensitive_language_detection


articles = [
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
 #"Hızlı kahverengi tilki tembel köpeğin üstünden atlar ve bunun cehenneme sikikleri",
 "Η γρήγορη καφέ αλεπού πηδάει πάνω από το μεσημέρι και πηδάει την κόλαση έξω από αυτό"
 ]
 




if __name__=="__main__":
    


    import redis , time, json
    db = redis.Redis(host='192.168.1.6', port=6666, db=3)
    from noocore.models.mongo_models import Article, Magazine    
    from mongoengine import connect
   
    DATABASE = "nootropia"
    USERNAME = "dummy"
    PASSWORD = "dummy"
     
    mdb = connect(DATABASE, username = USERNAME, password = PASSWORD)    
    
    cp = corpus_handler.CorpusHandler(debug=True, db=db)
    cp.drop()

    QH = query_handler.QueryHandler(debug=True, db=db, limit=200)
    
    for i, v in enumerate(articles):
        cp.index({"id":i, "title":v, "content":v})

    for i, v in enumerate(articles):
        print i
        try:
            print sensitive_language_detection.check_lang(v), QH.process_query(" ".join(v.split()[1:4]))
        except:
            print "err"
        
