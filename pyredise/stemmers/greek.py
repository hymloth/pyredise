# -*- coding: utf-8  -*-

stopwords = ["είναι", "θέλω","ἀλλά", "κατά", "αυτός", "αυτή", "αυτό", "μετά", "περί", "ούτε", "παρά", "εμείς", "εσείς", "αυτοί", "αυτές", "αυτά", "είσαι","ηταν", "είμαστε",
             "είσαστε", "όπως", "χωρίς", "στους","οποία", "τρεις", "ακόμα","περίπου", "έχουν", "οποίος", "και", "από", "το"]

VOWELS = [i.decode("utf8") for i in ['α', 'ε', 'η', 'ι', 'ο', 'υ', 'ω', 'ά', 'έ', 'ή', 'ί', 'ό', 'ύ', 'ώ', 'ϊ', 'ϋ']]


replacements = {"Α":"α", "Β":"β", "Γ":"γ", "Δ":"δ", "Ε":"ε", "Ζ":"ζ", 'Η':'η', 'Θ':'θ', 'Ι':'ι', 
                'Κ':'κ','Λ':'λ','Μ':'μ','Ν':'ν','Ξ':'ξ','Ο':'ο','Π':'π','Ρ':'ρ','Σ':'σ','Τ':'τ','Υ':'υ','Φ':'φ',
                'Χ':'χ','Ψ':'ψ', 'Ω':'ω',
                'Ά':'α', 'Έ':'ε', 'Ή':'η', 'Ί':'ι', 'Ό':'ο', 'Ύ':'υ', 'Ώ':'ω', 'Ϊ':'ι', 'Ϋ':'υ',
                'ά':'α', 'έ':'ε', 'ή':'η', 'ί':'ι', 'ό':'ο', 'ύ':'υ', 'ώ':'ω', 'Ϊ':'ϊ', 'Ϋ':'ϋ'}


r = {}
for k, v in replacements.iteritems():
    r[k] = v

def ends_with(word, suffix):
    return word[len(word) - len(suffix):] == suffix

