__author__ = 'Anupam'

"Values as per textbook"
alpha =8
beta =16
gamma =4

def Rocchio(doc_score,unigramIndex,queryTerms):
    rel_docs = sorted(doc_score.items(),key=operator.itemgetter(1),reverse=True)[:50]
    non_rel = sorted(doc_score.items(),key=operator.itemgetter(1),reverse=True)[:200]
    query_expansion_map = {}

    for term in unigramIndex:
        query_term_weight =0.0
        rel_doc_weight =0.0
        non_rel_doc_weight =0.0
        if term in queryTerms:
            qval = queryTerms.count(term)
            query_term_weight = qval*alpha
        invertedList=unigramIndex[term]
        for entry in invertedList:
            docId=entry[0]
            frequency=entry[1]
            if docId in rel_docs:
                rel_doc_weight = rel_doc_weight+frequency
            else:
                if docId in non_rel:
                    non_rel_doc_weight = non_rel_doc_weight +frequency
        rel_doc_weight = (rel_doc_weight * beta)/50
        non_rel_doc_weight = (non_rel_doc_weight * gamma)/150
        "Rocchio Algorithm Summation.Store in map if value greater than zero"
        val = query_term_weight + rel_doc_weight - non_rel_doc_weight
        if val > 0:
            query_expansion_map[term] = val

    "Add 10 more terms form rel documents"
    expanded_query =sorted(query_expansion_map.items(),key=operator.itemgetter(1),reverse=True)[:(len(queryTerms)+10)]

    return expanded_query