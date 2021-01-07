package com.example.demo.exception;

public class InvalidFormatExceptionResponse {
	private String errorResponse;

	public InvalidFormatExceptionResponse() {
	}

	public InvalidFormatExceptionResponse(String errorResponse) {
		this.errorResponse = errorResponse;
	}

	public String getErrorResponse() {
		return errorResponse;
	}

	public void setErrorResponse(String errorResponse) {
		this.errorResponse = errorResponse;
	}

}
