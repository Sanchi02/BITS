package com.example.demo.entity;

import java.util.List;

public class QueryResponse {

	private String query;

	private String hadoopExecTime;

	private String hadoopResult;

	private List<String> hadoopIntOut;

	private String sparkResult;

	private String sparkExecTime;

	private String sparkIntOut;

	public QueryResponse() {
	}

	public QueryResponse(String query, String hadoopExecTime, String hadoopResult, List<String> hadoopIntOut,
			String sparkResult, String sparkExecTime, String sparkIntOut) {
		this.query = query;
		this.hadoopExecTime = hadoopExecTime;
		this.hadoopResult = hadoopResult;
		this.hadoopIntOut = hadoopIntOut;
		this.sparkResult = sparkResult;
		this.sparkExecTime = sparkExecTime;
		this.sparkIntOut = sparkIntOut;
	}

	public String getQuery() {
		return query;
	}

	public void setQuery(String query) {
		this.query = query;
	}

	public String getHadoopExecTime() {
		return hadoopExecTime;
	}

	public void setHadoopExecTime(String hadoopExecTime) {
		this.hadoopExecTime = hadoopExecTime;
	}

	public String getHadoopResult() {
		return hadoopResult;
	}

	public void setHadoopResult(String hadoopResult) {
		this.hadoopResult = hadoopResult;
	}

	public List<String> getHadoopIntOut() {
		return hadoopIntOut;
	}

	public void setHadoopIntOut(List<String> hadoopIntOut) {
		this.hadoopIntOut = hadoopIntOut;
	}

	public String getSparkResult() {
		return sparkResult;
	}

	public void setSparkResult(String sparkResult) {
		this.sparkResult = sparkResult;
	}

	public String getSparkExecTime() {
		return sparkExecTime;
	}

	public void setSparkExecTime(String sparkExecTime) {
		this.sparkExecTime = sparkExecTime;
	}

	public String getSparkIntOut() {
		return sparkIntOut;
	}

	public void setSparkIntOut(String sparkIntOut) {
		this.sparkIntOut = sparkIntOut;
	}

	@Override
	public String toString() {
		return "QueryResponse [query=" + query + ", hadoopExecTime=" + hadoopExecTime + ", hadoopResult=" + hadoopResult
				+ ", hadoopIntOut=" + hadoopIntOut + ", sparkResult=" + sparkResult + ", sparkExecTime=" + sparkExecTime
				+ ", sparkIntOut=" + sparkIntOut + "]";
	}

}
