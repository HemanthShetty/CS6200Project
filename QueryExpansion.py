
from PyDictionary import PyDictionary

from Stopping import isStopWord

def DictExpandQuery(q_terms, k=5):
    dic = PyDictionary()
    
    new_terms = []

    for term in q_terms:
        if isStopWord(term):
            continue

        # check if word exists in the dictionary
        w_found = True
        try:
            dic.meaning(term)
        except:
            w_found = False        
            
        # get k first synonyms
        if w_found:
            try:
                synonyms = dic.synonym(term)
            except:
                continue 

            if synonyms == None:
                continue

            if len(synonyms) > k:
                synonyms = synonyms[:k]
            new_terms.extend(synonyms)

    new_query_terms = q_terms + new_terms

    return new_query_terms

if __name__ == '__main__':
    test_query = "global warming potential"

    expanded_query = DictExpandQuery(test_query.split(' '),k=2) 
    print expanded_query
