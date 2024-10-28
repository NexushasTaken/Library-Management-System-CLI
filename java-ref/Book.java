package libsystem;

import java.io.PrintStream;
import java.util.ArrayList;
import java.util.HashMap;

public class Book {

	static ArrayList<Book> bookRecord = new ArrayList<>();
	static HashMap<String, ArrayList<Book>> returnedBooks = new HashMap<>();
	private final int isbn;
	private int bookNum, qty;
	private String bookTitle;
	private String bookAuthor;
	private String bookCategory;

	public Book(int isbn, int bookNum, String bookTitle, String bookAuthor, int qty, String bookCategory) {
		this.isbn = isbn;
		this.bookNum = bookNum;
		this.bookTitle = bookTitle;
		this.bookAuthor = bookAuthor;
		this.qty = qty;
		this.bookCategory = bookCategory;
	}

	public int getIsbn() {
		return isbn;
	}

	public int getBookNum() {
		return bookNum;
	}

	public void setBookNum(int bookNum) {
		this.bookNum = bookNum;
	}

	public int getQty() {
		return qty;
	}

	public void setQty(int qty) {
		this.qty = qty;
	}

	public String getBookTitle() {
		return bookTitle;
	}

	public void setBookTitle(String bookTitle) {
		this.bookTitle = bookTitle;
	}

	public String getBookAuthor() {
		return bookAuthor;
	}

	public void setBookAuthor(String bookAuthor) {
		this.bookAuthor = bookAuthor;
	}

	public String getBookCategory() {
		return bookCategory;
	}

	public void setBookCategory(String bookCategory) {
		this.bookCategory = bookCategory;
	}

	public static void displayBooks(int option) {
		if (bookRecord.size() == 0) {
			System.out.println("\nThere is no book available!!!");
		} else {
			if (option == 0) {
				System.out.format("\n%-5s %-5s %-14s %-12s %-14s %-10s%n", "ISBN", "BOOK#", "TITLE", "AUTHOR",
						"CATEGORY", "QTY");
				for (int index = 0; index < bookRecord.size(); index++) {
					printBookTable(index);
				}
			} else {
				String choosenCategory = Category.bookCategory.get(option - 1).getCategoryName();
				System.out.println("\nCATEGORY: " + choosenCategory + "");
				System.out.format("%-5s %-5s %-14s %-12s %-14s %-10s%n", "ISBN", "BOOK#", "TITLE", "AUTHOR", "CATEGORY",
						"QTY");
				for (int index = 0; index < bookRecord.size(); index++) {
					if (bookRecord.get(index).getBookCategory().equals(choosenCategory)) {

						printBookTable(index);
					}
				}
			}
		}
	}

	@Override
	public String toString() {
		return String.format("%-5s %-5s %-14s %-12s %-14s %-10s", getIsbn(),
				getBookNum(), getBookTitle(),
				getBookAuthor(), getBookCategory(),
				getQty());
	}

	public static PrintStream printBookTable(int index) {
		return System.out.printf("%-5s %-5s %-14s %-12s %-14s %-10s%n", bookRecord.get(index).getIsbn(),
				bookRecord.get(index).getBookNum(), bookRecord.get(index).getBookTitle(),
				bookRecord.get(index).getBookAuthor(), bookRecord.get(index).getBookCategory(),
				bookRecord.get(index).getQty());

	}

	public static void displayBorrowedBooks() {
		for (Account account : Account.accountRecord) {
			if (account.getBorrowedBooks().size() != 0) {
				System.out.println("\n----------------BorrowedBooks----------------------");
				System.out.format("\n%-5s %-5s %-14s %-12s %-14s %-10s %-10s %-14s%n",
						"ISBN", "BOOK#", "TITLE", "AUTHOR", "CATEGORY", "QTY", "BORROWED BY", "STATUS");
				for (Book book : account.getBorrowedBooks()) {
					System.out.printf("%s %-10s   NOT YET RETURNED%n", book.toString(), account.getUsername());
				}
			} else {
				System.out.println("\nNO BORROWED BOOK!");
				break;
			}
		}
		for (String key : returnedBooks.keySet()) {
			for (Book book : returnedBooks.get(key)) {
				System.out.printf("%s %-10s   RETURNED%n", book.toString(), key);
			}
		}
		System.out.println("---------------------------------------------------");
	}

}
