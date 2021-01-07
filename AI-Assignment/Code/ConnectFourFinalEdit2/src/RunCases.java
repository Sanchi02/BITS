import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.ObjectOutputStream;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Properties;
import java.util.concurrent.Executor;


public class RunCases  {
	
	public static void theExecutor(Double alpha, Double gamma, Double epsilon,int actionselection, int iterations) throws CloneNotSupportedException, IOException, ClassNotFoundException{
		TheBoard board = new TheBoard(5, 6);
		Game game = new Game();
		HashMap<String,Integer> scores = new HashMap<>();
		
		//state matrices for both players
		StateActionMatrix matrix1 = new StateActionMatrix();
		StateActionMatrix matrix2 = new StateActionMatrix();
		
		/* read configuration for the run from properties file */
		File configFile = new File("config.properties");
		//System.out.println(configFile.getAbsolutePath());
		 
		FileReader reader = new FileReader(configFile);
		Properties props = new Properties();
		props.load(reader);
		
		// types of agents.
	    String agent1 = props.getProperty("agent1");
	    String agent2 = props.getProperty("agent2");
	    
	    
		// if agent uses already trained values
		Utils util = new Utils(); 
		
		boolean use_prev_values1 = Boolean.parseBoolean(props.getProperty("use_prev_values1"));
		boolean use_prev_values2 = Boolean.parseBoolean(props.getProperty("use_prev_values2"));
		// load values from file
		if (use_prev_values1) {
			
			File f = new File(props.getProperty("f1")+".ser");
			matrix1.matrix=util.readqvaluesfromfile(f);
			//System.out.println(matrix1.matrix);
			}
		
		if (use_prev_values2) {
			
			File f = new File(props.getProperty("f2")+".ser");
			matrix1.matrix=util.readqvaluesfromfile(f);
		}
	// stats file
		FileWriter fw = new FileWriter(props.getProperty("statsfile"), true);
	    PrintWriter of = new PrintWriter(fw);
		
	    int winner;
	    // intialize scores
	    scores.put("Player1", 0);
	    scores.put("Player2", 0);
	    scores.put("Draw", 0);
	    
	
	    
	    System.out.println("CASE : Agent1: "+agent1+" Agent2: "+agent2);
	    
	    
	    int rows = Integer.parseInt(props.getProperty("rows"));
		int cols = Integer.parseInt(props.getProperty("cols"));
		int seed = Integer.parseInt(props.getProperty("seed"));
		
		for(int i=0; i<iterations; i++) {
//			System.out.println("Iteration num : "+i);
			
			 board = new TheBoard(rows,cols);
			 winner =game.play_game(agent1, agent2, board,matrix1,matrix2,alpha,gamma,epsilon,seed,actionselection);
			 int score;
			 switch(winner){
			 case 0 : 
				      score = scores.get("Player1");
				      scores.replace("Player1",score+1);
				      break;
			 case 1 : 
				      score = scores.get("Player2");
				      scores.replace("Player2",score+1);
				      break;
			      
			 case -1 : 
				      score = scores.get("Draw");
				      scores.replace("Draw",score+1);
				      break;
					 
			 }
			//System.out.println(winner+1);
		}

        System.out.println(scores);
        of.println(agent1+","+agent2+","+scores.get("Player1")+","+scores.get("Player2")+","+scores.get("Draw")+","+alpha+","+gamma+","+epsilon+","+actionselection);
        of.close();

		ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(props.getProperty("output")+".ser"));
		//System.out.println(props.getProperty("output"));
		out.writeObject(matrix1.matrix);
		out.close();
	}

	public static void main(String[] args) throws CloneNotSupportedException, IOException, ClassNotFoundException {
		
		//System.out.println("Starting run");
//		for (int i=0;i<3;i++) {
			//for(double j=0.2;j<1;j=j+0.2) {
				//for(double k=0.25;k<=0.7;k=k+0.05) {
					
					
						//System.out.println(j+" "+k+" "+i);
//						Aplha, gamma, epsilon, strategy
						theExecutor(0.8,0.2,0.0,2,100);
						System.out.println("Finish strategy 1");
//						theExecutor(0.8,0.2,0.0,2,200000);
//						System.out.println("Finish strategy 2");
//						theExecutor(0.8,0.2,0.0,2,300000);
//						System.out.println("Finish strategy3");
//						theExecutor(0.8,0.2,0.0,2,400000);
//						System.out.println("Finish strategy4");
//						theExecutor(0.8,0.2,0.0,2,500000);
//						System.out.println("Finish strategy5");
//						System.out.println("Finish");
				//}
			//}
		//}
		
		
		
	}
}


