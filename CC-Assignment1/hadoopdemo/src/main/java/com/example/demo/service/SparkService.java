package com.example.demo.service;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import org.springframework.stereotype.Service;

import com.example.demo.entity.QueryResponse;

@Service
public class SparkService {

	private boolean DEBUG = false;

	public void runSparkScript() {
		if (!DEBUG) {
			try {
				Process p = Runtime.getRuntime()
						.exec("/usr/local/spark/bin/spark-submit /home/subh/cctemp/spark/helloSpark.py");
				System.out.println("Spark script exec started");
				p.waitFor();
				System.out.println("Spark script exec done");
				p.destroy();
			} catch (IOException e) {
				e.printStackTrace();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}

	public QueryResponse readSparkJson() {
		if (!DEBUG) {
			QueryResponse qRes = new QueryResponse();
			JSONParser jsonParser = new JSONParser();

			try (FileReader reader = new FileReader("/home/subh/cctemp/spark/sparkop.json")) {
				// Read JSON file
				JSONObject obj = (JSONObject) jsonParser.parse(reader);

				qRes.setSparkResult((String) obj.get("output"));
				qRes.setSparkExecTime((Double) obj.get("timeToE") + " s");
				qRes.setSparkIntOut((String) obj.get("intermediateOp"));

				// qRes.setSparkTransform((String)obj.get("sparkTransform"));

			} catch (FileNotFoundException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			} catch (ParseException e) {
				e.printStackTrace();
			}

			return qRes;
		}else {
			return new QueryResponse();
		}
	}
}
