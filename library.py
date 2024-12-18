import datetime


class Book:
  def __init__(self, title, author, isbn, quantity, due_date=None, borrowed_date=None):
    self.title = title
    self.author = author
    self.isbn = isbn
    self.quantity = quantity
    self.due_date = due_date
    self.borrowed_date = borrowed_date
  def as_str(self):
    return f' {self.title:^24} | {self.author:^24} | {self.isbn:^4} | {self.quantity:^8} '
  def as_str_borrowed(self):
    return f' {self.title:^24} | {self.author:^24} | {self.isbn:^4} | {self.quantity:^8} | {self.due_date.strftime("%b %d, %Y"):^13} | {self.borrowed_date.strftime("%b %d, %Y"):^14} '
  def is_overdue(self):
    return datetime.datetime.now() > self.due_date


class Account:
  def __init__(self, name, password):
    self.name = name
    self.password = password
    self.borrowed_books = []
  def as_str(self):
    return f'{self.name:^26}'


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
  print(f'\n{" Adding a new book ":-^71}')
  print("Leave empty and press Enter to return to the Dashboard.")

  while True:
    title  = input("Enter title : ")
    if len(title) == 0: return

    author = input("Enter author: ")
    if len(author) == 0: return

    input_quantity = input("Enter quantity: ")
    if len(input_quantity) == 0: return
    if not input_quantity.isdigit():
      print(f'"{input_quantity}" is not a valid number!')
      continue

    quantity = int(input_quantity)
    if quantity <= 0:
      print(f'Quantity must be greater than 0!')
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
  print(f'\n{" Editing the book title and author ":-^71}')
  print("Leave empty and press Enter to return to the Dashboard.")

  while True:
    input_isbn = input("\nEnter ISBN: ")
    if len(input_isbn) == 0: return
    if not input_isbn.isdigit():
      print(f'ISBN must contain only digits.')
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

    print(f'A book with "{isbn}" was not found')


def remove_book():
  print(f'\n{" Removing a book ":-^71}')
  print("Leave empty and press Enter to return to the Dashboard.")

  while True:
    input_isbn = input("\nEnter ISBN: ")
    if len(input_isbn) == 0: return
    if not input_isbn.isdigit():
      print(f'ISBN must contain only digits.')
      continue

    isbn = int(input_isbn)
    for book in library_books:
      if isbn == book.isbn:
        while True:
          input_quantity = input(f'Enter Quantity(1-{book.quantity}): ')
          if len(input_quantity) == 0: return
          if not input_quantity.isdigit():
            print(f'"{input_quantity}" is not a valid number!')
            continue

          quantity = int(input_quantity)
          if quantity < 1 or quantity > book.quantity:
            print(f'Please enter a quantity in between 1 and {book.quantity}')
            continue

          book.quantity -= quantity
          if book.quantity == 0:
            library_books.remove(book)

          print(f'{quantity} books has been removed!')
          return

    print(f'A book with "{isbn}" was not found')


def search_book():
  print(f'\n{" Book searching ":-^71}')
  print("Leave empty and press Enter to return to the Dashboard.")

  while True:
    print("Search by title, author, ISBN, or quantity.")

    s = input("Search term: ")
    if len(s) == 0: return

    print(f'{"Search results":-^71}')
    print(f' {"Title":^24} | {"Author":^24} | {"ISBN":^4} | {"Quantity":^8} ')
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
  print(f'\n{" Borrowing a book ":-^71}')
  print("Leave empty and press Enter to return to the Dashboard.")

  while True:
    input_isbn = input("\nEnter ISBN: ")
    if len(input_isbn) == 0: return
    if not input_isbn.isdigit():
      print(f'ISBN must contain only digits.')
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

        now = datetime.datetime.now()
        due_date = now + datetime.timedelta(weeks=1)

        logged_in_user.borrowed_books.append(Book(book.title, book.author, book.isbn, 1, due_date, now))
        print("Sucessfully borrowed")
        return
    print(f'A book with "{isbn}" was not found')


def return_book_by_isbn(isbn):
  for borrowed_book in logged_in_user.borrowed_books:
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


