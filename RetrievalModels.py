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

import sys
import getopt
import json
import re
import math
import operator

from PseudoRelevanceRocchio import tfIdfPRF
from QueryExpansion import DictExpandQuery
from Stopping import StopList
from Evaluation import readQueryDocumentsRanking


SYSTEM_OPTIONS = ["","System 1: BM25", "System 2: Tf-idf",
                    "", "System 4: BM25 + query expansion-pseudo relevance",
                    "System 5: BM25 + query expansion: synonyms",
                    "System 6: BM25 + stopping",
                    "System 7: BM25 + stemming","System 8:BM25+QueryExpansion+stopping"]

UNIGRAM_INDEX_FILE = "unigramIndex.txt"
UNIGRAM_STEM_INDEX_FILE = "stemIndex.txt"
QUERY_FILE = "CACM_QUERY.txt"
QUERY_STEM_FILE = "../data/cacm_stem.query.txt"
QUERY_DOCUMENTS_FILE="../data/cacm.rel"


"less than 1000 because document names overlap after removing - and _ and these files have same content"
N=0
docTokenCountMapping={}
avdl=0
charactersToBeRemovedRegex=re.compile('[^a-zA-Z0-9-.,]')



def get_term_TFIDF_score(documentFrequency,frequencyOfTermInDocument,docLength):
    termFrequencyWeight=float(frequencyOfTermInDocument)/float(docLength)
    invertedDocumentFrequency=float(math.log(N/documentFrequency))
    score=float(termFrequencyWeight)*float(invertedDocumentFrequency)
    return score


def get_term_BM25_score(ni,fi,qfi,dl,ri,R):
    k1=1.2
    b=0.75
    k2=100
    score=0.0
    if fi==0:
        score=0.0
    else:
        K=k1*((1-b)+b*float(dl)/float(avdl))
        comp1=(float(N-ni-R+ri+0.5)/float(ni-ri+0.5))*(float(ri+0.5)/float(R-ri+0.5))
        comp2=float((k1+1)*fi)/float(K+fi)
        comp3=float((k2+1)*qfi)/float(k2+qfi)
        score=math.log(comp1)*comp2*comp3
    return score


def calculateDocumentStatisticsFromIndex(index):
    totalNumberOfTokens=0
    for term in index:
        invertedList=index[term]
        for entry in invertedList:
            docId=entry[0]
            frequency=entry[1]
            global docTokenCountMapping
            if docTokenCountMapping.has_key(docId):
                docTokenCountMapping[docId]=docTokenCountMapping[docId]+frequency
                totalNumberOfTokens=totalNumberOfTokens+frequency
            else:
                docTokenCountMapping[docId]=frequency
                totalNumberOfTokens=totalNumberOfTokens+frequency
    global N
    N=len(docTokenCountMapping.keys())
    global avdl
    avdl=totalNumberOfTokens/N


def writeDocumentScoresToFile(doc_score, queryID, fp):
    sorted_docscore = sorted(doc_score.items(),
                                key=operator.itemgetter(1),
                                reverse=True)[:100]
    doc_rank=1

    for doc in sorted_docscore:
        line = ' '.join([str(queryID), "Q0", doc[0], str(doc_rank), str(doc[1]), "hag"])
        fp.write("%s\n" % line)
        doc_rank+=1


def tokenizeQuery(query):
    textContent = re.sub("\.\.\."," ", query)
    textContent = re.sub(charactersToBeRemovedRegex," ", textContent)
    caseFoldedContent=textContent.lower()
    periodPunctuation=re.finditer('[a-zA-Z-][\s\t\r\n\f]*\.',caseFoldedContent)
    for stringSnippet in periodPunctuation:
        start=stringSnippet.start()
        end=stringSnippet.end()
        caseFoldedContent=caseFoldedContent[:start]+stringSnippet.group().replace("."," ")+caseFoldedContent[end:]
    periodPunctuationNumberCase=re.finditer('[0-9][\s\t\r\n\f]*\.[[\s\t\r\n\f]*]*[^0-9]+',caseFoldedContent)
    for stringSnippet in periodPunctuationNumberCase:
          start=stringSnippet.start()
          end=stringSnippet.end()
          caseFoldedContent=caseFoldedContent[:start]+stringSnippet.group().replace("."," ")+caseFoldedContent[end:]
    commaPunctuations=re.finditer('[a-zA-Z-][\s\t\r\n\f]*\,',caseFoldedContent)
    for snippet in commaPunctuations:
         start=snippet.start()
         end=snippet.end()
         caseFoldedContent=caseFoldedContent[:start]+snippet.group().replace(","," ")+caseFoldedContent[end:]
    commaPunctuationsNumberCase=re.finditer('[0-9][\s\t\r\n\f]*\,[\s\t\r\n\f]*[^0-9]+',caseFoldedContent)
    for snippet in commaPunctuationsNumberCase:
          start=snippet.start()
          end=snippet.end()
          caseFoldedContent=caseFoldedContent[:start]+snippet.group().replace(","," ")+caseFoldedContent[end:]
    contentWithoutWhiteSpaces=caseFoldedContent.rstrip('\n')
    queryTokens=contentWithoutWhiteSpaces.split()
    return queryTokens


def readIndex(sys_id):
    index = None

    if sys_id == 7:
        with open(UNIGRAM_STEM_INDEX_FILE) as data_file:
            index = json.load(data_file)
    else:
        with open(UNIGRAM_INDEX_FILE) as data_file:
            index = json.load(data_file)

    return index 

