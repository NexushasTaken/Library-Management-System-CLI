

class Account:
  def __init__(self, name, password):
    self.name = name
    self.password = password
    self.borrowed_books = []
  def as_str(self):
    return f"{self.name:^26}"


class Book:
  def __init__(self, title, author, isbn, quantity):
    self.title = title
    self.author = author
    self.isbn = isbn
    self.quantity = quantity
  def as_str(self):
    return f" {self.title:^24} | {self.author:^24} | {self.isbn:^4} | {self.quantity:^8} "


# Global Variables
library_books = [
  Book("Physics", "Isaac Newton", 0, 1),
  Book("Math", "3B1B", 1, 2),
  Book("Theory of relativity", "Albert Einstein", 2, 3),
]
registered_users = [
  Account("admin", "admin"),
  Account("isip", "isip"),
  Account("aton", "aton"),
  Account("cortez", "cortez"),
  Account("javier", "javier"),
  Account("geraldyn", "geraldyn"),
]

logged_in_user = None


# Book operations
def add_book():
  print(f"\n{" Adding a new book ":-^71}")
  print("Leave empty and press Enter to return to the Dashboard.")

  while True:
    title  = input("Enter title : ")
    if len(title) == 0: return

    author = input("Enter author: ")
    if len(author) == 0: return

    input_quantity = input("Enter quantity: ")
    if len(input_quantity) == 0: return
    if not input_quantity.isdigit():
      print(f"'{input_quantity}' is not a valid number!")
      continue

    quantity = int(input_quantity)
    if quantity <= 0:
      print(f"Quantity must be greater than 0!")
      continue

    # find the isbn that was not in used
    isbn = 0
    for book in library_books:
      isbn = max(book.isbn, isbn)
    for acc in registered_users:
      for book in acc.borrowed_books:
        isbn = max(book.isbn, isbn)
    isbn += 1

    library_books.append(Book(title, author, isbn, quantity))
    print("New book has been added!")
    break


def edit_book():
  print(f"\n{" Editing the book title and author ":-^71}")
  print("Leave empty and press Enter to return to the Dashboard.")

  while True:
    input_isbn = input("\nEnter ISBN: ")
    if len(input_isbn) == 0: return
    if not input_isbn.isdigit():
      print(f"ISBN must contain only digits.")
      continue

    isbn = int(input_isbn)
    for book in library_books:
      if isbn == book.isbn:
        print("\nLeave empty to keep current info unchanged.")
        title  = input("Enter title : ")
        author = input("Enter author: ")

        book.title = title or book.title
        book.author = author or book.author
        print("Book info has been updated!")
        return

    print(f"A book with '{isbn}' was not found")


def remove_book():
  print(f"\n{" Removing a book ":-^71}")
  print("Leave empty and press Enter to return to the Dashboard.")

  while True:
    input_isbn = input("\nEnter ISBN: ")
    if len(input_isbn) == 0: return
    if not input_isbn.isdigit():
      print(f"ISBN must contain only digits.")
      continue

    isbn = int(input_isbn)
    for book in library_books:
      if isbn == book.isbn:
        while True:
          input_quantity = input(f"Enter Quantity(1-{book.quantity}): ")
          if len(input_quantity) == 0: return
          if not input_quantity.isdigit():
            print(f"'{input_quantity}' is not a valid number!")
            continue

          quantity = int(input_quantity)
          if quantity < 1 or quantity > book.quantity:
            print(f"Please enter a quantity in between 1 and {book.quantity}")
            continue

          book.quantity -= quantity
          if book.quantity == 0:
            library_books.remove(book)

          print(f"{quantity} books has been removed!")
          return

    print(f"A book with '{isbn}' was not found")


def search_book():
  print(f"\n{" Book searching ":-^71}")
  print("Leave empty and press Enter to return to the Dashboard.")

  while True:
    print("Search by title, author, ISBN, or quantity.")

    s = input("Search term: ")
    if len(s) == 0: return

    print(f"{"Search results":-^71}")
    print(f" {"Title":^24} | {"Author":^24} | {"ISBN":^4} | {"Quantity":^8} ")
    print("-" * 71)
    for book in library_books:
      if s.isdigit(): # it's either isbn or quantity
        n = int(s)
        if n == book.isbn or n == book.quantity:
          print(book.as_str())
          continue
      if s in book.title or s in book.author:
        print(book.as_str())
        continue
    print("-" * 71)
    break


def borrow_book():
  print(f"\n{" Borrowing a book ":-^71}")
  print("Leave empty and press Enter to return to the Dashboard.")

  while True:
    input_isbn = input("\nEnter ISBN: ")
    if len(input_isbn) == 0: return
    if not input_isbn.isdigit():
      print(f"ISBN must contain only digits.")
      continue

    isbn = int(input_isbn)

    # A user can only borrow one copy of the same book.
    for book in logged_in_user.borrowed_books:
      if isbn == book.isbn:
        print("You already borrowed this book!")
        return

    for book in library_books:
      if isbn == book.isbn:
        book.quantity -= 1
        if book.quantity == 0:
          library_books.remove(book)

        logged_in_user.borrowed_books.append(Book(book.title, book.author, book.isbn, 1))
        print("Sucessfully borrowed")
        return
    print(f"A book with '{isbn}' was not found")


