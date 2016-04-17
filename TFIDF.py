import sys
import math
import operator
import json
import re
import os



"less than 1000 because document names overlap after removing - and _ and these files have same content"
N=0
docTokenCountMapping={}
avdl=0
charactersToBeRemovedRegex=re.compile('[^a-zA-Z0-9-.,]')
resultDirectoryName="TFIDF"



def get_term_TFIDF_score(documentFrequency,frequencyOfTermInDocument,docLength):
    termFrequencyWeight=float(frequencyOfTermInDocument)/float(docLength)
    invertedDocumentFrequency=float(math.log(N/documentFrequency))
    score=float(termFrequencyWeight)*float(invertedDocumentFrequency)
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

def writeBM25DocumentScoresToFile(doc_score,queryID):
    sorted_docscore=sorted(doc_score.items(),key=operator.itemgetter(1),reverse=True)[:100]
    doc_rank=1
    file=open(resultDirectoryName+"/"+"query"+queryID+".txt",'w')
    for doc in sorted_docscore:
        file.write(str(queryID)+" "+"Q0 "+doc[0]+" "+str(doc_rank)+" "+str(doc[1])+" Hemanth"+"\n")
        doc_rank+=1
    file.close()

def getListOfQueries(queryFileContent):
    regex=re.compile(r'<DOCNO>(.*?)</DOCNO>(.*?)</DOC>',re.DOTALL)
    queries=re.findall(regex,queryFileContent)
    return queries

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

def main(argv):
    if not os.path.exists(resultDirectoryName):
        os.makedirs(resultDirectoryName)
    if argv:
        index_filename=argv[0]
        query_filename=argv[1]
    else:
        index_filename="unigramIndex.txt"
        query_filename="CACM_QUERY.txt"
    with open(index_filename) as data_file:
        unigramIndex = json.load(data_file)
    "Calculate the total number of documents in the index and the average document length"
    calculateDocumentStatisticsFromIndex(unigramIndex)
    with open(query_filename) as query_content:
        queryEntries=getListOfQueries(query_content.read())
        for queryEntry in queryEntries:
            query=queryEntry[1].rstrip()
            queryID=queryEntry[0]
            queryTerms=tokenizeQuery(query)
            doc_score={}
            distinctQueryTerms=list(set(queryTerms))
            for queryTerm in distinctQueryTerms:
                if unigramIndex.has_key(queryTerm):
                    invertedList=unigramIndex[queryTerm]
                    documentFrequency=len(invertedList)
                    for entry in invertedList:
                        docID=entry[0]
                        docName="CACM-"+str(docID)
                        docLength=docTokenCountMapping[docID]
                        frequencyOfTermInDocument=entry[1]
                        termScore=get_term_TFIDF_score(documentFrequency,frequencyOfTermInDocument,docLength)
                        if doc_score.has_key(docName):
                            doc_score[docName]=doc_score[docName]+termScore
                        else:
                            doc_score[docName]=termScore
            writeBM25DocumentScoresToFile(doc_score,queryID)


main(sys.argv[1:])





