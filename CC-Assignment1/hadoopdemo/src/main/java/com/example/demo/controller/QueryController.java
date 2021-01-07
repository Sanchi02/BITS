package com.example.demo.controller;

import java.util.List;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.demo.entity.QueryInput;
import com.example.demo.entity.QueryResponse;
import com.example.demo.service.HadoopService;
import com.example.demo.service.QueryBuilderService;
import com.example.demo.service.SparkService;
import com.example.demo.utility.MapValidationErrorService;

@RestController
@RequestMapping("api/query")
public class QueryController {

	@Autowired
	MapValidationErrorService errorService;

	@Autowired
	QueryBuilderService qbSrv;

	@Autowired
	HadoopService hSrv;

	@Autowired
	SparkService spkSrv;

	@PostMapping("")
	public ResponseEntity<?> queryMethod(@Valid @RequestBody QueryInput qInput, BindingResult result) {

		// handle mapping errors
		if (result.hasErrors()) {
			ResponseEntity<?> errorMap = errorService.mapValidationError(result);
			return errorMap;
		}

		// build query from incoming JSON
		String query = qbSrv.buildQuery(qInput);

		// Write query to a file
		qbSrv.writeQueryToFile(query, qInput);

		// Delete HDFS output directory
		hSrv.deleteOutDir();

		// Invoke Hadoop Job
		long htime = hSrv.runJob(qInput.getFunc());

		// Read output file from HDFS
		String hOut = hSrv.readOutFile();

		// Read map output file from HDFS
		List<String> hIntOut = hSrv.readMapOutFile();
		//List<String> hIntOut=Collections.EMPTY_LIST;
		
				
		// Invoke spark script
		spkSrv.runSparkScript();

		// read spark output file
		QueryResponse partialSprkData = spkSrv.readSparkJson();

		// Combine response JSON
		QueryResponse qResp = new QueryResponse();
		qResp.setQuery(query);
		qResp.setHadoopExecTime(htime / 1000000 + " ms");
		qResp.setHadoopResult(hOut);
		qResp.setHadoopIntOut(hIntOut);

		// spark
		qResp.setSparkResult(partialSprkData.getSparkResult());
		qResp.setSparkExecTime(partialSprkData.getSparkExecTime());
		qResp.setSparkIntOut(partialSprkData.getSparkIntOut());
//		qResp.setSparkTransform(partialSprkData.getSparkTransform());

		return new ResponseEntity<QueryResponse>(qResp, HttpStatus.OK);

	}

}