def return_book():
  if len(logged_in_user.borrowed_books) == 0:
    print("You don't have any borrowed books!")
    return

  print(f'\n{" Returning a book ":-^71}')
  print("Leave empty and press Enter to return to the Dashboard.")

  while True:
    input_isbn = input("\nEnter ISBN: ")
    if len(input_isbn) == 0: return
    if not input_isbn.isdigit():
      print(f'ISBN must contain only digits.')
      continue

    isbn = int(input_isbn)

    for borrowed_book in logged_in_user.borrowed_books:
      if isbn == borrowed_book.isbn:
        entry = None
        return_book_by_isbn(isbn)
        print("Sucessfully returned")
        return
    print(f'A book with "{isbn}" was not found')


def validate_books_due_date():
  for book in logged_in_user.borrowed_books:
    if book.is_overdue():
      return_book_by_isbn(book.isbn)
      print(f"The book '{book.title}' has passed the due date, returning automatically.")


# Display operations
def display_all_books():
  print(f'\n{" Available books ":-^71}')
  print(f' {"Title":^24} | {"Author":^24} | {"ISBN":^4} | {"Quantity":^8} ')
  print("-" * 71)
  for book in library_books:
    print(book.as_str())
  print("-" * 71)


def display_all_borrowed_books():
  print(f'\n{" Borrowed Books by users ":-^85}')
  print(f' {"Title":^24} | {"Author":^24} | {"ISBN":^4} | {"Quantity":^8} | {"Date borrowed":^15} | {"Due date":10} | {"Borrowed by":^11}')
  print("-" * 85)
  for acc in registered_users:
    for book in acc.borrowed_books:
      print(book.as_str_borrowed(), end=f"| {acc.name:^11}")
      print()
  print("-" * 85)


def display_my_borrowed_books():
  if len(logged_in_user.borrowed_books) == 0:
    print("You don't have any borrowed books!")
    return

  print(f"\n{' Borrowed books ':-^103}")
  print(f' {"Title":^24} | {"Author":^24} | {"ISBN":^4} | {"Quantity":^8} | {"Date borrowed":^13} | {"Due date":10}')
  print("-" * 103)
  for book in logged_in_user.borrowed_books:
    print(book.as_str_borrowed())
  print("-" * 103)


def display_all_account():
  print(f'\n{" Registered Accounts ":-^71}')
  print(f'{"Name":^26}')
  print("-" * 26)
  for acc in registered_users:
    print(acc.as_str())
  print("-" * 26)


# User authentication
def login():
  global logged_in_user

  print(f'\n{" Login ":-^71}')
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
      print(f'User "{username}" not found!')
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
  print(f'\n{" Register ":-^71}')
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
  print(f'\n{" Main Menu ":-^71}')
  print("1. Login")
  print("2. Register")
  print("3. Exit")

  match input("Input: "):
    case "1":
      login()
    case "2":
      register()
    case "3":
      print("Exiting...")
      exit()
    case _:
      print("Invalid input!")


def user_dashboard():
  global logged_in_user

  while True:
    print(f'\n{f" Login as {logged_in_user.name} ":-^71}')
    validate_books_due_date()
    print("1. Search book")
    print("2. Borrow book")
    print("3. Return book")
    print("4. Display my borrowed books")
    print("5. Display all books")
    print("6. Logout")

    match input("Input: "):
      case "1":
        search_book()
      case "2":
        borrow_book()
      case "3":
        return_book()
      case "4":
        display_my_borrowed_books()
      case "5":
        display_all_books()
      case "6":
        logged_in_user = None
        print("Logout...")
        return
      case _:
        print("Invalid input!")


def admin_dashboard():
  global logged_in_user

  while True:
    print(f'\n{f" Admin Dashboard ":-^71}')
    print("1. Add book")
    print("2. Edit book")
    print("3. Remove book")
    print("4. Search book")
    print("5. Display all books")
    print("6. Display all account")
    print("7. Display all borrowed books")
    print("8. Logout")

    match input("Input: "):
      case "1":
        add_book()
      case "2":
        edit_book()
      case "3":
        remove_book()
      case "4":
        search_book()
      case "5":
        display_all_books()
      case "6":
        display_all_account()
      case "7":
        display_all_borrowed_books()
      case "8":
        logged_in_user = None
        print("Logout...")
        return
      case _:
        print("Invalid input!")


# Main entry
while True:
  main_menu()
