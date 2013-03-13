# -*- coding: utf-8  -*-

stopwords = ["είναι", "θέλω","ἀλλά", "κατά", "αυτός", "αυτή", "αυτό", "μετά", "περί", "ούτε", "παρά", "εμείς", "εσείς", "αυτοί", "αυτές", "αυτά", "είσαι","ηταν", "είμαστε",
             "είσαστε", "όπως", "χωρίς", "στους","οποία", "τρεις", "ακόμα","περίπου", "έχουν", "οποίος"]

VOWELS = ['α', 'ε', 'η', 'ι', 'ο', 'υ', 'ω', 'ά', 'έ', 'ή', 'ί', 'ό', 'ύ', 'ώ', 'ϊ', 'ϋ']


replacements = {"Α":"α", "Β":"β", "Γ":"γ", "Δ":"δ", "Ε":"ε", "Ζ":"ζ", 'Η':'η', 'Θ':'θ', 'Ι':'ι', 
                'Κ':'κ','Λ':'λ','Μ':'μ','Ν':'ν','Ξ':'ξ','Ο':'ο','Π':'π','Ρ':'ρ','Σ':'σ','Τ':'τ','Υ':'υ','Φ':'φ',
                'Χ':'χ','Ψ':'ψ', 'Ω':'ω',
                'Ά':'α', 'Έ':'ε', 'Ή':'η', 'Ί':'ι', 'Ό':'ο', 'Ύ':'υ', 'Ώ':'ω', 'Ϊ':'ι', 'Ϋ':'υ',
                'ά':'α', 'έ':'ε', 'ή':'η', 'ί':'ι', 'ό':'ο', 'ύ':'υ', 'ώ':'ω', 'Ϊ':'ϊ', 'Ϋ':'ϋ'}


r = {}
for k, v in replacements.iteritems():
    r[k.decode("utf-8")] = v.decode("utf-8")

def ends_with(word, suffix):
    return word[len(word) - len(suffix):] == suffix

