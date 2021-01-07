import java.util.HashMap;

public class StateActionMatrix {

	 
	  HashMap <String, Double> matrix = new HashMap <String, Double>();
	 
	  public void update_state_action_matrix(TheBoard brd,char player,int move,double qvalue ) {
			
		    Utils util = new Utils();
		    double score = util.heuristic_score(brd,player,move);
		    String state = brd.get_board_config();
			state = state + move;
			if(matrix.containsKey(state)) {
				matrix.put(state, qvalue);
			}
			else {
			matrix.put(state, score);
			}

		}
	  public double getQ(TheBoard board,char player, int action)
	    {
		   String state = board.get_board_config();
		   state = state + action;
		   Double value;
		   Utils util = new Utils();
		   
		   if(matrix.containsKey(state)) {
			   value = matrix.get(state);
			}
		   else {
			   value = util.heuristic_score(board,player,action);
		   }
	        return value;
	    }

	
	  
}
