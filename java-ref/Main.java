package libsystem;

import java.io.*;

public class Main {

	static BufferedReader in = new BufferedReader(new InputStreamReader(System.in));

	static int menu;
	static String username, password;

	public static void main(String[] args) throws IOException {
		Account.accountRecord.add(new Account("nexus", "nexus"));
		Category.bookCategory.add(new Category("Programming"));
		Category.bookCategory.add(new Category("Mathematics"));
		Category.bookCategory.add(new Category("Science"));

		Book.bookRecord.add(new Book(1000, 1, "Programming1", "Patrick O.", 5, "Programming"));
		Book.bookRecord.add(new Book(1001, 2, "Programming2", "Janus T.", 3, "Programming"));
		Book.bookRecord.add(new Book(1002, 3, "HCI 1", "Janus T.", 5, "Programming"));
		Book.bookRecord.add(new Book(1004, 1, "Algebra 1", "Emmanuel M.", 5, "Mathematics"));
		Book.bookRecord.add(new Book(243, 1005, "Chemistry 3", "Mendoza S.", 4, "Science"));

		do {
			System.out.println("\n-----------------------------------------");
			System.out.println("--------Library Management System--------");
			System.out.println("-----------------------------------------");
			// LANDING MAIN MENU
			System.out.println("[1] Sign Up");
			System.out.println("[2] Log in");
			System.out.println("[3] Exit");

			switch (validateInput()) {
			case 1:
				Transaction.addAccount();
				break;
			case 2:
				System.out.println("\n---------------L O G I N-----------------");
				System.out.print("Username: ");
				username = in.readLine();
				System.out.print("Password: ");
				password = in.readLine();
				if (username.equals("admin") && password.equals("admin")) {
					adminDashboard();
				}
				for (Account account : Account.accountRecord) {
					if (account.getUsername().equals(username) && account.getPassword().equals(password)) {
						studentDashboard(account);
						break;
					}
				}
				break;
			case 3:
				return;
			}
		} while (true);

	}

	private static void adminDashboard() throws IOException {
		boolean exit = true;
		do {
			System.out.println("\n----------------ADMIN MENU---------------");
			System.out.println("\n-----ADMIN MENU-----");
			System.out.println("[0] Add Book");
			System.out.println("[1] Remove Book");
			System.out.println("[2] View Book");
			System.out.println("[3] Edit Book");
			System.out.println("[4] Search Book");
			System.out.println("[5] View all borrowed");
			System.out.println("[6] Add category");
			System.out.println("[7] View all category");
			System.out.println("[8] View all accounts");
			System.out.println("[9] LOGOUT ");
			switch (validateInput()) {
			case 0:
				Transaction.addBook();
				break;
			case 1:
				Transaction.removeBook();
				break;
			case 2:
				System.out.println("\n----------------VIEW BOOK----------------");
				System.out.println("[1] Per Book Category");
				System.out.println("[2] All Book");
				System.out.println("[0] back");
				switch (validateInput()) {
				case 1:
					Category.displayAllBookCategory();
					System.out.print("\nCategory: ");
					Book.displayBooks(validateInput());
					break;
				case 2:
					Book.displayBooks(0);
					break;
				}
				break;
			case 3:
				Transaction.editBook();
				break;
			case 4:
				Transaction.searchBook();
				break;
			case 5:
				Transaction.displayAllBorrowedBook();
				break;
			case 6:
				Transaction.addCategory();
				break;
			case 7:
				Category.displayAllBookCategory();
				System.out.println();
				break;
			case 8:
				Account.displayAllRegisteredUser();
				break;
			case 9:
				System.out.println("\nTHANK YOU!!!");
				exit = false;
				break;
			}
		} while (exit);
	}

	private static void studentDashboard(Account user) throws IOException {
		boolean exit = true;
		do {
			System.out.println("\n--------------STUDENT MENU---------------");
			System.out.println("[1] Search book");
			System.out.println("[2] Borrow book");
			System.out.println("[3] Return book");
			System.out.println("[4] View books");
			System.out.println("[5] View Categories");
			System.out.println("[6] View My Borrowed Books");
			System.out.println("[7] LOGOUT");
			switch (validateInput()) {
			case 1:
				Transaction.searchBook();
				break;
			case 2:
				Transaction.borrowBook(user);
				break;
			case 3:
				System.out.println("\n---------------RETURN BOOK---------------");
				Transaction.returnBook(user);
				break;
			case 4:
				System.out.println("\n----------------VIEW BOOK----------------");
				System.out.println("[1] Per Book Category");
				System.out.println("[2] All Book");
				System.out.println("[0] back");
				switch (validateInput()) {
				case 1:
					Category.displayAllBookCategory();
					System.out.print("\nCategory: ");
					Book.displayBooks(validateInput());
					break;
				case 2:
					Book.displayBooks(0);
					break;
				}
				break;
			case 5:
				Category.displayAllBookCategory();
				break;
			case 6:
				Transaction.displayAllBorrowedBook(user);
				break;
			case 7:
				exit = false;
				break;
			}
		} while (exit != false);
	}

	private static int validateInput() throws IOException {
		do {
			System.out.print("\nInput: ");
			String input = in.readLine();
			try {
				return Integer.parseInt(input);
			} catch (NumberFormatException e) {
				System.out.println("Invalid Input, Please try again!!!");
			}
		} while (true);

	}

}