def stem(w):
    
    
    word = ""

    for i in w:
        if i in r:
            word += r[i]
        else:
            word += i

    done = len(word) <= 3


    
    ##rule-set  1
    ##γιαγιαδεσ->γιαγ, ομαδεσ->ομαδ
    if not done:
        for suffix in [i.decode("utf8") for i in ['ιαδες', 'αδες', 'αδων']]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                remaining_part_does_not_end_on = True
                for s in [i.decode("utf8") for i in ['οκ', 'μαμ', 'μαν', 'μπαμπ', 'πατερ', 'γιαγ', 'νταντ', 'κυρ', 'θει', 'πεθερ']]:
                    if ends_with(word, s):
                        remaining_part_does_not_end_on = False
                        break
                if remaining_part_does_not_end_on:
                    word = word + 'αδ'.decode("utf8")
                done = True
                break

    ##rule-set  2
    ##καφεδεσ->καφ, γηπεδων->γηπεδ
    if not done:
        for suffix in [i.decode("utf8") for i in ['εδες', 'εδων']]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                for s in [i.decode("utf8") for i in ['οπ', 'ιπ', 'εμπ', 'υπ', 'γηπ', 'δαπ', 'κρασπ', 'μιλ']]:
                    if ends_with(word, s):
                        word = word + 'εδ'.decode("utf8")
                        break
                done = True
                break

    ##rule-set  3
    ##παππουδων->παππ, αρκουδεσ->αρκουδ
    if not done:
        for suffix in [i.decode("utf8") for i in ['ουδες', 'ουδων']]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                for s in [i.decode("utf8") for i in ['αρκ', 'καλιακ', 'πεταλ', 'λιχ', 'πλεξ', 'σκ', 'ς', 'φλ', 'φρ', 'βελ', 'λουλ', 'χν', 'σπ', 'τραγ', 'φε']]:
                    if ends_with(word, s):
                        word = word + 'ουδ'.decode("utf8")
                        break
                done = True
                break

    ##rule-set  4
    ##υποθεσεωσ->υποθεσ, θεων->θε
    if not done:
        for suffix in [i.decode("utf8") for i in ['εως', 'εων']]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                for s in [i.decode("utf8") for i in ['θ', 'δ', 'ελ', 'γαλ', 'ν', 'π', 'ιδ', 'παρ']]:
                    if ends_with(word, s):
                        word = word + 'ε'.decode("utf8")
                        break
                done = True
                break

    ##rule-set  5
    ##παιδια->παιδ, τελειου->τελει
    if not done:
        for suffix in [i.decode("utf8") for i in ['ια', 'ιου', 'ιων']]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                for s in VOWELS:
                    if ends_with(word, s):
                        word = word + 'ι'.decode("utf8")
                        break
                done = True
                break

    ##rule-set  6
    ##ζηλιαρικο->ζηλιαρ, αγροικοσ->αγροικ
    if not done:
        for suffix in [i.decode("utf8") for i in ['ικα', 'ικου', 'ικων', 'ικος', 'ικο', 'ικη']]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in [i.decode("utf8") for i in ['αλ', 'αδ', 'ενδ', 'αμαν', 'αμμοχαλ', 'ηθ', 'ανηθ', 'αντιδ', 'φυς', 'βρωμ', 'γερ', 'εξωδ', 'καλπ',
                            'καλλιν', 'καταδ', 'μουλ', 'μπαν', 'μπαγιατ', 'μπολ', 'μπος', 'νιτ', 'ξικ', 'συνομηλ', 'πετς', 'πιτς',
                            'πικαντ', 'πλιατς', 'ποντ', 'ποστελν', 'πρωτοδ', 'σερτ', 'συναδ', 'τσαμ', 'υποδ', 'φιλον', 'φυλοδ',
                            'χας']]:
                    word = word + 'ικ'.decode("utf8")
                else:
                    for s in VOWELS:
                        if ends_with(word, s):
                            word = word + 'ικ'.decode("utf8")
                            break
                done = True
                break

    ##rule-set  7
    ##αγαπαγαμε->αγαπ, αναπαμε->αναπαμ
    if not done:
        if word == 'αγαμε'.decode("utf8"): word = 2*word
        for suffix in [i.decode("utf8") for i in ['ηθηκαμε', 'αγαμε', 'ησαμε', 'ουσαμε', 'ηκαμε']]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['φ'.decode("utf8")]:
                    word = word + 'αγαμ'.decode("utf8")
                done = True
                break
        if not done and ends_with(word, 'αμε'.decode("utf8")):
            word = word[:len(word) - len('αμε'.decode("utf8"))]
            if word in [i.decode("utf8") for i in ['αναπ', 'αποθ', 'αποκ', 'αποστ', 'βουβ', 'ξεθ', 'ουλ', 'πεθ', 'πικρ', 'ποτ', 'σιχ', 'χ']]:
                word = word + 'αμ'.decode("utf8")
            done = True

    ##rule-set  8
    ##αγαπησαμε->αγαπ, τραγανε->τραγαν
    if not done:
        for suffix in [i.decode("utf8") for i in ['ιουντανε', 'ιοντανε', 'ουντανε', 'ηθηκανε', 'ουσανε', 'ιοτανε', 'οντανε', 'αγανε', 'ησανε',
                       'οτανε', 'ηκανε']]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in [i.decode("utf8") for i in ['τρ', 'τς', 'φ']]:
                    word = word + 'αγαν'.decode("utf8")
                done = True
                break
        if not done and ends_with(word, 'ανε'.decode("utf8")):
            word = word[:len(word) - len('αμε'.decode("utf8"))]
            if word in [i.decode("utf8") for i in ['βετερ', 'βουλκ', 'βραχμ', 'γ', 'δραδουμ', 'θ', 'καλπουζ', 'καστελ', 'κορμορ', 'λαοπλ', 'μωαμεθ', 'μ',
                        'μουσουλμ', 'ν', 'ουλ', 'π', 'πελεκ', 'πλ', 'πολις', 'πορτολ', 'σαρακατς', 'σουλτ', 'τσαρλατ', 'ορφ',
                        'τσιγγ', 'τσοπ', 'φωτοστεφ', 'χ', 'ψυχοπλ', 'αγ', 'ορφ', 'γαλ', 'γερ', 'δεκ', 'διπλ', 'αμερικαν', 'ουρ',
                        'πιθ', 'πουριτ', 'ς', 'ζωντ', 'ικ', 'καστ', 'κοπ', 'λιχ', 'λουθηρ', 'μαιντ', 'μελ', 'σιγ', 'σπ', 'στεγ',
                        'τραγ', 'τσαγ', 'φ', 'ερ', 'αδαπ', 'αθιγγ', 'αμηχ', 'ανικ', 'ανοργ', 'απηγ', 'απιθ', 'ατσιγγ', 'βας',
                        'βασκ', 'βαθυγαλ', 'βιομηχ', 'βραχυκ', 'διατ', 'διαφ', 'ενοργ', 'θυς', 'καπνοβιομηχ', 'καταγαλ', 'κλιβ',
                        'κοιλαρφ', 'λιβ', 'μεγλοβιομηχ', 'μικροβιομηχ', 'νταβ', 'ξηροκλιβ', 'ολιγοδαμ', 'ολογαλ', 'πενταρφ',
                        'περηφ', 'περιτρ', 'πλατ', 'πολυδαπ', 'πολυμηχ', 'στεφ', 'ταβ', 'τετ', 'υπερηφ', 'υποκοπ', 'χαμηλοδαπ',
                        'ψηλοταβ']]:
                word = word + 'αν'.decode("utf8")
            else:
                for s in VOWELS:
                    if ends_with(word, s):
                        word = word + 'αν'.decode("utf8")
                        break
            done = True

    ##rule-set  9
    ##αγαπησετε->αγαπ, βενετε->βενετ
    if not done:
        if ends_with(word, 'ησετε'.decode("utf8")):
            word = word[:len(word) - len('ησετε'.decode("utf8"))]
            done = True
        elif ends_with(word, 'ετε'.decode("utf8")):
            word = word[:len(word) - len('ετε'.decode("utf8"))]
            if word in [i.decode("utf8") for i in ['αβαρ', 'βεν', 'εναρ', 'αβρ', 'αδ', 'αθ', 'αν', 'απλ', 'βαρον', 'ντρ', 'σκ', 'κοπ', 'μπορ', 'νιφ', 'παγ',
                        'παρακαλ', 'σερπ', 'σκελ', 'συρφ', 'τοκ', 'υ', 'δ', 'εμ', 'θαρρ', 'θ']]:
                word = word + 'ετ'.decode("utf8")
            else:
                for s in [i.decode("utf8") for i in ['οδ', 'αιρ', 'φορ', 'ταθ', 'διαθ', 'σχ', 'ενδ', 'ευρ', 'τιθ', 'υπερθ', 'ραθ', 'ενθ', 'ροθ', 'σθ', 'πυρ',
                          'αιν', 'συνδ', 'συν', 'συνθ', 'χωρ', 'πον', 'βρ', 'καθ', 'ευθ', 'εκθ', 'νετ', 'ρον', 'αρκ', 'βαρ', 'βολ',
                          'ωφελ']] + VOWELS:
                    if ends_with(word, s):
                        word = word + 'ετ'.decode("utf8")
                        break
            done = True

    ##rule-set 10
    ##αγαπωντασ->αγαπ, ξενοφωντασ->ξενοφων
    if not done:
        for suffix in [i.decode("utf8") for i in ['οντας', 'ωντας']]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['αρχ'.decode("utf8")]:
                    word = word + 'οντ'.decode("utf8")
                elif word in [i.decode("utf8") for i in ['ξενοφ', 'κρε']]:
                    word = word + 'ωντ'.decode("utf8")
                done = True
                break

    ##rule-set 11
    ##αγαπιομαστε->αγαπ, ονομαστε->ονομαστ
    if not done:
        for suffix in [i.decode("utf8") for i in ['ιομαστε', 'ομαστε']]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['ον'.decode("utf8")]:
                    word = word + 'ομαστ'.decode("utf8")
                done = True
                break

    ##rule-set 12
    ##αγαπιεστε->αγαπ, πιεστε->πιεστ
    if not done:
        for suffix in ['ιεστε'.decode("utf8")]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in [i.decode("utf8") for i in ['π', 'απ', 'συμπ', 'ασυμπ', 'καταπ', 'μεταμφ']]:
                    word = word + 'ιεστ'.decode("utf8")
                done = True
                break
    if not done:
        for suffix in ['εστε'.decode("utf8")]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in [i.decode("utf8") for i in ['αλ', 'αρ', 'εκτελ', 'ζ', 'μ', 'ξ', 'παρακαλ', 'αρ', 'προ', 'νις']]:
                    word = word + 'εστ'.decode("utf8")
                done = True
                break

    ##rule-set 13
    ##χτιστηκε->χτιστ, διαθηκεσ->διαθηκ
    if not done:
        for suffix in [i.decode("utf8") for i in ['ηθηκα', 'ηθηκες', 'ηθηκε']]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                done = True
                break
    if not done:
        for suffix in [i.decode("utf8") for i in ['ηκα', 'ηκες', 'ηκε']]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in [i.decode("utf8") for i in ['διαθ', 'θ', 'παρακαταθ', 'προσθ', 'συνθ']]:
                    word = word + 'ηκ'.decode("utf8")
                else:
                    for suffix in [i.decode("utf8") for i in ['σκωλ', 'σκουλ', 'ναρθ', 'σφ', 'οθ', 'πιθ']]:
                        if ends_with(word, suffix):
                            word = word + 'ηκ'.decode("utf8")
                            break
                done = True
                break
            
    ##rule-set 14
    ##χτυπουσεσ->χτυπ, μεδουσεσ->μεδουσ
    if not done:
        for suffix in [i.decode("utf8") for i in ['ουσα', 'ουσες', 'ουσε']]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in [i.decode("utf8") for i in ['φαρμακ', 'χαδ', 'αγκ', 'αναρρ', 'βρομ', 'εκλιπ', 'λαμπιδ', 'λεχ', 'μ', 'πατ', 'ρ', 'λ', 'μεδ', 'μεσαζ',
                            'υποτειν', 'αμ', 'αιθ', 'ανηκ', 'δεσποζ', 'ενδιαφερ', 'δε', 'δευτερευ', 'καθαρευ', 'πλε', 'τσα']]:
                    word = word + 'ους'.decode("utf8")
                else:
                    for s in [i.decode("utf8") for i in ['ποδαρ', 'βλεπ', 'πανταχ', 'φρυδ', 'μαντιλ', 'μαλλ', 'κυματ', 'λαχ', 'ληγ', 'φαγ', 'ομ', 'πρωτ']] + VOWELS:
                        if ends_with(word, s):
                            word = word + 'ους'.decode("utf8")
                            break
                done = True
                break

    ##rule-set 15
    #κολλαγεσ->κολλ, αβασταγα->αβαστ
    if not done:
        for suffix in [i.decode("utf8") for i in ['αγα', 'αγες', 'αγε']]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in [i.decode("utf8") for i in ['αβαστ', 'πολυφ', 'αδηφ', 'παμφ', 'ρ', 'ασπ', 'αφ', 'αμαλ', 'αμαλλι', 'ανυστ', 'απερ', 'ασπαρ', 'αχαρ',
                            'δερβεν', 'δροσοπ', 'ξεφ', 'νεοπ', 'νομοτ', 'ολοπ', 'ομοτ', 'προστ', 'προσωποπ', 'συμπ', 'συντ', 'τ',
                            'υποτ', 'χαρ', 'αειπ', 'αιμοστ', 'ανυπ', 'αποτ', 'αρτιπ', 'διατ', 'εν', 'επιτ', 'κροκαλοπ', 'σιδηροπ',
                            'λ', 'ναυ', 'ουλαμ', 'ουρ', 'π', 'τρ', 'μ']]:
                    word = word + 'αγ'.decode("utf8")
                else:
                    for s in [i.decode("utf8") for i in ['οφ', 'πελ', 'χορτ', 'σφ', 'ρπ', 'φρ', 'πρ', 'λοχ', 'σμην']]:
                        # αφαιρεθηκε: 'λλ'
                        if ends_with(word, s):
                            if not word in ['ψοφ'.decode("utf8"), 'ναυλοχ'.decode("utf8")]:
                                word = word + 'αγ'.decode("utf8")
                            break
                done = True
                break

    ##rule-set 16
    ##αγαπησε->αγαπ, νησου->νησ
    if not done:
        for suffix in [i.decode("utf8") for i in ['ησε', 'ησου', 'ησα']]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in [i.decode("utf8") for i in ['ν', 'χερσον', 'δωδεκαν', 'ερημον', 'μεγαλον', 'επταν', 'αγαθον']]:
                    word = word + 'ης'.decode("utf8")
                done = True
                break
            
    ##rule-set 17
    ##αγαπηστε->αγαπ, σβηστε->σβηστ
    if not done:
        for suffix in ['ηστε'.decode("utf8")]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in [i.decode("utf8") for i in ['ασβ', 'σβ', 'αχρ', 'χρ', 'απλ', 'αειμν', 'δυσχρ', 'ευχρ', 'κοινοχρ', 'παλιμψ']]:
                    word = word + 'ηστ'.decode("utf8")
                done = True
                break
            
    ##rule-set 18
    ##αγαπουνε->αγαπ, σπιουνε->σπιουν
    if not done:
        for suffix in [i.decode("utf8") for i in ['ουνε', 'ησουνε', 'ηθουνε']]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in [i.decode("utf8") for i in ['ν', 'ρ', 'σπι', 'στραβομουτς', 'κακομουτς', 'εξων']]:
                    word = word + 'ουν'.decode("utf8")
                done = True
                break
            
    ##rule-set 19
    ##αγαπουμε->αγαπ, φουμε->φουμ
    if not done:
        for suffix in [i.decode("utf8") for i in ['ουμε', 'ησουμε', 'ηθουμε']]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in [i.decode("utf8") for i in ['παρασους', 'φ', 'χ', 'ωριοπλ', 'αζ', 'αλλοσους', 'ασους']]:
                    word = word + 'ουμ'.decode("utf8")
                done = True
                break
            
    ##rule-set 20
    ##κυματα->κυμ, χωρατο->χωρατ
    if not done:
        for suffix in [i.decode("utf8") for i in ['ματα', 'ματων', 'ματος']]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                word = word + 'μ'.decode("utf8")
                done = True
                break
            
    ##rule-set 21
    if not done:
        for suffix in [i.decode("utf8") for i in ['ιοντουσαν', 'ιουμαστε', 'ιομασταν', 'ιοσασταν', 'οντουσαν', 'ιοσαστε', 'ιεμαστε', 'ιεσαστε', 'ιομουνα',
                       'ιοσουνα', 'ιουνται', 'ιουνταν', 'ηθηκατε', 'ομασταν', 'οσασταν', 'ουμαστε', 'ιομουν', 'ιονταν', 'ιοσουν',
                       'ηθειτε', 'ηθηκαν', 'ομουνα', 'οσαστε', 'οσουνα', 'ουνται', 'ουνταν', 'ουσατε',  'αγατε', 'ειται', 'ιεμαι',
                       'ιεται', 'ιεσαι', 'ιοταν', 'ιουμα', 'ηθεις', 'ηθουν', 'ηκατε', 'ησατε', 'ησουν', 'ομουν',  'ονται',
                       'ονταν', 'οσουν', 'ουμαι', 'ουσαν',  'αγαν', 'αμαι', 'ασαι', 'αται', 'ειτε', 'εσαι', 'εται', 'ηδες',
                       'ηδων', 'ηθει', 'ηκαν', 'ησαν', 'ησει', 'ησες', 'ομαι', 'οταν',  'αει',  'εις',  'ηθω',  'ησω', 'ουν',
                       'ους',  'αν', 'ας', 'αω', 'ει', 'ες', 'ης', 'οι', 'ον', 'ος', 'ου', 'υς', 'ων', 'ως', 'α', 'ε', 'ι', 'η',
                       'ο',  'υ', 'ω']]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                break

    ##rule-set 22
    ##πλησιεστατοσ->πλυσι, μεγαλυτερη->μεγαλ, κοντοτερο->κοντ
    if not done:
        for suffix in [i.decode("utf8") for i in ['εστερ', 'εστατ', 'οτερ', 'οτατ', 'υτερ', 'υτατ', 'ωτερ', 'ωτατ']]:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                break
    
    if len(word) >=3:   
        return word
    return ""


#print stem("γιαγιαδες")