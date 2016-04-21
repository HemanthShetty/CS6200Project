__author__ = 'Anupam'

import operator
import  math
from Stopping import isStopWord
"Values as per textbook"
alpha =1.0
beta =0.8
gamma =0.1

def Rocchio(doc_score,unigramIndex,queryTerms):
    rel = sorted(doc_score.items(),key=operator.itemgetter(1),reverse=True)[:50]
    rel_docs=[x[0] for x in rel]
    non_rel = sorted(doc_score.items(),key=operator.itemgetter(1),reverse=True)[:200]
    non_rel_docs =[x[0] for x in non_rel]
    query_expansion_map = {}

    for term in unigramIndex:
        query_term_weight =0.0
        non_rel_doc_weight =0.0
        rel_doc_weight=0.0
        no_of_rel_docs=0.0
        no_of_non_rel_docs=0.0
        if term in queryTerms:
            qval = queryTerms.count(term)
            query_term_weight = qval*alpha
        invertedList=unigramIndex[term]
        for entry in invertedList:
            docId=entry[0]
            frequency=entry[1]
            docName="CACM-"+str(docId)
            if docName in rel_docs:
                no_of_rel_docs+=1
                rel_doc_weight = rel_doc_weight+frequency
            else:
                if docName in non_rel_docs:
                    no_of_non_rel_docs+=1
                    non_rel_doc_weight = non_rel_doc_weight +frequency
        if (not isStopWord(str(term)))& (no_of_rel_docs > 0) :
            idf = math.log(50/no_of_rel_docs)
            rel_doc_weight = (rel_doc_weight*idf * beta)/50
        if (not isStopWord(str(term)))& (no_of_non_rel_docs > 0) :
            idf = math.log(150/no_of_non_rel_docs)
            non_rel_doc_weight = (non_rel_doc_weight *idf* gamma)/150
        "Rocchio Algorithm Summation.Store in map if value greater than zero"
        val = query_term_weight + rel_doc_weight - non_rel_doc_weight
        if val > 0:
            query_expansion_map[str(term)] = val

    "Add 10 more terms form rel documents"
    expanded_query =sorted(query_expansion_map.items(),key=operator.itemgetter(1),reverse=True)[:(len(queryTerms)+20)]
    expand_que =[x[0] for x in expanded_query]
    total_list = expand_que+queryTerms
    return expanded_query


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