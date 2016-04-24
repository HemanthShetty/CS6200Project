package search.engine.test;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

import org.apache.lucene.document.Document;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.ScoreDoc;

public class FileReadWrite {
	
	//Reads Query and converts it to a lost of queries
	static public String[] getQuery(String path,String fileName) throws FileNotFoundException{
		File fin = new File(path);
		StringBuilder filehtmltext= new StringBuilder();
		//Read file line by line
		try {
			BufferedReader br = new BufferedReader(new FileReader(fin));
			String line = null;
			while ((line = br.readLine()) != null) {
				filehtmltext.append(line);
				filehtmltext.append(" ");
			}
			br.close();
		} catch (FileNotFoundException e) {
			throw e;
		} catch (IOException e) {
			e.printStackTrace();
		}
		String htmltext = filehtmltext.toString();
		String[] query = htmltext.split("</DOCNO>");
		String[] newquery = new String[query.length-1];
		int count=0;
		for(String q :query){
			if(count!=0){
				String[] internalText = q.split("</DOC>");
				String text = internalText[0];
				newquery[count-1] = text.trim();
			}
			count++;
		}
		File resultsfile = new File(fileName);
		try{
			if(!resultsfile.getParentFile().exists())
			{
				if (!resultsfile.getParentFile().mkdirs())
					throw new IOException("Unable to create " + resultsfile.getParentFile());
			}

			BufferedWriter out = new BufferedWriter(new FileWriter(resultsfile,false));
		}catch(IOException i){
				i.printStackTrace();
		}
		return newquery;
	}
	
	//Writes results to file 
	static public void writeResult(ScoreDoc[] hits,int qid,IndexSearcher searcher,String fileName){
		File resultsfile = new File(fileName);
		try{
			BufferedWriter out3 = new BufferedWriter(new FileWriter(resultsfile,true));
			for (int i = 0; i < hits.length; ++i) {
				out3.append(String.valueOf(qid));
				out3.append(" ");
				out3.append("Q0");
				out3.append(" ");
				int docId = hits[i].doc;
				Document d = searcher.doc(docId);
				String dpath = d.get("path");
				String[] paths =dpath.split("\\\\");
				dpath = paths[paths.length-1];
				dpath = (dpath.split("\\."))[0];
				out3.append(dpath);
				out3.append(" ");
				out3.append(String.valueOf(i+1));
				out3.append(" ");
				out3.append(String.valueOf(hits[i].score));
				out3.append(" ");
				out3.append("hag");
				out3.newLine();
			}
			out3.close();
		}
		catch(IOException i){
			i.printStackTrace();
		}
	}
	
	
}
