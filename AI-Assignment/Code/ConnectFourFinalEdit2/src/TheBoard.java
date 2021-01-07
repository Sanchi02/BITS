import java.util.Arrays;
import java.util.*;

public class TheBoard implements Cloneable{
	  final int rows, cols;
	  char[][] board;
	  public int lastRowDim=0, lastColDim=0;

	  public TheBoard(int r, int c) {
	    rows = r;
	    cols = c;
	    board = new char[r][c];
//	    System.out.println("Here");
	    for (int i = 0; i < r; i++) {
	      Arrays.fill(board[i] = new char[c], '-');
	    }
	  }
	  
	  public void printBoard() {
		  String tmp = "";
		  for(int i =rows-1; i>=0; i--) {
			  for(int j = 0; j < cols; j++) {
//				  System.out.println("i=" + i + "   j=" +j);
				  tmp = tmp + board[i][j];
			  }
			  tmp = tmp + "\n";
		  }
	  //System.out.println(tmp);
	  }
	  
	  public char[][] getBoard() {
		  char[][] b = new char[rows][cols];
		  for(int i = 0; i < rows; i++) {
			  for(int j = 0; j < cols; j++) {
//				  System.out.println("i=" + i + "   j=" +j);
				  b[i][j] = board[i][j];
			  }
		  }
		  return b;
	  }
	  
	  public Vector<Integer> getValidMoves() {
		  Vector<Integer> validMoves = new Vector<Integer>();
		  for(int i=0; i<cols; i++) {
			  if(board[rows-1][i] == '-') {
				  validMoves.add(i);
			  }
		  }
		  return validMoves;
	  }
	  
	  public void makeMove(char player, int col) {
		if(col>=cols) {
			lastColDim = col;
			return;
		}
		int row =0;
		//System.out.println(col);
		
			for(int i =0; i<rows; i++) {
				if (board[i][col] == '-') {
					row = i;
					break;
				}
			}
			if(board[row][col] != '-' )
			{
	//			System.out.println("Invalid Move");
			}
			else {
				board[row][col] = player;
				lastRowDim=row;
				lastColDim = col;
				
			}
	   
		
	  }
	  
	  public boolean hasWon() {
		  char sym = board[lastRowDim][lastColDim];
//		  System.out.println("In has won function");
		  String winningPattern = String.format("%c%c%c%c", sym, sym, sym, sym);
		 
//		  Checking the row
//		  System.out.println("Checking rows");
		  String checkRow = "";
		  for(int i=0; i<cols; i++) {
//			  System.out.println("i= " + lastRowDim + "   j= "+ i);
			  checkRow = checkRow + board[lastRowDim][i]; 
		  }
//		  System.out.println("checkrow = " + checkRow);
		  if(checkRow.contains(winningPattern)) {
			  return true;
		  }

//		  Checking the col
//		  System.out.println("checking cols");
		  String checkCol = "";
		  for(int i=0; i<rows;i++) {
			  checkCol = checkCol + board[i][lastColDim];
		  }
		  if(checkCol.contains(winningPattern)) {
			  return true;
		  }
		  
//		  Checking left of right diagonal \
//		  System.out.println("checking LR diagonal");
		  String checkDiagLR = "";
		  int YDim = Math.abs(lastColDim - lastRowDim);
//		  System.out.println("lastColDim = " + lastColDim + "    lastRowDim =" + lastRowDim);
		  for(int i=0; i<rows;i++) {
			  if(YDim < cols) {
//				  System.out.println("i= " + i + "   j= "+YDim);
				  checkDiagLR = checkDiagLR + board[i][YDim];
				  YDim = YDim + 1;
			  }
		  }
		  if(checkDiagLR.contains(winningPattern)) {
			  return true;
		  }

//		  Checking right of left diagonal /
//		  System.out.println("checking RL diagonal");
		  String checkDiagRL = "";
		  YDim = lastColDim + lastRowDim;
		  for(int i=0; i<rows;i++) {
			  if(YDim < cols && YDim >= 0) {
				  checkDiagLR = checkDiagLR + board[i][YDim];
			  }
			  YDim = YDim - 1;
		  }
		  if(checkDiagRL.contains(winningPattern)) {
			  return true;
		  }
		  
		  return false;
	  }
	  

	  public String get_board_config() {
		  char[][] b = this.getBoard();

			
			String state ="";
			for(int i=0;i<rows;i++) {
				for(int j=0;j<cols;j++)
				{
					state= state+b[i][j];
				}
			}
			return state;
	  }
	  

}
