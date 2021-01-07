public class Game {
	
	public void playAsPerStrategy(int move, char playerToken, TheBoard board) {
		   
		   board.makeMove(playerToken,move);
		   board.printBoard();
		  // matrix.update_state_action_matrix(board,playerToken, move, 0);
	}

	public int play_game(String player1Strategy, String player2Strategy,TheBoard board,StateActionMatrix matrix1,StateActionMatrix matrix2,double alpha, double gamma, double epsilon,int seed,int actionselection)  {
		
		char redPlayer = 'r';
		char bluePlayer = 'b';
		int playerNum = 0;
		
		Agent agent = new Agent();
		Utils util = new Utils();
		
		Boolean play  =  true;
		while(play) {
			if(playerNum%2==0) {
//				System.out.println("########################## Player 1#################################");
				switch(player1Strategy) {
				case "random":
						playAsPerStrategy(agent.RandomAgent(board), redPlayer, board);
						break;
						
				case "simple":			    
						playAsPerStrategy(agent.SimpleAgentleft(board), redPlayer, board);
						break;
						
				case "q":	
					QLearningAgent qagent = new QLearningAgent(true,matrix1,gamma,alpha,epsilon,seed,actionselection);
					int move=qagent.getAction(board,redPlayer);
					
					double feedback =util.heuristic_score(board,redPlayer,move);
					qagent.UpdateQval(board, redPlayer, feedback);
					playAsPerStrategy(move, redPlayer, board);
					break;
				}
				
				
			}
			else {
//				System.out.println("########################## Player 2#################################");
				switch(player2Strategy) {
				case "random":
						playAsPerStrategy(agent.RandomAgent(board), bluePlayer, board);
						break;
						
				case "simple":
						playAsPerStrategy(agent.SimpleAgentleft(board), bluePlayer, board);
						
					   break;
					   
				case "q":			    
					QLearningAgent qagent = new QLearningAgent(true,matrix2,gamma,alpha,epsilon,seed,actionselection);
					int move=qagent.getAction(board,bluePlayer);
					double feedback =util.heuristic_score(board,bluePlayer,move);
					qagent.UpdateQval(board, bluePlayer, feedback);
					playAsPerStrategy(move, bluePlayer, board);
					break;
				}
				
				
			}
			if(board.lastColDim==board.cols) { 
				//System.out.println("Draw");
				playerNum =-1;
				break;
			}

			if(board.hasWon()) {
				int tmp = playerNum%2;
				//System.out.println(tmp + " Player won");
				break;
			}
			
			
			playerNum += 1;
			
		}
		return playerNum%2;
		
	}
	
	
	
	
	
}