def return_book():
  if len(logged_in_user.borrowed_books) == 0:
    print("You don't have any borrowed books!")
    return

  print(f"\n{" Returning a book ":-^71}")
  print("Leave empty and press Enter to return to the Dashboard.")

  while True:
    input_isbn = input("\nEnter ISBN: ")
    if len(input_isbn) == 0: return
    if not input_isbn.isdigit():
      print(f"ISBN must contain only digits.")
      continue

    isbn = int(input_isbn)

    for borrowed_book in logged_in_user.borrowed_books:
      if isbn == borrowed_book.isbn:
        entry = None

        for record in library_books:
          if isbn == record.isbn:
            entry = record

        if entry == None:
          library_books.append(Book(borrowed_book.title, borrowed_book.author, borrowed_book.isbn, 1))
        else:
          entry.quantity += 1

        # Assuming each book's quantity is set to one, since a user can only
        # borrow the same book once.
        logged_in_user.borrowed_books.remove(borrowed_book)

        print("Sucessfully returned")
        return
    print(f"A book with '{isbn}' was not found")


# Display operations
def display_all_books():
  print(f"\n{" Available books ":-^71}")
  print(f" {"Title":^24} | {"Author":^24} | {"ISBN":^4} | {"Quantity":^8} ")
  print("-" * 71)
  for book in library_books:
    print(book.as_str())
  print("-" * 71)


def display_all_borrowed_books():
  print(f"\n{" Borrowed Books by users ":-^85}")
  print(f" {"Title":^24} | {"Author":^24} | {"ISBN":^4} | {"Quantity":^8} | {"Borrowed by":^11} ")
  print("-" * 85)
  for acc in registered_users:
    for book in acc.borrowed_books:
      print(book.as_str(), end=f"| {acc.name:^11}")
      print()
  print("-" * 85)


def display_my_borrowed_books():
  if len(logged_in_user.borrowed_books) == 0:
    print("You don't have any borrowed books!")
    return

  print(f"\n{" Borrowed books ":-^71}")
  print(f" {"Title":^24} | {"Author":^24} | {"ISBN":^4} | {"Quantity":^8} ")
  print("-" * 71)
  for book in logged_in_user.borrowed_books:
    print(book.as_str())
  print("-" * 71)


def display_all_account():
  print(f"\n{" Registered Accounts ":-^71}")
  print(f"{"Name":^26}")
  print("-" * 26)
  for acc in registered_users:
    print(acc.as_str())
  print("-" * 26)


# User authentication
def login():
  global logged_in_user

  print(f"\n{" Login ":-^71}")
  print("Leave empty and press Enter to return to the Main Menu.")

  while True:
    username = input("\nEnter username: ")
    if len(username) == 0: return

    password = input("Enter password: ")

    entry = None
    for acc in registered_users:
      if username == acc.name:
        entry = acc

    if entry == None:
      print(f"User '{username}' not found!")
    else:
      if password == entry.password:
        logged_in_user = entry
        if username == "admin":
          admin_dashboard()
        else:
          user_dashboard()
        return
      else:
        print("Invalid password!")


def register():
  print(f"\n{" Register ":-^71}")
  print("Leave empty and press Enter to return to the Main Menu.")

  while True:
    username = input("\nEnter username: ")
    if len(username) == 0: return

    for acc in registered_users:
      if username == acc.name:
        print("This username already exist!")
        return

    print("Empty password is allowed")
    password = input("Enter password: ")

    registered_users.append(Account(username, password))
    print("Account has been Registered!")
    break


# Menus
def main_menu():
  print(f"\n{" Main Menu ":-^71}")
  print("[0] Login")
  print("[1] Register")
  print("[2] Exit")

  match input("Input: "):
    case "0":
      login()
    case "1":
      register()
    case "2":
      print("Exiting...")
      exit()
    case _:
      print("Invalid input!")


def user_dashboard():
  global logged_in_user

  while True:
    print(f"\n{f" Login as {logged_in_user.name} ":-^71}")
    print("[0] Search book")
    print("[1] Borrow book")
    print("[2] Return book")
    print("[3] Display my borrowed books")
    print("[4] Display all books")
    print("[5] Logout")

    match input("Input: "):
      case "0":
        search_book()
      case "1":
        borrow_book()
      case "2":
        return_book()
      case "3":
        display_my_borrowed_books()
      case "4":
        display_all_books()
      case "5":
        logged_in_user = None
        print("Logout...")
        return
      case _:
        print("Invalid input!")


def admin_dashboard():
  global logged_in_user

  while True:
    print(f"\n{f" Admin Dashboard ":-^71}")
    print("[0] Add book")
    print("[1] Edit book")
    print("[2] Remove book")
    print("[3] Search book")
    print("[4] Display all books")
    print("[5] Display all account")
    print("[6] Display all borrowed books")
    print("[7] Logout")

    match input("Input: "):
      case "0":
        add_book()
      case "1":
        edit_book()
      case "2":
        remove_book()
      case "3":
        search_book()
      case "4":
        display_all_books()
      case "5":
        display_all_account()
      case "6":
        display_all_borrowed_books()
      case "7":
        logged_in_user = None
        print("Logout...")
        return
      case _:
        print("Invalid input!")


# Main entry
while True:
  main_menu()

