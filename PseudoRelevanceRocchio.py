__author__ = 'Anupam'

import operator
import  math
from Stopping import isStopWord

def tfIdfPRF(doc_score,unigramIndex,queryTerms):
    rel = sorted(doc_score.items(),key=operator.itemgetter(1),reverse=True)[:50]
    rel_docs=[x[0] for x in rel]
    query_expansion_map = {}

    for term in unigramIndex:
        if term not in queryTerms:
            invertedList=unigramIndex[term]
            rel_doc_weight=0.0
            no_of_rel_docs=0.0
            for entry in invertedList:
                docId=entry[0]
                frequency=entry[1]
                docName="CACM-"+str(docId)
                if docName in rel_docs:
                    no_of_rel_docs+=1
                    rel_doc_weight+=frequency
            if (not isStopWord(str(term)))& (no_of_rel_docs > 0) :
                idf = math.log(50/no_of_rel_docs)
                query_expansion_map[str(term)]= (rel_doc_weight*idf)
    expanded_query =sorted(query_expansion_map.items(),key=operator.itemgetter(1),reverse=True)[:20]
    expand_que =[x[0] for x in expanded_query]
    total_list = expand_que+queryTerms
    return total_list