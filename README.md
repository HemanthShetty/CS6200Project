# CS6200Project
Information Retrieval Project

Initial Setup
There are two python files which have to be run in order

1)Indexing.py

To create indexing file run following command,
   example- python Indexing.py

Command takes no argument. data.txt which has the raw crawled documents is presumed to be in the same working directory

2)BM25.py

After running Indexing.py an index file called unigramIndex.txt and mapping file called docIDMapping.txt are created in the same directory.   

To get BM25 ranking, run following command,
   example- python BM25.py

a text file known as queries.txt is present in the same working directory. It has the value,
1-global warming potential
2-green power renewable energy
3-solar energy california
4-light bulb bulbs alternative alternatives 

format-> {queryID}-{Query}

Lucene
Run the java file HW3.java in the command line,
In the setup project we need a referance to external jar json-simple-1.1.1.jar
This is because data.txt has json content that needs to be decoded

These two files must be in the current working directory of the java program{they are included in source code},
1)queries.txt- contains queries in this format(no query ID)

global warming potential
green power renewable energy
solar energy california
light bulb bulbs alternative alternatives 

2)data.txt - raw crawled articles in json format
