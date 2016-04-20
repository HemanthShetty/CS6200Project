# CS6200Project
Information Retrieval Project

There are 7 retrieval systems implemented in this project, as follows:
SYSTEM NUMBERS
1. BM25
2. TFIDF
3. Lucene (not implemented in this script
4. Query expansion(pseudo relevance) + BM25
5. Query expansion(synonyms) + BM25
6. BM25 + stopping
7. BM25 + stemming

Model 3 uses Lucene and is implemented in Java.

#TODO
instructions for lucene

All the other models are implemented in python and the instructions to run them are provided below.

******
Python programs

Dependencies:
- PyDictionary: for dictionary and synonyms. Computer has to be on the internet as it makes web requests

There is a sequence of a few python files which have to be run in order:

1)Indexing.py

To create indexing file run following command,
   example- python Indexing.py

Command takes no argument. data.txt which has the raw crawled documents is presumed to be in the same working directory

After running Indexing.py an index file called unigramIndex.txt and mapping file called docIDMapping.txt are created in the same directory.   

2)RetrievalModels.py

Takes as an argument the system number and run the related retrieval model, reading the queries and the index and producing an output file with the ranking of documents for each query (TREC eval format)

To run the Retrieval Models:
   example- python RetrievalModels.py --sys=1

3)Evaluation.py
Takes as an argument the system number and run the evaluation on the related retrieval model. 

To run the Evaluation :
   example- python Evaluation.py --sys=1
