package libsystem;

import java.io.*;
import java.util.*;

public class Transaction {

	static BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
	static Random random = new Random();

	public static void addBook() throws IOException {
		int bookNum, qty, category;
		String title, author;
		System.out.println("\n--------------ADD NEW BOOK---------------");
		System.out.print("Book Number: ");
		bookNum = Integer.parseInt(in.readLine());
		System.out.print("Book Title: ");
		title = in.readLine();
		System.out.print("Book Author: ");
		author = in.readLine();
		System.out.print("Quantity: ");
		qty = Integer.parseInt(in.readLine());

		Category.displayAllBookCategory();
		System.out.print("\nCategory: ");
		category = Integer.valueOf(in.readLine());

		Book.bookRecord.add(new Book(validateISBN(), bookNum, title, author, qty,
				Category.bookCategory.get(category - 1).getCategoryName()));

		System.out.println("__________________________________________");
		System.out.println("|  New Book Has Been Successfully Added! |");
		System.out.println("|________________________________________|\n");

	}

	private static int validateISBN() {
		for (int index = 0; index < Book.bookRecord.size(); index++) {
			int randomNumber = getRandomForISBN(100, 10000);
			if (Book.bookRecord.get(index).getIsbn() != randomNumber) {
				return randomNumber;
			}
		}
		return 0;

	}

	public static void editBook() throws IOException {
		if (Book.bookRecord.size() != 0) {
			String isbn, title, author;
			System.out.print("ISBN: ");
			isbn = in.readLine();
			System.out.print("Title: ");
			title = in.readLine();
			System.out.print("Author: ");
			author = in.readLine();
			for (Book book : Book.bookRecord) {
				if (book.getIsbn() == Integer.valueOf(isbn)) {
					book.setBookTitle(title);
					book.setBookAuthor(author);
					System.out.println("__________________________________________");
					System.out.println("|   Book Has Been Successfully Updated   |");
					System.out.println("|________________________________________|\n");
					return;
				}
			}
			System.out.println("\n>> Book not found!! <<");
		} else {
			System.out.println("\nThere is no book available!!!");
		}
	}

	public static int getRandomForISBN(int min, int max) {
		return random.nextInt(max - min) + min;
	}

	public static void addAccount() throws IOException {
		String username, password;
		System.out.println("\n------------R E G I S T E R--------------");
		System.out.print("Enter username: ");
		username = in.readLine();
		System.out.print("Enter password: ");
		password = in.readLine();

		Account.accountRecord.add(new Account(username, password));

		System.out.println("_________________________________________");
		System.out.println("|New Account Has Been Successfully Added!|");
		System.out.println("|________________________________________|\n");

	}

	public static void removeBook() throws IOException {
		if (Book.bookRecord.size() != 0) {
			String isbn;
			System.out.println("\n---------------DELETE BOOK---------------");
			System.out.print("ISBN: ");
			isbn = in.readLine();
			for (int i = 0; i < Book.bookRecord.size(); ++i) {
				if (Book.bookRecord.get(i).getIsbn() == Integer.valueOf(isbn)) {
					Book.bookRecord.remove(i);
					System.out.println("__________________________________________");
					System.out.println("|    Book Has Been Successfully Remove!  |");
					System.out.println("|________________________________________|\n");
					return;
				}
			}
			System.out.println("\n>> Book not found!! <<");
		} else {
			System.out.println("\nThere is no book available!!!");
		}
	}

	public static void searchBook() throws IOException {
		if (Book.bookRecord.size() != 0) {
			String isbn;
			System.out.println("\n---------------SEARCH BOOK---------------");
			System.out.print("ISBN: ");
			isbn = in.readLine();
			for (int i = 0; i < Book.bookRecord.size(); ++i) {
				if (Book.bookRecord.get(i).getIsbn() == Integer.valueOf(isbn)) {
					System.out.format("\n%-5s %-5s %-14s %-12s %-14s %-10s%n", "ISBN", "BOOK#", "TITLE", "AUTHOR",
							"CATEGORY", "QTY");
					Book.printBookTable(i);
					return;
				}
			}
			System.out.println("\n>> Book not found!! <<");
		} else {
			System.out.println("\nThere is no book available!!!");
		}

	}

	public static void addCategory() throws IOException {
		System.out.println("\n------------ADD NEW CATEGORY-------------");
		String category;
		System.out.print("Category:");
		category = in.readLine();

		Category.bookCategory.add(new Category(category));

		System.out.println("__________________________________________");
		System.out.println("|New Category Has Been Successfully Added|");
		System.out.println("|________________________________________|\n");

	}

	public static void displayAllBorrowedBook() throws IOException {
		Book.displayBorrowedBooks();
	}

	public static void borrowBook(Account user) throws IOException {
		if (Book.bookRecord.size() != 0) {
			int isbn;
			System.out.print("ISBN: ");
			isbn = Integer.valueOf(in.readLine());
			for (int i = 0; i < Book.bookRecord.size(); ++i) {
				if (Book.bookRecord.get(i).getIsbn() == isbn) {
					// Check if the user book borrowing already borrowed
					for (Book e : user.getBorrowedBooks()) {
						if (e.getIsbn() == isbn) {
							return;
						}
					}
					Book book;
					if (Book.bookRecord.get(i).getQty() == 1) {
						book = Book.bookRecord.remove(i);
					} else {
						book = Book.bookRecord.get(i);
						book.setQty(book.getQty() - 1);
					}
					user.getBorrowedBooks().add(new Book(book.getIsbn(), book.getBookNum(), book.getBookTitle(),
							book.getBookAuthor(), 1, book.getBookCategory()));
					System.out.println("__________________________________________");
					System.out.println("|         Successfully Borrowed!         |");
					System.out.println("|________________________________________|\n");
					break;
				}
			}
		} else {
			System.out.println("\nThere is no book available!!!");
		}
	}

	public static void returnBook(Account user) throws IOException {
		if (Book.bookRecord.size() != 0) {
			int isbn;
			System.out.print("ISBN: ");
			isbn = Integer.valueOf(in.readLine());
			for (int i = 0; i < user.getBorrowedBooks().size(); ++i) {
				if (user.getBorrowedBooks().get(i).getIsbn() == isbn) {
					Book book;
					if (user.getBorrowedBooks().get(i).getQty() == 1) {
						book = user.getBorrowedBooks().remove(i);
					} else {
						book = user.getBorrowedBooks().get(i);
						book.setQty(book.getQty() - 1);
					}

					boolean found = false;
					for (Book e : Book.bookRecord) {
						if (e.getIsbn() == isbn) {
							e.setQty(e.getQty() + 1);
							found = true;
							break;
						}
					}
					if (!found)
						Book.bookRecord.add(book);
					System.out.println("__________________________________________");
					System.out.println("|         Successfully Return!           |");
					System.out.println("|________________________________________|\n");
					if (Book.returnedBooks.containsKey(user.getUsername())) {
						Book.returnedBooks.get(user.getUsername()).add(book);
					} else {
						ArrayList<Book> list = new ArrayList<Book>();
						Book.returnedBooks.put(user.getUsername(), list);
						list.add(book);
					}
					return;
				}
			}
			System.out.println("Book not found");
		} else {
			System.out.println("\nThere is no book available!!!");
		}
	}

	public static void displayAllBorrowedBook(Account user) throws IOException {
		for (Book book : user.getBorrowedBooks()) {
			System.out.println(book);
		}
	}

}
