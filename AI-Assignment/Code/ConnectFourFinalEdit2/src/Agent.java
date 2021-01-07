import java.util.Random;
import java.util.*;

public class Agent {
	
	Utils util = new Utils();
	
	// Random Agent
	 public int RandomAgent(TheBoard board) {
		 Random rand = new Random();
		 Vector<Integer> availableMoves = board.getValidMoves();
		 if (availableMoves.size() != 0) {
			 int move = rand.nextInt(availableMoves.size());
			 return availableMoves.get(move);
		 }
		 else return board.cols;
		 
	 }
	 
	 // Simple Agent
	 public int SimpleAgent(TheBoard board,char player) {
		 int move = -1;
		 char opponent;
		 if (player=='r')
			 opponent='b';
		 else 
			 opponent ='r';
		 
		 TheBoard b= board;
		 Vector<Integer> availableMoves = board.getValidMoves();
		 // first check all cols for winning move of player
		 for ( int i=0;i<availableMoves.size();i++)
		 {
			 b= board;
			 if(util.check_winning_move(b,player,availableMoves.get(i))) {
				 move=availableMoves.get(i);
			 }
		 }
		 
		 // if no winning move , then check winning move for opponent
		 if(move == -1) {
		 for ( int i=0;i<availableMoves.size();i++)
		 {
			     b= board;
				 if(util.check_winning_move(b,opponent,availableMoves.get(i))) {
					 move=availableMoves.get(i);
				 }
			 }
		 }
		 
		 // else select random move.
		 if(move ==-1) {
			 move=RandomAgent(board);
		 }	 
		return move;	 
	 }
	 
 public int SimpleAgentleft (TheBoard board) {
	 Vector<Integer> availableMoves = board.getValidMoves();
		 if (availableMoves.size() != 0) {
			 return availableMoves.get(0);
		 }
		 else return board.cols;
			 
	 }
 
 
 
}
