# Records
books_record = []
accounts_record = []

current_login_user = None


class Account:
  def __init__(self, name, password):
    self.name = name
    self.password = password
    self.borrowed_books = []
  def __str__(self):
    return f"{self.name:^26}"


class Book:
  def __init__(self, title, author, isbn, quantity):
    self.title = title
    self.author = author
    self.isbn = isbn
    self.quantity = quantity
  def __str__(self):
    return f" {self.title:^24} | {self.author:^24} | {self.isbn:^4} | {self.quantity:^8} "


def add_default_records():
  # default books
  books_record.append(Book("Physics", "Isaac Newton", 0, 1))
  books_record.append(Book("Math", "3B1B", 1, 2))
  books_record.append(Book("Theory of relativity", "Albert Einstein", 2, 3))

  # group members (account)
  accounts_record.append(Account("admin", "admin"))
  accounts_record.append(Account("isip", "isip"))
  accounts_record.append(Account("aton", "aton"))
  accounts_record.append(Account("cortez", "cortez"))
  accounts_record.append(Account("javier", "javier"))
  accounts_record.append(Account("geraldyn", "geraldyn"))


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
    for book in books_record:
      isbn = max(book.isbn, isbn)
    for acc in accounts_record:
      for book in acc.borrowed_books:
        isbn = max(book.isbn, isbn)
    isbn += 1

    books_record.append(Book(title, author, isbn, quantity))
    print("New book has been added!")
    break


def edit_book():
  print(f"\n{" Editing the book title and author ":-^71}")
  print("Leave empty and press Enter to return to the Dashboard.")

  while True:
    input_isbn = input("Enter ISBN: ")
    if len(input_isbn) == 0: return
    if not input_isbn.isdigit():
      print(f"ISBN must contain only digits.")
      continue

    isbn = int(input_isbn)
    for book in books_record:
      if isbn == book.isbn:
        print("Leave empty to keep current info unchanged.")
        title  = input("Enter title : ")
        author = input("Enter author: ")

        book.title = title or book.title
        book.author = author or book.author
        print("Book info has been updated!")
        return


def remove_book():
  print(f"\n{" Removing a book ":-^71}")
  print("Leave empty and press Enter to return to the Dashboard.")

  while True:
    input_isbn = input("Enter ISBN: ")
    if len(input_isbn) == 0: return
    if not input_isbn.isdigit():
      print(f"ISBN must contain only digits.")
      continue

    isbn = int(input_isbn)
    for book in books_record:
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
            books_record.remove(book)

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
    for book in books_record:
      if s.isdigit(): # it's either isbn or quantity
        n = int(s)
        if n == book.isbn or n == book.quantity:
          print(book)
          continue
      if s in book.title or s in book.author:
        print(book)
        continue
    print("-" * 71)
    break


def borrow_book():
  print(f"\n{" Borrowing a book ":-^71}")
  print("Leave empty and press Enter to return to the Dashboard.")

  while True:
    input_isbn = input("Enter ISBN: ")
    if len(input_isbn) == 0: return
    if not input_isbn.isdigit():
      print(f"ISBN must contain only digits.")
      continue

    isbn = int(input_isbn)

    # A user can only borrow one copy of the same book.
    for book in current_login_user.borrowed_books:
      if isbn == book.isbn:
        print("You already borrowed this book!")
        return

    for book in books_record:
      if isbn == book.isbn:
        book.quantity -= 1
        if book.quantity == 0:
          books_record.remove(book)

        current_login_user.borrowed_books.append(Book(book.title, book.author, book.isbn, 1))
        print("Sucessfully borrowed")
        return
    print(f"A book with '{isbn}' was not found")


def return_book():
  if len(current_login_user.borrowed_books) == 0:
    print("You don't have any borrowed books!")
    return

  print(f"\n{" Returning a book ":-^71}")
  print("Leave empty and press Enter to return to the Dashboard.")

  while True:
    input_isbn = input("Enter ISBN: ")
    if len(input_isbn) == 0: return
    if not input_isbn.isdigit():
      print(f"ISBN must contain only digits.")
      continue

    isbn = int(input_isbn)

    for borrowed_book in current_login_user.borrowed_books:
      if isbn == borrowed_book.isbn:
        entry = None

        for record in books_record:
          if isbn == record.isbn:
            entry = record

        if entry == None:
          books_record.append(Book(borrowed_book.title, borrowed_book.author, borrowed_book.isbn, 1))
        else:
          entry.quantity += 1

        # Assuming each book's quantity is set to one, since a user can only
        # borrow the same book once.
        current_login_user.borrowed_books.remove(borrowed_book)

        print("Sucessfully returned")
        return
    print(f"A book with '{isbn}' was not found")


# Display operations
def display_all_books():
  print(f"\n{" Available books ":-^71}")
  print(f" {"Title":^24} | {"Author":^24} | {"ISBN":^4} | {"Quantity":^8} ")
  print("-" * 71)
  for book in books_record:
    print(book)
  print("-" * 71)


def display_all_borrowed_books():
  print(f"\n{" Borrowed Books by users ":-^85}")
  print(f" {"Title":^24} | {"Author":^24} | {"ISBN":^4} | {"Quantity":^8} | {"Borrowed by":^11} ")
  print("-" * 85)
  for acc in accounts_record:
    for book in acc.borrowed_books:
      print(book, end=f"| {acc.name:^11}")
      print()
  print("-" * 85)


def display_my_borrowed_books():
  if len(current_login_user.borrowed_books) == 0:
    print("You don't have any borrowed books!")
    return

  print(f"\n{" Borrowed books ":-^71}")
  print(f" {"Title":^24} | {"Author":^24} | {"ISBN":^4} | {"Quantity":^8} ")
  print("-" * 71)
  for book in current_login_user.borrowed_books:
    print(book)
  print("-" * 71)


def display_all_account():
  print(f"\n{" Registered Accounts ":-^71}")
  print(f"{"Name":^26}")
  print("-" * 26)
  for acc in accounts_record:
    print(acc)
  print("-" * 26)


# User account management
def login():
  global current_login_user

  print(f"\n{" Login ":-^71}")
  print("Leave empty and press Enter to return to the Main Menu.")

  while True:
    username = input("Enter username: ")
    if len(username) == 0: return

    password = input("Enter password: ")

    entry = None
    for acc in accounts_record:
      if username == acc.name:
        entry = acc

    if entry == None:
      print(f"User '{username}' not found!")
    else:
      if password == entry.password:
        current_login_user = entry
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
    username = input("Enter username: ")
    if len(username) == 0: return

    for acc in accounts_record:
      if username == acc.name:
        print("This username already exist!")
        return

    print("Empty password is allowed")
    password = input("Enter password: ")

    accounts_record.append(Account(username, password))
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
  global current_login_user

  while True:
    print(f"\n{f" Login as {current_login_user.name} ":-^71}")
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
        current_login_user = None
        print("Logout...")
        return
      case _:
        print("Invalid input!")


def admin_dashboard():
  global current_login_user

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
        current_login_user = None
        print("Logout...")
        return
      case _:
        print("Invalid input!")


# main entry
add_default_records()
while True:
  main_menu()