def readQueries(sys_id):
    queries = []

    if sys_id == 7:
        with open(QUERY_STEM_FILE) as queryFileContent:
            for i,line in enumerate(queryFileContent, start=1):
                queries.append((i,line))

    else:
        with open(QUERY_FILE) as queryFileContent:
            regex = re.compile(r'<DOCNO>\s+(.*?)\s+</DOCNO>(.*?)</DOC>',re.DOTALL)
            queries = re.findall(regex,queryFileContent.read())

    return queries


def calculateScore(distinctQueryTerms,index,queryTerms,queryID):
    doc_score={}
    eval_results = readQueryDocumentsRanking(QUERY_DOCUMENTS_FILE)
    queryRelevantDocuments=eval_results[int(queryID)]
    totalNumberOfRelDocs=len(queryRelevantDocuments)
    for queryTerm in distinctQueryTerms:
        if index.has_key(queryTerm):
            invertedList=index[queryTerm]
            documentFrequency=len(invertedList)
            queryFrequency=queryTerms.count(queryTerm)
            relevantDocsWithQueryTerm=0
            for entry in invertedList:
                docID=entry[0]
                docName="CACM-"+str(docID)
                if docName in queryRelevantDocuments:
                    relevantDocsWithQueryTerm=relevantDocsWithQueryTerm+1

            for entry in invertedList:
                docID=entry[0]
                docName="CACM-"+str(docID)
                docLength=docTokenCountMapping[docID]
                frequencyOfTermInDocument=entry[1]
                termScore=get_term_BM25_score(documentFrequency,
                                                        frequencyOfTermInDocument,
                                                        queryFrequency,
                                                        docLength,
                                                        relevantDocsWithQueryTerm,
                                                        totalNumberOfRelDocs)
                if doc_score.has_key(docName):
                    doc_score[docName]=doc_score[docName]+termScore
                else:
                    doc_score[docName]=termScore
    return doc_score


def main():

    try:
        opts,args = getopt.getopt(sys.argv[1:], '', ['sys='])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(-1)
    
    opts = {x[0]:x[1] for x in opts}
    sys_id = int(opts['--sys'])

    if sys_id not in range(1,9) or sys_id == 3:
        print "System number has to be from 1 to 7. 3 is Lucene"
        sys.exit(-1)

    print SYSTEM_OPTIONS[sys_id]

    index = readIndex(sys_id)

    "Calculate the total number of documents in the index and the average document length"
    calculateDocumentStatisticsFromIndex(index)


    outputFile = open("model%d" % sys_id+"_"+"queries_results.txt",'w')

    queries = readQueries(sys_id) 

    for queryID,query in queries:
        queryTerms = tokenizeQuery(query)
        doc_score={}

        # Query expansion - pseudo relevance
        if sys_id == 4:
            score= calculateScore(list(set(queryTerms)),index,queryTerms,queryID)
            queryTerms=tfIdfPRF(score,index,queryTerms)
        # Query expansion - Synonyms
        elif sys_id == 5:
            # 3 synonyms per word found in dictionary
            queryTerms = DictExpandQuery(queryTerms,3)
        elif sys_id == 6:
            index, queryTerms = StopList(index, queryTerms)
        elif sys_id == 8:
            index, queryTerms = StopList(index, queryTerms)
            score= calculateScore(list(set(queryTerms)),index,queryTerms,queryID)
            queryTerms=tfIdfPRF(score,index,queryTerms)

        distinctQueryTerms=list(set(queryTerms))
        eval_results = readQueryDocumentsRanking(QUERY_DOCUMENTS_FILE)
        queryRelevantDocuments=eval_results[int(queryID)]
        totalNumberOfRelDocs=len(queryRelevantDocuments)

        for queryTerm in distinctQueryTerms:
            if index.has_key(queryTerm):
                invertedList=index[queryTerm]
                documentFrequency=len(invertedList)
                relevantDocsWithQueryTerm=0

                for entry in invertedList:
                    docID=entry[0]
                    docName="CACM-"+str(docID)
                    if docName in queryRelevantDocuments:
                        relevantDocsWithQueryTerm=relevantDocsWithQueryTerm+1

                queryFrequency=queryTerms.count(queryTerm)

                for entry in invertedList:
                    docID=entry[0]
                    docName="CACM-"+str(docID)
                    docLength=docTokenCountMapping[docID]
                    frequencyOfTermInDocument=entry[1]

                    if sys_id != 2 and sys_id!=7:
                        termScore=get_term_BM25_score(documentFrequency,
                                                        frequencyOfTermInDocument,
                                                        queryFrequency,
                                                        docLength,relevantDocsWithQueryTerm,totalNumberOfRelDocs)
                    elif sys_id==7:
                        termScore=get_term_BM25_score(documentFrequency,
                                                        frequencyOfTermInDocument,
                                                        queryFrequency,
                                                        docLength,0,0)
                    else:
                        termScore=get_term_TFIDF_score(documentFrequency,
                                                        frequencyOfTermInDocument,
                                                        docLength)


                    if doc_score.has_key(docName):
                        doc_score[docName]=doc_score[docName]+termScore
                    else:
                        doc_score[docName]=termScore

        writeDocumentScoresToFile(doc_score,queryID,outputFile)

    outputFile.close()    


if __name__ == "__main__":
    main()
