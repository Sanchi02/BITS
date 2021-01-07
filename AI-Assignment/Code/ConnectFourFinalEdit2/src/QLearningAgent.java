import java.util.Random;
import java.util.*;
//import java.io.*;
//import java.util.LinkedHashMap;
import java.util.HashMap;


public class QLearningAgent 
{
    
    private StateActionMatrix stateMatrix;
    private double explorationQuotient;
    private final double discountFactor;
    private final double learningRate;
    private final int seed;
    private final int actionselection;
    
    private Vector<Integer> sortedActionsAsPerQValues = new Vector<>();
    private HashMap<Integer, Double> actionToQValues = new HashMap<Integer, Double>();

    
    // agent is training then update q matrix 
    boolean training;
    
    public QLearningAgent(boolean train, StateActionMatrix matrix,double gamma, double alpha,double epsilon,int seed,int actionselection)
    {
        this.stateMatrix = matrix;
        this.discountFactor = gamma;
        this.learningRate = alpha;
        this.training = train;
        this.explorationQuotient = epsilon;
        this.seed = seed;
        this.actionselection=actionselection;
    }
    
    public Vector<Integer> sortHashMapByValues(HashMap<Integer, Double> passedMap) {
        List<Integer> mapKeys = new ArrayList<>(passedMap.keySet());
        List<Double> mapValues = new ArrayList<>(passedMap.values());
        Collections.sort(mapValues);
        Collections.sort(mapKeys);

        Vector<Integer> sortedMap =
            new Vector<>();

        Iterator<Double> valueIt = mapValues.iterator();
        while (valueIt.hasNext()) {
            Double val = valueIt.next();
            Iterator<Integer> keyIt = mapKeys.iterator();

            while (keyIt.hasNext()) {
                Integer key = keyIt.next();
                Double comp1 = passedMap.get(key);
                Double comp2 = val;

                if (comp1.equals(comp2)) {
                    keyIt.remove();
                    sortedMap.add(key);
                    break;
                }
            }
        }
        return sortedMap;
    }

    private int getRandomNumberWithinRange(int start, int end) {
    	Random r = new Random();
    	return r.nextInt((end - start) + 1) + start;	
    }
    
    public void getQValsOfAvailableAction(TheBoard board, char Player) {
    	Vector<Integer> actions = board.getValidMoves();
    	if(actions.size()==0) {
    		sortedActionsAsPerQValues.add(board.cols);
    		return;
    	}
    	
    	for (Integer i : actions) {
    		double tmp = stateMatrix.getQ(board, Player, i);
    		actionToQValues.put(i, tmp);
    	}
    	sortedActionsAsPerQValues = sortHashMapByValues(actionToQValues);    	
    }
 
    // calculate softmax probabilities according to the q values.
    
    public HashMap<Integer,Double> calculate_softmax_probabilities(){
    	HashMap<Integer,Double> probs = new HashMap<Integer,Double>();
    	double total =0;
    	for (Double i : actionToQValues.values()) {
    		
    		total = total+i;
    	}
      for (Integer i : actionToQValues.keySet()) {
    		 probs.put(i, Math.exp(actionToQValues.get(i))/Math.exp(total));
    	}
    	return probs;
    }
    
    
    public int getAction(TheBoard board, char Player)
    {
    	getQValsOfAvailableAction(board,Player);

    	if ( explorationQuotient ==0) {
//        	Greedy  		
//    		System.out.println("Here");
    		if(actionselection ==0) {
	    		if(sortedActionsAsPerQValues.size()==0)
	    			return board.cols;
	    		else
	       	 		return sortedActionsAsPerQValues.get(0);
	    		}
    		
   // softmax 		
    		else {
        		int totalAvailableActions = sortedActionsAsPerQValues.size();
        		int randomNum = getRandomNumberWithinRange(1,100);
        		HashMap<Integer,Double> prob= calculate_softmax_probabilities();
        		for( Integer i :sortedActionsAsPerQValues ) {
        	        if (randomNum < (prob.get(i)*100)) {
        	            return i;
        	        }
        		}
        		return board.cols;
        	  }
    		}
       
//    	E-greedy
    	else {
    		int epsilon = (int)(100*explorationQuotient);
    		int totalAvailableActions = sortedActionsAsPerQValues.size();
    		int randomNum = getRandomNumberWithinRange(1,100);

    		if(randomNum > epsilon || totalAvailableActions==1) {
//    			System.out.println("Best chosen");
    			return sortedActionsAsPerQValues.get(0);
    		}
    		else {
//    			System.out.println("Non best chosen");
    			int randomNum2 = getRandomNumberWithinRange(1,totalAvailableActions-1);
    			return sortedActionsAsPerQValues.get(randomNum2);
    		}
    	}
    }

   
    public void UpdateQval(TheBoard board,  char Player,double feedback)
    {
        if (training) {
        	
        	String lastState = board.get_board_config();
        	
        	String last= lastState+board.lastColDim;
        	
            Double lastQ = stateMatrix.matrix.get(last);
            
            int max = getAction(board,Player);
            double maxval = stateMatrix.getQ(board,Player,max);
            if(lastQ== null) {lastQ= 0.0;}
            
            double newQValue =lastQ+ learningRate* (feedback + discountFactor* maxval - lastQ);
            //System.out.println(lastQ+" "+newQValue+" "+learningRate+" "+discountFactor+" "+feedback);
            stateMatrix.update_state_action_matrix(board, Player, max, newQValue);
            
        } 
    }

   
}