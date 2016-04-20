import sys
import getopt
import json
import re
import math
import operator

from PseudoRelevanceRocchio import Rocchio
from QueryExpansion import DictExpandQuery


UNIGRAM_INDEX_FILE = "unigramIndex.txt"
UNIGRAM_STEM_INDEX_FILE = "unigramStemIndex.txt"
QUERY_FILE = "CACM_QUERY.txt"
QUERY_STEM_FILENAME = ""


"less than 1000 because document names overlap after removing - and _ and these files have same content"
N=0
docTokenCountMapping={}
avdl=0
charactersToBeRemovedRegex=re.compile('[^a-zA-Z0-9-.,]')


"""
SYSTEM NUMBERS
1. BM25
2. TFIDF
3. Lucene (not implemented in this script
4. Query expansion(pseudo relevance) + BM25
5. Query expansion(synonyms) + BM25
6. Query expansion(synonyms+stopping) + BM25
7. Stemming + BM25
"""

def get_term_TFIDF_score(documentFrequency,frequencyOfTermInDocument,docLength):
    termFrequencyWeight=float(frequencyOfTermInDocument)/float(docLength)
    invertedDocumentFrequency=float(math.log(N/documentFrequency))
    score=float(termFrequencyWeight)*float(invertedDocumentFrequency)
    return score


def get_term_BM25_score(ni,fi,qfi,dl):
    k1=1.2
    b=0.75
    k2=100
    score=0.0
    if fi==0:
        score=0.0
    else:
        K=k1*((1-b)+b*float(dl)/float(avdl))
        comp1=float(N-ni+0.5)/float(ni+0.5)
        comp2=float((k1+1)*fi)/float(K+fi)
        comp3=float((k2+1)*qfi)/float(k2+qfi)
        score=math.log(comp1)*comp2*comp3
    return score


def calculateDocumentStatisticsFromIndex(unigramIndex):
    totalNumberOfTokens=0
    for term in unigramIndex:
        invertedList=unigramIndex[term]
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
    sorted_docscore = sorted(doc_score.items(),key=operator.itemgetter(1),reverse=True)[:100]
    doc_rank=1

    for doc in sorted_docscore:
        fp.write(str(queryID)+" "+"Q0 "+doc[0]+" "+str(doc_rank)+" "+str(doc[1])+" Hemanth"+"\n")
        doc_rank+=1


def getListOfQueries(queryFileContent):
    regex = re.compile(r'<DOCNO>(.*?)</DOCNO>(.*?)</DOC>',re.DOTALL)
    queries = re.findall(regex,queryFileContent)
    return queries

def getListOfStemmedQueries(queryFileContent):
    #TODO
    return NULL


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


    with open(UNIGRAM_INDEX_FILE) as data_file:
        unigramIndex = json.load(data_file)

    "Calculate the total number of documents in the index and the average document length"
    calculateDocumentStatisticsFromIndex(unigramIndex)

    output_file = open("model%d" % sys_id+"_"+"queries_results.txt",'w')

    with open(QUERY_FILE) as query_content:
        queryEntries=getListOfQueries(query_content.read())

        for queryEntry in queryEntries:
            query=queryEntry[1].rstrip()
            queryID=queryEntry[0]
            queryTerms=tokenizeQuery(query)
            doc_score={}

            if sys_id == 5:
                queryTerms = DictExpandQuery(queryTerms)

            distinctQueryTerms=list(set(queryTerms))

            for queryTerm in distinctQueryTerms:
                if unigramIndex.has_key(queryTerm):
                    invertedList=unigramIndex[queryTerm]
                    documentFrequency=len(invertedList)
                    queryFrequency=queryTerms.count(queryTerm)

                    for entry in invertedList:
                        docID=entry[0]
                        docName="CACM-"+str(docID)
                        docLength=docTokenCountMapping[docID]
                        frequencyOfTermInDocument=entry[1]

                        if sys_id != 2:
                            termScore=get_term_BM25_score(documentFrequency,
                                                            frequencyOfTermInDocument,
                                                            queryFrequency,
                                                            docLength)
                        else:
                            termScore=get_term_TFIDF_score(documentFrequency,
                                                            frequencyOfTermInDocument,
                                                            docLength)


                        if doc_score.has_key(docName):
                            doc_score[docName]=doc_score[docName]+termScore
                        else:
                            doc_score[docName]=termScore

            writeDocumentScoresToFile(doc_score,queryID,output_file)

    output_file.close()    

if __name__ == "__main__":
    main()
