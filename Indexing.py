import re
import io,json,os


charactersToBeRemovedRegex=re.compile('[^a-zA-Z0-9-.,]')
corpusDirectoryName='corpus'
vocabularySize=0
unigramInvertedIndex={}
unigramTokensCountMapping={}
unigramInvertedIndexFile="unigramIndex.txt"
stemIndexFile="stemIndex.txt"
stemInvertedIndex={}
totalNumberOfTokens=0
documentTokenLength={}
content_regex="<pre>(.*)</pre>"
contentPattern=re.compile(content_regex)





def TokenizeArticleContent(textContent):
    textContent = re.sub("\.\.\."," ", textContent)
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
    return caseFoldedContent


def formatPageName(pageName):
    articleTitle=pageName[len("wiki/"):]
    underScoresRemoved = articleTitle.replace("_", "")
    formattedTitle=underScoresRemoved.replace("-","")
    return formattedTitle.replace("/","")

def updateUnigramIndexForDocument(documentTermFrequency,documentID,index):
    if index == 'uni':
        for term in documentTermFrequency:
            if unigramInvertedIndex.has_key(term):
                unigramInvertedIndex[term].append((documentID,documentTermFrequency[term]))
            else:
                unigramInvertedIndex[term]=[(documentID,documentTermFrequency[term])]
    else:
        for term in documentTermFrequency:
            if stemInvertedIndex.has_key(term):
                stemInvertedIndex[term].append((documentID,documentTermFrequency[term]))
            else:
                stemInvertedIndex[term]=[(documentID,documentTermFrequency[term])]

def unigramIndexer(corpusDirectoryName):
    for file in os.listdir(corpusDirectoryName):
        if file.endswith(".html"):
            with open(corpusDirectoryName+"/"+file) as corpusFile:
                documentTermFrequency={}
                tokens=[]
                pageContent=corpusFile.read()
                begin="<pre>"
                end="</pre>"
                startIndex=pageContent.find(begin)
                endIndex=pageContent.find(end,startIndex)
                content=pageContent[startIndex+len(begin):endIndex]
                content= re.sub('\d+[\t]\d+[\t]\d+'," ", content)
                content=TokenizeArticleContent(content)
                textContent = content.split('\n')
                for line in textContent:
                    textLine=line.strip('\n')
                    lineTokens=textLine.split()
                    if lineTokens:
                        tokens=tokens+lineTokens
                documentID=file.split('-')[1].replace(".html",'')
                documentTermFrequency=generateIndexFromTokens(tokens,documentTermFrequency)
                updateUnigramIndexForDocument(documentTermFrequency,documentID,'uni')
        if file.endswith(".txt"):
            with open(corpusDirectoryName+"/"+file) as corpusFile:

                pageContent=corpusFile.read()
                documentText = pageContent.split("#")
                documentText.pop(0)
                count =0
                for fileText in documentText:
                    documentTermFrequency={}
                    tokens=[]
                    count +=1
                    text=str(count)
                    fileText=fileText.split(text+'\n',1)[-1]
                    content=TokenizeArticleContent(fileText)
                    textContent = content.split('\n')
                    for line in textContent:
                        textLine=line.strip('\n')
                        lineTokens=textLine.split()
                        if lineTokens:
                            tokens=tokens+lineTokens
                    documentTermFrequency=generateIndexFromTokens(tokens,documentTermFrequency)
                    updateUnigramIndexForDocument(documentTermFrequency,count,'stem')

    StoreIndex(unigramInvertedIndexFile,unigramInvertedIndex)
    StoreIndex(stemIndexFile,stemInvertedIndex)


def StoreIndex(fileName,filedata):
    with io.open(fileName, 'w', encoding='utf-8') as file:
        file.write(unicode(json.dumps(filedata,sort_keys=True)))

def StoreDatastructures(fileName,filedata):
    with io.open(fileName, 'w', encoding='utf-8') as file:
        file.write(unicode(json.dumps(filedata)))


def generateIndexFromTokens(tokens,documentTermFrequency):
    for token in tokens:
        if documentTermFrequency.has_key(token):
            documentTermFrequency[token]=documentTermFrequency[token]+1
        else:
            documentTermFrequency[token]=1
    return documentTermFrequency

def main():
    unigramIndexer(corpusDirectoryName)


main()



