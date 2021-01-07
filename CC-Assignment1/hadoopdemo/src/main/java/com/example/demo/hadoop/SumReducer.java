package com.example.demo.hadoop;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import com.example.demo.entity.QueryInput;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

public class SumReducer extends Reducer<Text, LongWritable, Text, LongWritable> {
	private LongWritable result = new LongWritable();

	private QueryInput qInput;

	public void reduce(Text key, Iterable<LongWritable> values, Context context)
			throws IOException, InterruptedException {

		// System.out.print(key+": [");

		long sum = 0l;

		for (LongWritable val : values) {
			sum += val.get();
			// System.out.print(val+",");
		}
		// System.out.println("\b ]");

		// System.out.println(key+": "+sum);

		GsonBuilder builder = new GsonBuilder();
		Gson gson = builder.create();
		BufferedReader bufferedReader;
		try {
			bufferedReader = new BufferedReader(new FileReader("/home/subh/cctemp/query.json"));
			qInput = gson.fromJson(bufferedReader, QueryInput.class);

		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}

		boolean flag = false;

		// having condition
		// >,<,=
		long havCond = Long.parseLong(qInput.getHavCond());

		// >,<,=
		if (qInput.getHavOp().equals("<") && sum < havCond) {
			flag = true;
		} else if (qInput.getHavOp().equals(">") && sum > havCond) {
			flag = true;
		} else if (qInput.getHavOp().equals("=") && sum == havCond) {
			flag = true;
		}

		if (flag) {
			result.set(sum);
			context.write(key, result);
		}
	}

}
