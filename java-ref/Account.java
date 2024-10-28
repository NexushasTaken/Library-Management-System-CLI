package libsystem;

import java.util.ArrayList;

public class Account extends Transaction{

	static ArrayList<Account> accountRecord = new ArrayList<Account>();
	private ArrayList<Book> myBorrowedBooks;
	private String username;
	private String password;

	public String getUsername() {
		return username;
	}

	public void setUsername(String username) {
		this.username = username;
	}

	public String getPassword() {
		return password;
	}

	public void setPassword(String password) {
		this.password = password;
	}

	public Account(String username, String password) {
		this.username = username;
		this.password = password;
		this.myBorrowedBooks = new ArrayList<Book>();
	}
	
	public ArrayList<Book> getBorrowedBooks(){
		return this.myBorrowedBooks;
	}

	public static void displayAllRegisteredUser() {
		System.out.println("\n--------------LIST OF USER---------------");
		System.out.format("\n%-10s%n", "List of User: ");
		for (int index = 0; index < accountRecord.size(); index++) {
			System.out.printf("%-10s%n", accountRecord.get(index).getUsername());
		}
	}

}
