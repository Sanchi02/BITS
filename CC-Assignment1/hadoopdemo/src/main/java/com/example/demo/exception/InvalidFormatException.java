package com.example.demo.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.BAD_REQUEST)
public class InvalidFormatException extends RuntimeException {

	private static final long serialVersionUID = 6386837414057421221L;

	public InvalidFormatException(String message) {
		super(message);
	}
}