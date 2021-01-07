import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.util.HashMap;

public class Utils {

	
	public HashMap readqvaluesfromfile(File f) throws IOException, ClassNotFoundException {
		  
        FileInputStream fis=new FileInputStream(f);
        ObjectInputStream ois=new ObjectInputStream(fis);

        HashMap<String,Double> matrix=(HashMap<String, Double>)ois.readObject();
        ois.close();
        fis.close();
        return matrix;
	}
	public boolean check_winning_move( TheBoard board, char player,int col ) {
		//System.out.println("checking winning move");

		board.makeMove(player,col);
		char[][] b = board.getBoard();
		// horizontal
		for( int i = 0; i < board.rows; i++){ 
			for ( int j= 0; j< board.cols-3; j++){ 
				int count = 0;
				for (int k= j ; k< j+3;k++) {

					if (b[i][k] == player) {
						count++;
					}
					if (count == 3) { return true;} 
				}
			}

		}
		//vertical
		for( int i = 0; i < board.rows-3; i++){ 
			for ( int j= 0; j< board.cols; j++){ 
				int count = 0;
				for (int k= i ; k< i+3;k++) {

					if (b[k][j] == player) {
						count++;
					}

					if (count == 3) { return true;} 
				}
			}

		}


		// LR diagonal
		for( int i = 0; i < board.rows-3; i++){ 
			for ( int j= 0; j< board.cols-3; j++){ 
				int count = 0;
				for (int k= i ; k< i+3;k++) {
					for (int l= j ; l< j+3;l++) {

						if (b[k][l] == player) {
							count++;
						}
						if (count == 3) { return true;} 
					}
				}
			}

		}

		// RL diagonal
		for( int i =3 ; i < board.rows-3; i++){ 
			for ( int j= 0; j< board.cols-3; j++){ 
				int count = 0;
				for (int k= i ; k > i-4;k--) {
					for (int l= j ; l< j+3;l++) {

						if (b[k][l] == player) {
							count++;
						}
						if (count == 3) { return true;} 
					}
				}
			}

		}

		return false;
	}

	/****one step look ahead heuristic**************/

	// counts number of configurations(like 3 in a row or 4 in a row) satisfying heuristic conditions( one step look ahead)

	public int count_config(TheBoard board,int num,char player ) {
		int num_config = 0;
		int count=0, count1=0; // for counting number of 'r'/'b' and  number of '-' in the configuration

		char[][] b = board.getBoard();
		// horizontal configurations
		for( int i = 0; i < board.rows; i++){ 
			for ( int j= 0; j< board.cols-3; j++){ 
				count = 0;
				count1=0;
				for (int k= j ; k< j+3;k++) {
					if (b[i][k] == player) {
						count++;
					}
					if(b[i][k]=='-') {
						count1++;
					}
					if (count == num && count1== 4-num) { num_config++;} 
				}
			}

		}

		//vertical
		for( int i = 0; i < board.rows-3; i++){ 
			for ( int j= 0; j< board.cols; j++){ 
				count = 0;
				count1=0;
				for (int k= i ; k< i+3;k++) {

					if (b[k][j] == player) {
						count++;
					}

					if(b[i][k]=='-') {
						count1++;
					}
					if (count == num && count1== 4-num) { num_config++;} 

				}
			}

		}


		// LR diagonal
		for( int i = 0; i < board.rows-3; i++){ 
			for ( int j= 0; j< board.cols-3; j++){ 
				count = 0;
				count1=0;
				for (int k= i ; k< i+3;k++) {
					for (int l= j ; l< j+3;l++) {

						if (b[k][l] == player) {
							count++;
						}
						if(b[i][k]=='-') {
							count1++;
						}
						if (count == num && count1== 4-num) { num_config++;} 

					}
				}
			}

		}

		// RL diagonal
		for( int i =3 ; i < board.rows-3; i++){ 
			for ( int j= 0; j< board.cols-3; j++){ 
				count = 0;
				count1=0;
				for (int k= i ; k > i-4;k--) {
					for (int l= j ; l< j+3;l++) {

						if (b[k][l] == player) {
							count++;
						}
						if(b[i][k]=='-') {
							count1++;
						}
						if (count == num && count1== 4-num) { num_config++;} 

					}
				}
			}

		}

		return num_config;
	}

	// calculates heuristic score 
	public double heuristic_score(TheBoard b, char player,int move)  {

		char[][] brd = makeMove(b,player,move);
		TheBoard b1 = new TheBoard(b.rows,b.cols);
		b1.board = brd;
		//b.makeMove(player,move);
		char opp;
		if (player=='r') opp='b';
		else opp ='r';

		int num_threes = count_config(b, 3, player);
		int num_fours = count_config(b, 4, player);
		int num_threes_opp = count_config(b, 3,opp);
		int num_fours_opp = count_config(b, 4, player);

		double score = (num_threes) - 1.2*(num_threes_opp) + 1.5*(num_fours) - 1.8*(num_fours_opp);
		return score;
	}

	// for making a temporary move and to get heuristic score

	public char[][] makeMove(TheBoard b,char player, int col) {
		char[][] brd = b.getBoard();
		int row = 0;
		//System.out.println(col);
		if(col < b.cols) {
		for(int i =0; i<b.rows; i++) {
			if (brd[i][col] == '-') {
				row = i;
				break;
			}
		}
		brd[row][col] = player;
		}
		return brd;
	}

}
