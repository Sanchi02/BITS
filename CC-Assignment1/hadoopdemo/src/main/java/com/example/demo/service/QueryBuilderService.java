package com.example.demo.service;

import java.io.FileWriter;
import java.io.IOException;

import org.springframework.stereotype.Service;

import com.example.demo.entity.QueryInput;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

@Service
public class QueryBuilderService {

	private static String PATH = "/home/subh/cctemp/";

	public String buildQuery(QueryInput qInput) {
		StringBuilder sb = new StringBuilder("SELECT ");
		for (String s : qInput.getSelect()) {
			sb.append(s + ",");
		}
		// sb.deleteCharAt(sb.length() - 1);

		sb.append(qInput.getFunc() + "(" + qInput.getFuncCol() + ") ");
		sb.append("FROM " + qInput.getFrom() + " ");
		sb.append("WHERE " + qInput.getWhereCol() + " "+qInput.getWhereOp() + " "+qInput.getWhereCond());
		sb.append(" GROUP BY ");
		for (String s : qInput.getSelect()) {
			sb.append(s + ",");
		}
		sb.deleteCharAt(sb.length() - 1);

		sb.append(" HAVING " + qInput.getFunc() + "(" + qInput.getFuncCol() + ")" + qInput.getHavOp()
				+ qInput.getHavCond());

		return sb.toString();
	}

	public boolean writeQueryToFile(String query, QueryInput qInput) {
		try {

			GsonBuilder builder = new GsonBuilder();
			Gson gson = builder.create();
			FileWriter writer = new FileWriter(PATH + "query.json");
			writer.write(gson.toJson(qInput));
			writer.close();

			FileWriter myWriter = new FileWriter(PATH + "query.txt");
			myWriter.write(query);
			myWriter.close();
			return true;
		} catch (IOException e) {
			System.out.println("An error occurred.");
			e.printStackTrace();
			return false;
		}
	}
}
