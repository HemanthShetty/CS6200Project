
from PyDictionary import PyDictionary


def DictExpandQuery(query):
    dic = PyDictionary()
    
    q_terms = query.split(' ')
    new_terms = []

    for term in q_terms:
        w_found = True
        try:
            dic.meaning(term)
        except:
            w_found = False        
            
        if w_found:
            synonyms = dic.synonym(term)
            new_terms.extend(synonyms)

    new_query_terms = query + ' ' + ' '.join(new_terms)

    return new_query_terms

if __name__ == '__main__':
    test_query = "global warming potential"

    expanded_query = DictExpandQuery(test_query) 
    print expanded_query
