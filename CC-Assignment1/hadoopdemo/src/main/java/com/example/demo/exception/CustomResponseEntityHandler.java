package com.example.demo.exception;

import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.HttpMediaTypeNotAcceptableException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.context.request.WebRequest;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

@ControllerAdvice
@RestController
public class CustomResponseEntityHandler extends ResponseEntityExceptionHandler {

	@ExceptionHandler(InvalidFormatException.class)
	public final ResponseEntity<InvalidFormatExceptionResponse> handleStudentIdExceptionResponse(
			InvalidFormatException ex, WebRequest request) {
		InvalidFormatExceptionResponse response = new InvalidFormatExceptionResponse(ex.getMessage());
		return new ResponseEntity<InvalidFormatExceptionResponse>(response, HttpStatus.BAD_REQUEST);
	}

	@Override
	protected ResponseEntity<Object> handleHttpMediaTypeNotAcceptable(HttpMediaTypeNotAcceptableException ex,
			HttpHeaders headers, HttpStatus status, WebRequest request) {
//		System.out.println(headers);
//		System.out.println(request.getHeaderNames());
//		System.out.println(status);
		String s = "acceptable MIME type:" + MediaType.APPLICATION_JSON_VALUE;
		return new ResponseEntity<Object>(s, HttpStatus.NOT_ACCEPTABLE);
	}
}