def stem(w):
    
    
    word = ""

    for i in w.decode("utf-8"):
        if i in r:
            word += r[i]
        else:
            word += i


    done = len(word) <= 3
    
    ##rule-set  1
    ##γιαγιαδεσ->γιαγ, ομαδεσ->ομαδ
    if not done:
        for suffix in ['ιαδες', 'αδες', 'αδων']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                remaining_part_does_not_end_on = True
                for s in ['οκ', 'μαμ', 'μαν', 'μπαμπ', 'πατερ', 'γιαγ', 'νταντ', 'κυρ', 'θει', 'πεθερ']:
                    if ends_with(word, s):
                        remaining_part_does_not_end_on = False
                        break
                if remaining_part_does_not_end_on:
                    word = word + 'αδ'
                done = True
                break

    ##rule-set  2
    ##καφεδεσ->καφ, γηπεδων->γηπεδ
    if not done:
        for suffix in ['εδες', 'εδων']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                for s in ['οπ', 'ιπ', 'εμπ', 'υπ', 'γηπ', 'δαπ', 'κρασπ', 'μιλ']:
                    if ends_with(word, s):
                        word = word + 'εδ'
                        break
                done = True
                break

    ##rule-set  3
    ##παππουδων->παππ, αρκουδεσ->αρκουδ
    if not done:
        for suffix in ['ουδες', 'ουδων']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                for s in ['αρκ', 'καλιακ', 'πεταλ', 'λιχ', 'πλεξ', 'σκ', 'ς', 'φλ', 'φρ', 'βελ', 'λουλ', 'χν', 'σπ', 'τραγ', 'φε']:
                    if ends_with(word, s):
                        word = word + 'ουδ'
                        break
                done = True
                break

    ##rule-set  4
    ##υποθεσεωσ->υποθεσ, θεων->θε
    if not done:
        for suffix in ['εως', 'εων']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                for s in ['θ', 'δ', 'ελ', 'γαλ', 'ν', 'π', 'ιδ', 'παρ']:
                    if ends_with(word, s):
                        word = word + 'ε'
                        break
                done = True
                break

    ##rule-set  5
    ##παιδια->παιδ, τελειου->τελει
    if not done:
        for suffix in ['ια', 'ιου', 'ιων']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                for s in VOWELS:
                    if ends_with(word, s):
                        word = word + 'ι'
                        break
                done = True
                break

    ##rule-set  6
    ##ζηλιαρικο->ζηλιαρ, αγροικοσ->αγροικ
    if not done:
        for suffix in ['ικα', 'ικου', 'ικων', 'ικος', 'ικο', 'ικη']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['αλ', 'αδ', 'ενδ', 'αμαν', 'αμμοχαλ', 'ηθ', 'ανηθ', 'αντιδ', 'φυς', 'βρωμ', 'γερ', 'εξωδ', 'καλπ',
                            'καλλιν', 'καταδ', 'μουλ', 'μπαν', 'μπαγιατ', 'μπολ', 'μπος', 'νιτ', 'ξικ', 'συνομηλ', 'πετς', 'πιτς',
                            'πικαντ', 'πλιατς', 'ποντ', 'ποστελν', 'πρωτοδ', 'σερτ', 'συναδ', 'τσαμ', 'υποδ', 'φιλον', 'φυλοδ',
                            'χας']:
                    word = word + 'ικ'
                else:
                    for s in VOWELS:
                        if ends_with(word, s):
                            word = word + 'ικ'
                            break
                done = True
                break

    ##rule-set  7
    ##αγαπαγαμε->αγαπ, αναπαμε->αναπαμ
    if not done:
        if word == 'αγαμε': word = 2*word
        for suffix in ['ηθηκαμε', 'αγαμε', 'ησαμε', 'ουσαμε', 'ηκαμε']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['φ']:
                    word = word + 'αγαμ'
                done = True
                break
        if not done and ends_with(word, 'αμε'):
            word = word[:len(word) - len('αμε')]
            if word in ['αναπ', 'αποθ', 'αποκ', 'αποστ', 'βουβ', 'ξεθ', 'ουλ', 'πεθ', 'πικρ', 'ποτ', 'σιχ', 'χ']:
                word = word + 'αμ'
            done = True

    ##rule-set  8
    ##αγαπησαμε->αγαπ, τραγανε->τραγαν
    if not done:
        for suffix in ['ιουντανε', 'ιοντανε', 'ουντανε', 'ηθηκανε', 'ουσανε', 'ιοτανε', 'οντανε', 'αγανε', 'ησανε',
                       'οτανε', 'ηκανε']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['τρ', 'τς', 'φ']:
                    word = word + 'αγαν'
                done = True
                break
        if not done and ends_with(word, 'ανε'):
            word = word[:len(word) - len('αμε')]
            if word in ['βετερ', 'βουλκ', 'βραχμ', 'γ', 'δραδουμ', 'θ', 'καλπουζ', 'καστελ', 'κορμορ', 'λαοπλ', 'μωαμεθ', 'μ',
                        'μουσουλμ', 'ν', 'ουλ', 'π', 'πελεκ', 'πλ', 'πολις', 'πορτολ', 'σαρακατς', 'σουλτ', 'τσαρλατ', 'ορφ',
                        'τσιγγ', 'τσοπ', 'φωτοστεφ', 'χ', 'ψυχοπλ', 'αγ', 'ορφ', 'γαλ', 'γερ', 'δεκ', 'διπλ', 'αμερικαν', 'ουρ',
                        'πιθ', 'πουριτ', 'ς', 'ζωντ', 'ικ', 'καστ', 'κοπ', 'λιχ', 'λουθηρ', 'μαιντ', 'μελ', 'σιγ', 'σπ', 'στεγ',
                        'τραγ', 'τσαγ', 'φ', 'ερ', 'αδαπ', 'αθιγγ', 'αμηχ', 'ανικ', 'ανοργ', 'απηγ', 'απιθ', 'ατσιγγ', 'βας',
                        'βασκ', 'βαθυγαλ', 'βιομηχ', 'βραχυκ', 'διατ', 'διαφ', 'ενοργ', 'θυς', 'καπνοβιομηχ', 'καταγαλ', 'κλιβ',
                        'κοιλαρφ', 'λιβ', 'μεγλοβιομηχ', 'μικροβιομηχ', 'νταβ', 'ξηροκλιβ', 'ολιγοδαμ', 'ολογαλ', 'πενταρφ',
                        'περηφ', 'περιτρ', 'πλατ', 'πολυδαπ', 'πολυμηχ', 'στεφ', 'ταβ', 'τετ', 'υπερηφ', 'υποκοπ', 'χαμηλοδαπ',
                        'ψηλοταβ']:
                word = word + 'αν'
            else:
                for s in VOWELS:
                    if ends_with(word, s):
                        word = word + 'αν'
                        break
            done = True

    ##rule-set  9
    ##αγαπησετε->αγαπ, βενετε->βενετ
    if not done:
        if ends_with(word, 'ησετε'):
            word = word[:len(word) - len('ησετε')]
            done = True
        elif ends_with(word, 'ετε'):
            word = word[:len(word) - len('ετε')]
            if word in ['αβαρ', 'βεν', 'εναρ', 'αβρ', 'αδ', 'αθ', 'αν', 'απλ', 'βαρον', 'ντρ', 'σκ', 'κοπ', 'μπορ', 'νιφ', 'παγ',
                        'παρακαλ', 'σερπ', 'σκελ', 'συρφ', 'τοκ', 'υ', 'δ', 'εμ', 'θαρρ', 'θ']:
                word = word + 'ετ'
            else:
                for s in ['οδ', 'αιρ', 'φορ', 'ταθ', 'διαθ', 'σχ', 'ενδ', 'ευρ', 'τιθ', 'υπερθ', 'ραθ', 'ενθ', 'ροθ', 'σθ', 'πυρ',
                          'αιν', 'συνδ', 'συν', 'συνθ', 'χωρ', 'πον', 'βρ', 'καθ', 'ευθ', 'εκθ', 'νετ', 'ρον', 'αρκ', 'βαρ', 'βολ',
                          'ωφελ'] + VOWELS:
                    if ends_with(word, s):
                        word = word + 'ετ'
                        break
            done = True

    ##rule-set 10
    ##αγαπωντασ->αγαπ, ξενοφωντασ->ξενοφων
    if not done:
        for suffix in ['οντας', 'ωντας']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['αρχ']:
                    word = word + 'οντ'
                elif word in ['ξενοφ', 'κρε']:
                    word = word + 'ωντ'
                done = True
                break

    ##rule-set 11
    ##αγαπιομαστε->αγαπ, ονομαστε->ονομαστ
    if not done:
        for suffix in ['ιομαστε', 'ομαστε']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['ον']:
                    word = word + 'ομαστ'
                done = True
                break

    ##rule-set 12
    ##αγαπιεστε->αγαπ, πιεστε->πιεστ
    if not done:
        for suffix in ['ιεστε']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['π', 'απ', 'συμπ', 'ασυμπ', 'καταπ', 'μεταμφ']:
                    word = word + 'ιεστ'
                done = True
                break
    if not done:
        for suffix in ['εστε']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['αλ', 'αρ', 'εκτελ', 'ζ', 'μ', 'ξ', 'παρακαλ', 'αρ', 'προ', 'νις']:
                    word = word + 'εστ'
                done = True
                break

    ##rule-set 13
    ##χτιστηκε->χτιστ, διαθηκεσ->διαθηκ
    if not done:
        for suffix in ['ηθηκα', 'ηθηκες', 'ηθηκε']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                done = True
                break
    if not done:
        for suffix in ['ηκα', 'ηκες', 'ηκε']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['διαθ', 'θ', 'παρακαταθ', 'προσθ', 'συνθ']:
                    word = word + 'ηκ'
                else:
                    for suffix in ['σκωλ', 'σκουλ', 'ναρθ', 'σφ', 'οθ', 'πιθ']:
                        if ends_with(word, suffix):
                            word = word + 'ηκ'
                            break
                done = True
                break
            
    ##rule-set 14
    ##χτυπουσεσ->χτυπ, μεδουσεσ->μεδουσ
    if not done:
        for suffix in ['ουσα', 'ουσες', 'ουσε']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['φαρμακ', 'χαδ', 'αγκ', 'αναρρ', 'βρομ', 'εκλιπ', 'λαμπιδ', 'λεχ', 'μ', 'πατ', 'ρ', 'λ', 'μεδ', 'μεσαζ',
                            'υποτειν', 'αμ', 'αιθ', 'ανηκ', 'δεσποζ', 'ενδιαφερ', 'δε', 'δευτερευ', 'καθαρευ', 'πλε', 'τσα']:
                    word = word + 'ους'
                else:
                    for s in ['ποδαρ', 'βλεπ', 'πανταχ', 'φρυδ', 'μαντιλ', 'μαλλ', 'κυματ', 'λαχ', 'ληγ', 'φαγ', 'ομ', 'πρωτ'] + VOWELS:
                        if ends_with(word, s):
                            word = word + 'ους'
                            break
                done = True
                break

    ##rule-set 15
    #κολλαγεσ->κολλ, αβασταγα->αβαστ
    if not done:
        for suffix in ['αγα', 'αγες', 'αγε']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['αβαστ', 'πολυφ', 'αδηφ', 'παμφ', 'ρ', 'ασπ', 'αφ', 'αμαλ', 'αμαλλι', 'ανυστ', 'απερ', 'ασπαρ', 'αχαρ',
                            'δερβεν', 'δροσοπ', 'ξεφ', 'νεοπ', 'νομοτ', 'ολοπ', 'ομοτ', 'προστ', 'προσωποπ', 'συμπ', 'συντ', 'τ',
                            'υποτ', 'χαρ', 'αειπ', 'αιμοστ', 'ανυπ', 'αποτ', 'αρτιπ', 'διατ', 'εν', 'επιτ', 'κροκαλοπ', 'σιδηροπ',
                            'λ', 'ναυ', 'ουλαμ', 'ουρ', 'π', 'τρ', 'μ']:
                    word = word + 'αγ'
                else:
                    for s in ['οφ', 'πελ', 'χορτ', 'σφ', 'ρπ', 'φρ', 'πρ', 'λοχ', 'σμην']:
                        # αφαιρεθηκε: 'λλ'
                        if ends_with(word, s):
                            if not word in ['ψοφ', 'ναυλοχ']:
                                word = word + 'αγ'
                            break
                done = True
                break

    ##rule-set 16
    ##αγαπησε->αγαπ, νησου->νησ
    if not done:
        for suffix in ['ησε', 'ησου', 'ησα']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['ν', 'χερσον', 'δωδεκαν', 'ερημον', 'μεγαλον', 'επταν', 'αγαθον']:
                    word = word + 'ης'
                done = True
                break
            
    ##rule-set 17
    ##αγαπηστε->αγαπ, σβηστε->σβηστ
    if not done:
        for suffix in ['ηστε']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['ασβ', 'σβ', 'αχρ', 'χρ', 'απλ', 'αειμν', 'δυσχρ', 'ευχρ', 'κοινοχρ', 'παλιμψ']:
                    word = word + 'ηστ'
                done = True
                break
            
    ##rule-set 18
    ##αγαπουνε->αγαπ, σπιουνε->σπιουν
    if not done:
        for suffix in ['ουνε', 'ησουνε', 'ηθουνε']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['ν', 'ρ', 'σπι', 'στραβομουτς', 'κακομουτς', 'εξων']:
                    word = word + 'OYN'
                done = True
                break
            
    ##rule-set 19
    ##αγαπουμε->αγαπ, φουμε->φουμ
    if not done:
        for suffix in ['ουμε', 'ησουμε', 'ηθουμε']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['παρασους', 'φ', 'χ', 'ωριοπλ', 'αζ', 'αλλοσους', 'ασους']:
                    word = word + 'ουμ'
                done = True
                break
            
    ##rule-set 20
    ##κυματα->κυμ, χωρατο->χωρατ
    if not done:
        for suffix in ['ματα', 'ματων', 'ματος']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                word = word + 'μ'
                done = True
                break
            
    ##rule-set 21
    if not done:
        for suffix in ['ιοντουσαν', 'ιουμαστε', 'ιομασταν', 'ιοσασταν', 'οντουσαν', 'ιοσαστε', 'ιεμαστε', 'ιεσαστε', 'ιομουνα',
                       'ιοσουνα', 'ιουνται', 'ιουνταν', 'ηθηκατε', 'ομασταν', 'οσασταν', 'ουμαστε', 'ιομουν', 'ιονταν', 'ιοσουν',
                       'ηθειτε', 'ηθηκαν', 'ομουνα', 'οσαστε', 'οσουνα', 'ουνται', 'ουνταν', 'ουσατε',  'αγατε', 'ειται', 'ιεμαι',
                       'ιεται', 'ιεσαι', 'ιοταν', 'ιουμα', 'ηθεις', 'ηθουν', 'ηκατε', 'ησατε', 'ησουν', 'ομουν',  'ονται',
                       'ονταν', 'οσουν', 'ουμαι', 'ουσαν',  'αγαν', 'αμαι', 'ασαι', 'αται', 'ειτε', 'εσαι', 'εται', 'ηδες',
                       'ηδων', 'ηθει', 'ηκαν', 'ησαν', 'ησει', 'ησες', 'ομαι', 'οταν',  'αει',  'εις',  'ηθω',  'ησω', 'ουν',
                       'ους',  'αν', 'ας', 'αω', 'ει', 'ες', 'ης', 'οι', 'ον', 'ος', 'ου', 'υς', 'ων', 'ως', 'α', 'ε', 'ι', 'η',
                       'ο',  'υ', 'ω']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                break

    ##rule-set 22
    ##πλησιεστατοσ->πλυσι, μεγαλυτερη->μεγαλ, κοντοτερο->κοντ
    if not done:
        for suffix in ['εστερ', 'εστατ', 'οτερ', 'οτατ', 'υτερ', 'υτατ', 'ωτερ', 'ωτατ']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                break
    
    if len(word.decode("utf-8")) >=3:   
        return word
    return ""


#print stem("γιαγιαδες")