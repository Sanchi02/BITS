package com.example.demo.entity;

import java.util.List;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;

public class QueryInput {

	@NotNull(message = "Columns are required")
	private List<String> select;

	@NotBlank(message = "Func is required")
	private String func;

	@NotBlank(message = "Func Column is required")
	private String funcCol;

	@NotBlank(message = "From is required")
	private String from;

	@NotBlank(message = "Where col is required")
	private String whereCol;

	@NotBlank(message = "Where op is required")
	private String whereOp;

	@NotBlank(message = "Where condition is required")
	private String whereCond;

	@NotBlank(message = "Having op is required")
	private String havOp;

	@NotBlank(message = "Having condition is required")
	private String havCond;

	public QueryInput() {
	}

	public QueryInput(@NotNull(message = "Columns are required") List<String> select,
			@NotBlank(message = "Func is required") String func,
			@NotBlank(message = "Func Column is required") String funcCol,
			@NotBlank(message = "From is required") String from,
			@NotBlank(message = "Where col is required") String whereCol,
			@NotBlank(message = "Where op is required") String whereOp,
			@NotBlank(message = "Where condition is required") String whereCond,
			@NotBlank(message = "Having op is required") String havOp,
			@NotBlank(message = "Having condition is required") String havCond) {
		this.select = select;
		this.func = func;
		this.funcCol = funcCol;
		this.from = from;
		this.whereCol = whereCol;
		this.whereOp = whereOp;
		this.whereCond = whereCond;
		this.havOp = havOp;
		this.havCond = havCond;
	}

	public List<String> getSelect() {
		return select;
	}

	public void setSelect(List<String> select) {
		this.select = select;
	}

	public String getFunc() {
		return func;
	}

	public void setFunc(String func) {
		this.func = func;
	}

	public String getFuncCol() {
		return funcCol;
	}

	public void setFuncCol(String funcCol) {
		this.funcCol = funcCol;
	}

	public String getFrom() {
		return from;
	}

	public void setFrom(String from) {
		this.from = from;
	}

	public String getWhereCol() {
		return whereCol;
	}

	public void setWhereCol(String whereCol) {
		this.whereCol = whereCol;
	}

	public String getWhereOp() {
		return whereOp;
	}

	public void setWhereOp(String whereOp) {
		this.whereOp = whereOp;
	}

	public String getWhereCond() {
		return whereCond;
	}

	public void setWhereCond(String whereCond) {
		this.whereCond = whereCond;
	}

	public String getHavOp() {
		return havOp;
	}

	public void setHavOp(String havOp) {
		this.havOp = havOp;
	}

	public String getHavCond() {
		return havCond;
	}

	public void setHavCond(String havCond) {
		this.havCond = havCond;
	}

	@Override
	public String toString() {
		return "QueryInput [select=" + select + ", func=" + func + ", funcCol=" + funcCol + ", from=" + from
				+ ", whereCol=" + whereCol + ", whereOp=" + whereOp + ", whereCond=" + whereCond + ", havOp=" + havOp
				+ ", havCond=" + havCond + "]";
	}

}
