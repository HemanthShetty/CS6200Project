import sys
import math
import operator
import json



"less than 1000 because document names overlap after removing - and _ and these files have same content"
N=0
docTokenCountMapping={}
avdl=0



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

def writeBM25DocumentScoresToFile(doc_score,queryID):
    sorted_docscore=sorted(doc_score.items(),key=operator.itemgetter(1),reverse=True)[:100]
    doc_rank=1
    file=open("query"+queryID+".txt",'w')
    for doc in sorted_docscore:
        file.write(str(queryID)+" "+"Q0 "+doc[0].replace(".txt","")+" "+str(doc_rank)+" "+str(doc[1])+" Hemanth"+"\n")
        doc_rank+=1
    file.close()

def main(argv):
    if argv:
        index_filename=argv[0]
        query_filename=argv[1]
    else:
        index_filename="unigramIndex.txt"
        query_filename="queries.txt"
    unigramIndex={}
    docIDMapping={}
    with open(index_filename) as data_file:
        unigramIndex = json.load(data_file)
    with open("docIDMapping.txt") as mapping_file:
        docIDMapping = json.load(mapping_file)
    "Calculate the total number of documents in the index and the average document length"
    calculateDocumentStatisticsFromIndex(unigramIndex)
    with open(query_filename) as query_content:
        queryEntries=query_content.readlines()
        for queryEntry in queryEntries:
            query=queryEntry.split('-')[1].rstrip()
            queryID=queryEntry.split('-')[0]
            queryTerms=query.split(' ')
            doc_score={}
            distinctQueryTerms=list(set(queryTerms))
            for queryTerm in distinctQueryTerms:
                if unigramIndex.has_key(queryTerm):
                    invertedList=unigramIndex[queryTerm]
                    documentFrequency=len(invertedList)
                    queryFrequency=queryTerms.count(queryTerm)
                    for entry in invertedList:
                        docID=entry[0]
                        docName=docIDMapping[str(docID)]
                        docLength=docTokenCountMapping[docID]
                        frequencyOfTermInDocument=entry[1]
                        termScore=get_term_BM25_score(documentFrequency,frequencyOfTermInDocument,queryFrequency,docLength)
                        if doc_score.has_key(docName):
                            doc_score[docName]=doc_score[docName]+termScore
                        else:
                            doc_score[docName]=termScore
            writeBM25DocumentScoresToFile(doc_score,queryID)


main(sys.argv[1:])





