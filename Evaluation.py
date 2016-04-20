
import getopt
import sys
from collections import defaultdict

QUERY_DOCUMENTS_FILE = "../data/cacm.rel"


def readQueryDocumentsRanking(filename):
    query_document = defaultdict(list)

    fp = open(filename, 'r')
    lines = fp.readlines()

    for line in lines:
        q_id,_,doc_id,_ = line.split(' ')[:4]

        query_document[int(q_id)].append(doc_id)

    fp.close()

    return query_document

def calcQueryPrecision(relevant_docs, docs):
     
    precision_docs = []
    docs_found = 0
    
    for n,d in enumerate(docs,start=1):
        if d in relevant_docs:
            docs_found += 1

        p = float(docs_found) / n
        precision_docs.append(p)

    avg_precision = sum(precision_docs) / len(precision_docs)

    return avg_precision, precision_docs


def calcMeanAvgPrecision(query_relevant_docs, query_results):
    
    avg_queries_precision = []

    # evaluate for every query and relevant documents
    for q_id,relevant_docs in query_relevant_docs.items():
        query_docs = query_results[q_id]
        avg_p,_ = calcQueryPrecision(relevant_docs, query_docs) 

        avg_queries_precision.append(avg_p)

    mean_avg_precision = sum(avg_queries_precision) / len(avg_queries_precision)
    
    return mean_avg_precision


def calcPrecisionAtK(query_relevant_docs, query_results, k):
    precision = []

    # evaluate for every query and relevant documents
    for q_id,relevant_docs in query_relevant_docs.items():
        query_docs = query_results[q_id]
        _,p = calcQueryPrecision(relevant_docs, query_docs)

        precision.append(p[k-1])

    mean_precision = sum(precision) / len(precision)
    
    return mean_precision


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

def main():
    
    try:
        opts,args = getopt.getopt(sys.argv[1:], '', ['sys='])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(-1)
    
    opts = {x[0]:x[1] for x in opts}
    sys_id = int(opts['--sys'])

    if sys_id not in range(1,7) or sys_id == 3:
        print "System number has to be from 1 to 7. 3 is Lucene"
        sys.exit(-1)

    
    sys_filename = "model%d_queries_results.txt" % sys_id 

    sys_results = readQueryDocumentsRanking(sys_filename)
    eval_results = readQueryDocumentsRanking(QUERY_DOCUMENTS_FILE)

    mean_avg_prec = calcMeanAvgPrecision(eval_results, sys_results)
    mRR = calcMeanRR(eval_results, sys_results)
    pAt5 = calcPrecisionAtK(eval_results, sys_results, k=5)
    pAt20 = calcPrecisionAtK(eval_results, sys_results, k=20)

    print "Results for system %d\n" % sys_id 

    print "MAP: \t%f" % mean_avg_prec 
    print "MRR: \t%f" % mRR 
    print "P@5: \t%f" % pAt5 
    print "P@20: \t%f" % pAt20 

if __name__ == '__main__':
    main()
