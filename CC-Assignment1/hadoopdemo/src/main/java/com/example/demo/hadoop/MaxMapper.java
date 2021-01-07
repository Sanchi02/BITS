package com.example.demo.hadoop;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import com.example.demo.entity.QueryInput;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

public class MaxMapper extends Mapper<LongWritable, Text, Text, IntWritable> {

	private QueryInput qInput;

	private Text mapkey = new Text();
	private IntWritable funcColVal = new IntWritable();

	@Override
	protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {

		GsonBuilder builder = new GsonBuilder();
		Gson gson = builder.create();
		BufferedReader bufferedReader;
		try {
			bufferedReader = new BufferedReader(new FileReader("/home/subh/cctemp/query.json"));
			qInput = gson.fromJson(bufferedReader, QueryInput.class);

		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}

		JSONParser jsonParser = new JSONParser();
		try {
			FileWriter fw = new FileWriter("/home/subh/cctemp/hadoopIntOut.txt", true);
			JSONObject jsonobject = (JSONObject) jsonParser.parse(value.toString());

			// select clause
			String col = (String) jsonobject.get(qInput.getSelect().get(0));

			// funcCol

			// where clause

			mapkey.set(col);

			boolean flag = false;

			if (qInput.getFuncCol().equals("ProductID") || qInput.getFuncCol().equals("ASIN")
					|| qInput.getFuncCol().equals("salesrank")) {

				// code to check string type col or int type col
				if (qInput.getWhereCol().equals("categories")) {

					JSONArray arrObj = (JSONArray) jsonobject.get(qInput.getWhereCol());

					ArrayList<String> arr = new ArrayList<>();
					for (Object o : arrObj) {
						arr.add((String) o);
					}

					String whereCond = qInput.getWhereCond();

					// only supports = and "contains" for string
					if (qInput.getWhereOp().equals("=") && arr.contains(whereCond)) {
						flag = true;
					} else if (qInput.getWhereOp().equals("contains")) {
						for (String s : arr) {
							if (s.contains(whereCond)) {
								flag = true;
								break;
							}
						}
					}

				} else if (qInput.getWhereCol().equals("title") || qInput.getWhereCol().equals("group")) {
					String s = (String) jsonobject.get(qInput.getWhereCol());
					s = s.trim();

					String whereCond = qInput.getWhereCond();

					// only supports = and "contains" for string
					if (qInput.getWhereOp().equals("=") && s.equals(whereCond)) {
						flag = true;
					} else if (qInput.getWhereOp().equals("contains") && s.contains(whereCond)) {
						// System.out.println("in string comp "+whereCond);
						flag = true;
					}
				} else {
					String s = (String) jsonobject.get(qInput.getWhereCol());
					int val = Integer.parseInt(s.trim());

					int whereCond = Integer.parseInt(qInput.getWhereCond());

					// >,<,=
					if (qInput.getWhereOp().equals("<") && val < whereCond) {
						flag = true;
					} else if (qInput.getWhereOp().equals(">") && val > whereCond) {
						flag = true;
					} else if (qInput.getWhereOp().equals("=") && val == whereCond) {
						flag = true;
					}
				}
			}

			if (flag) {
				String s = (String) jsonobject.get(qInput.getFuncCol());
				int val = Integer.parseInt(s.trim());
				funcColVal.set(val);

				context.write(mapkey, funcColVal);
				fw.write("<" + mapkey.toString() + "," + funcColVal.get() + ">\n");
			}
			fw.close();

		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
