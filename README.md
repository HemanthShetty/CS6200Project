# CS6200Project
Information Retrieval Project

The input files are assumed to be in relative folder ../data. It can be easily changed using the constants at the beggining of the python files.

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
Models 1,2,4,5,6,7 are implemented in Python, using a sequence of commands for the steps

#TODO
instructions for lucene


******
Python programs

Dependencies:
- PyDictionary: for dictionary and synonyms. Computer has to be on the internet ; it makes web requests to thresaurus.com

There is a sequence of a few python programs which have to be run in order:

1)Indexing.py

To create indexing file run following command,
   example- python Indexing.py

Command takes no argument. data.txt which has the raw crawled documents is presumed to be in the same working directory

After running Indexing.py an index file called unigramIndex.txt and mapping file called docIDMapping.txt are created in the same directory.   

2)RetrievalModels.py

Takes as an argument the system number and run the related retrieval model, reading the queries and the index and producing an output file with the ranking of documents for each query (TREC eval format).

To run the Retrieval Models:
   example- python RetrievalModels.py --sys=1

See table above for all the system options

When running system 5, some error messages might show up. They are from PyDictionary and don't affect the system.

3)Evaluation.py
Takes as an argument the system number and run the evaluation on the related retrieval model. 

To run the Evaluation :
   example- python Evaluation.py --sys=1

To perform the evaluation, relevance judgment is needed. System 7 - with stemming - don't have that information for the queries, so no evaluation metrics can be calculated.  

Outputs the MAP, MRR, P@5 and P@20. Precision and recall tables are saved in a file with the system number.
