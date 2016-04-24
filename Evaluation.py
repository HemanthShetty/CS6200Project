"""
SYSTEM NUMBERS
1. BM25
2. TFIDF
3. Lucene (not implemented in this script
4. Query expansion(pseudo relevance) + BM25
5. Query expansion(synonyms) + BM25
6. BM25 + stopping
7. BM25 + stemming
"""


import getopt
import sys
import os
from collections import defaultdict

SYSTEM_OPTIONS = ["","System 1: BM25", "System 2: Tf-idf",
                    "", "System 4: BM25 + query expansion-pseudo relevance",
                    "System 5: BM25 + query expansion: synonyms",
                    "System 6: BM25 + stopping",
                    "System 7: BM25 + stemming"]

QUERY_DOCUMENTS_FILE = "../data/cacm.rel"

OUTPUT_DIR = "output"


class prettyfloat(float):
    def __repr__(self):
        return "%0.2f" % self

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

    return precision_docs


def calcMeanQueryPrecision(relevant_docs, docs):
    precision_docs = []
    docs_found = 0
    
    for n,d in enumerate(docs,start=1):
        if d in relevant_docs:
            docs_found += 1

            p = float(docs_found) / n
            precision_docs.append(p)

    if len(precision_docs) > 0:
        avg_precision = sum(precision_docs) / len(precision_docs)
    else:
        avg_precision = 0

    return avg_precision


def calcQueryRecall(relevant_docs, docs):
    recall_docs = []
    docs_found = 0
    n_docs = len(relevant_docs)
    
    for d in docs:
        if d in relevant_docs:
            docs_found += 1

        r = float(docs_found) / n_docs
        recall_docs.append(r)

    return recall_docs


def calcMeanAvgPrecision(query_relevant_docs, query_results):
    
    avg_queries_precision = []

    # evaluate for every query and relevant documents
    for q_id,relevant_docs in query_relevant_docs.items():
        query_docs = query_results[q_id]
        avg_p = calcMeanQueryPrecision(relevant_docs, query_docs) 

        avg_queries_precision.append(avg_p)

    mean_avg_precision = sum(avg_queries_precision) / len(avg_queries_precision)
    
    return mean_avg_precision


def calcPrecisionAtK(query_relevant_docs, query_results, k):
    precision = []

    # evaluate for every query and relevant documents
    for q_id,relevant_docs in query_relevant_docs.items():
        query_docs = query_results[q_id]
        p = calcQueryPrecision(relevant_docs, query_docs)

        precision.append(p[k-1])

    mean_precision = sum(precision) / len(precision)
    
    return mean_precision


def calcPrecision(query_relevant_docs, query_results):
    precision = defaultdict(list)

    # evaluate for every query and relevant documents
    for q_id,relevant_docs in query_relevant_docs.items():
        query_docs = query_results[q_id]
        p = calcQueryPrecision(relevant_docs, query_docs)

        precision[q_id] = p

    return precision

def calcRecall(query_relevant_docs, query_results):
    recall = defaultdict(list)

    # evaluate for every query and relevant documents
    for q_id,relevant_docs in query_relevant_docs.items():
        query_docs = query_results[q_id]
        r = calcQueryRecall(relevant_docs, query_docs)

        recall[q_id] = r

    return recall


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


def expPrecisionRecallTables(precision, recall, sys_id, results):
    
    filename = os.path.join(OUTPUT_DIR, 
                            "model%d_precision_recall_tables.csv" % sys_id)
    fp = open(filename, 'w')

    fp.write("\"Query ID\", \"Doc ID\", \"Ranking\", \"Precision\", \"Recall\"\n")

    query_ids = precision.keys()
    for q_id in query_ids:
        docs = results[q_id]
        for i,d in enumerate(docs): 
            fp.write(','.join([str(q_id), d, str(i+1),
                                "%.3f" % precision[q_id][i], 
                                "%.3f" % recall[q_id][i]]))
            fp.write("\n")

        #fp.write("Query %d:\n" % q_id)
        #fp.write("Precision: %s\n" % str(map(prettyfloat,precision[q_id])))
        #fp.write("Recall: %s\n\n" % str(map(prettyfloat,recall[q_id])))

    fp.close()

def main():
    
    try:
        opts,args = getopt.getopt(sys.argv[1:], '', ['sys='])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(-1)
    
    opts = {x[0]:x[1] for x in opts}
    sys_id = int(opts['--sys'])

    NO_EVAL_MODELS = [7]
    if sys_id not in range(1,8) or sys_id in NO_EVAL_MODELS:
        print "System number has to be from 1 to 7."
        sys.exit(-1)

    print SYSTEM_OPTIONS[sys_id]

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

    precision = calcPrecision(eval_results, sys_results)
    recall = calcRecall(eval_results, sys_results)
    
    expPrecisionRecallTables(precision, recall, sys_id, sys_results)


if __name__ == '__main__':
    main()
