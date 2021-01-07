package com.example.demo.hadoop;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import com.example.demo.entity.QueryInput;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

public class MaxReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
	private IntWritable result = new IntWritable();

	private QueryInput qInput;

	public void reduce(Text key, Iterable<IntWritable> values, Context context)
			throws IOException, InterruptedException {

		GsonBuilder builder = new GsonBuilder();
		Gson gson = builder.create();
		BufferedReader bufferedReader;
		try {
			bufferedReader = new BufferedReader(new FileReader("/home/subh/cctemp/query.json"));
			qInput = gson.fromJson(bufferedReader, QueryInput.class);

		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}

		int max = Integer.MIN_VALUE;
		for (IntWritable val : values) {
			max = Math.max(val.get(), max);
		}

		boolean flag = false;

		// having condition
		// >,<,=
		int havCond = Integer.parseInt(qInput.getHavCond());

		// >,<,=
		if (qInput.getHavOp().equals("<") && max < havCond) {
			flag = true;
		} else if (qInput.getHavOp().equals(">") && max > havCond) {
			flag = true;
		} else if (qInput.getHavOp().equals("=") && max == havCond) {
			flag = true;
		}

		if (flag) {
			result.set(max);
			context.write(key, result);
		}
	}

}
