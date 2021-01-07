package com.example.demo.utility;

import java.util.HashMap;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;

@Service
public class MapValidationErrorService {
	public ResponseEntity<?> mapValidationError(BindingResult result) {

		if (result.hasErrors()) {

			HashMap<String, String> errorMap = new HashMap<String, String>();
			for (FieldError fe : result.getFieldErrors()) {
				errorMap.put(fe.getField(), fe.getDefaultMessage());
			}

			return new ResponseEntity<>(errorMap, HttpStatus.BAD_REQUEST);
		} else {
			return null;
		}
	}
}
