package libsystem;

import java.util.ArrayList;

public class Category {

	static ArrayList<Category> bookCategory = new ArrayList<Category>();
	private String categoryName;

	public Category(String category) {
		this.setCategoryName(category);
	}

	public String getCategoryName() {
		return categoryName;
	}

	public void setCategoryName(String categoryName) {
		this.categoryName = categoryName;
	}

	public static void displayAllBookCategory() {
		for (int index = 0; index < bookCategory.size(); index++) {
			System.out.print("\n[" + (index + 1) + "] " + bookCategory.get(index).getCategoryName());
		}
	}

}
