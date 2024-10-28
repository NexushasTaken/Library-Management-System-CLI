import random

# Records
books_record = []
accounts_record = []

current_login_user = -1


class Account:
  ...
  # name
  # password
  # borrowed books

class Book:
  ...
  # isbn
  # quantity
  # title
  # author


def add_default():
  ...

# admin operations
def add_book():
  ...
def edit_book():
  ...
def remove_book():
  ...
def display_all_account():
  ...

# regular user / admin operations 
def view_book():
  ...
def search_book():
  ...
def borrow_book():
  ...
def display_my_borrowed_books():
  ...
def display_all_books():
  ...

# universal operations
def login():
  ...
def signin():
  ...
def logout():
  ...

# login/signin/logout menu
def main_menu():
  ...
def user_menu():
  ...
def admin_menu():
  ...
