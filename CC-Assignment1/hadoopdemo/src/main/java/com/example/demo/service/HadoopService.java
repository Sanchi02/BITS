package com.example.demo.service;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Collections;
import java.util.List;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.springframework.stereotype.Service;

import com.example.demo.hadoop.CountMapper;
import com.example.demo.hadoop.CountReducer;
import com.example.demo.hadoop.MaxMapper;
import com.example.demo.hadoop.MaxReducer;
import com.example.demo.hadoop.MinMapper;
import com.example.demo.hadoop.MinReducer;
import com.example.demo.hadoop.SumMapper;
import com.example.demo.hadoop.SumReducer;

@Service
public class HadoopService {

	private static String uri = "hdfs://localhost:9000/";

	public boolean deleteOutDir() {
		Configuration conf = new Configuration();

		try {
			FileSystem fs = FileSystem.get(URI.create(uri), conf);
			fs.delete(new Path(uri + "output"), true);
			File file = new File("/home/subh/cctemp/hadoopIntOut.txt");
			file.delete();
			return true;
		} catch (Exception e) {

			e.printStackTrace();
			return false;
		}
	}

	public String readOutFile() {
		Configuration conf = new Configuration();
		StringBuilder sb = new StringBuilder();

		try {
			FileSystem fs = FileSystem.get(URI.create(uri), conf);
			FSDataInputStream in = fs.open(new Path(uri + "output/part-r-00000"));

			BufferedReader reader = new BufferedReader(new InputStreamReader(in));

			String line;
			line = reader.readLine();
			while (line != null) {
				sb.append(line);
				sb.append("\n");
				line = reader.readLine();
			}
			reader.close();
			in.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
		return sb.toString();

	}

	public List<String> readMapOutFile() {
		List<String> lines = Collections.emptyList();
		try {
			lines = Files.readAllLines(Paths.get("/home/subh/cctemp/hadoopIntOut.txt"), StandardCharsets.UTF_8);
		} catch (IOException e) {
			e.printStackTrace();
		}
		return lines;
	}

	@SuppressWarnings("deprecation")
	public long runJob(String func) {
		Configuration conf = new Configuration();

		Job job;
		try {
			job = new Job(conf, "HDFS_Map_Reduce");

			job.setJarByClass(HadoopService.class);

			job.setOutputKeyClass(Text.class);
			job.setOutputValueClass(IntWritable.class);

			// change mapper reducer according to func

			if (func.equalsIgnoreCase("count")) {
				job.setMapperClass(CountMapper.class);
				job.setCombinerClass(CountReducer.class);
				job.setReducerClass(CountReducer.class);
			} else if (func.equalsIgnoreCase("min")) {
				job.setMapperClass(MinMapper.class);
				job.setCombinerClass(MinReducer.class);
				job.setReducerClass(MinReducer.class);
			} else if (func.equalsIgnoreCase("Max")) {
				job.setMapperClass(MaxMapper.class);
				job.setCombinerClass(MaxReducer.class);
				job.setReducerClass(MaxReducer.class);
			} else if (func.equalsIgnoreCase("sum")) {
				job.setMapperClass(SumMapper.class);
				job.setCombinerClass(SumReducer.class);
				job.setReducerClass(SumReducer.class);
				job.setOutputValueClass(LongWritable.class);

			}

			FileInputFormat.addInputPath(job, new Path(uri + "input"));
			FileOutputFormat.setOutputPath(job, new Path(uri + "output"));
			long startTime = System.nanoTime();
			job.waitForCompletion(false);
			long stopTime = System.nanoTime();
			return stopTime - startTime;

		} catch (Exception e) {

			e.printStackTrace();
			return 0;
		}
	}

}
