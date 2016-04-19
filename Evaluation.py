
from collections import defaultdict

QUERY_DOCUMENTS_FILE = "../data/cacm.rel"


def readQueryDocumentsRanking():
    query_document = defaultdict(list)

    fp = open(QUERY_DOCUMENTS_FILE, 'r')
    lines = fp.readlines()

    for line in lines:
        q_id,_,doc_id,_ = line.split(' ')

        query_document[int(q_id)].append(doc_id)

    return query_document

def calcQueryPrecision(relevant_docs, docs):
     
    presicion_docs = []
    docs_found = 0
    for n,d in enumerate(docs,start=1):
        if d in relevant_docs:
            docs_found += 1

        p = float(docs_found) / n
        presicion_docs.append(p)

    avg_precision = sum(precision_docs) / len(precision_docs)

    return avg_precision


def calcMeanAvgPrecision(query_relevant_docs, query_results):
    
    avg_queries_precision = []

    # evaluate for every query and relevant documents
    for q_id,relevant_docs in query_relevant_docs.items():
        query_docs = query_results[q_id]
        avg_p = calcQueryPrecision(relevant_docs, query_docs) 

        avg_queries_precision.append(avg_p)

    mean_avg_precision = sum(avg_queries_precision) / len(avg_queries_precision)
    
    return mean_avg_precision

# TODO
def calcPrecisionatK(query_relevant_docs, query_results, k):
    
    return 0


def calcRR(relevant_docs, docs):
    
    for n,d in enumerate(docs,start=1):
        if d in relevant_docs:
            return 1 / float(n)

    return 0

def calcMeanRR(query_relevant_docs, query_results):
    
    docs_RR = []

    # evaluate for every query and relevant documents
    for q_id,relevant_docs in query_relevant_docs.items():
        query_docs = query_results[q_id]

        RR = calcRR(relevant_docs, query_docs)

        docs_RR.append(RR)

    mean_RR = sum(docs_RR) / len(docs_RR)

    return mean_RR

# test
#qc = readQueryDocumentsRanking()
#print qc
