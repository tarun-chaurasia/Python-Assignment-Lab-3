# Name = Tarun Kumar Chaurasia
# Roll no = 2501350067

import csv
from abc import ABC, abstractmethod


class LibraryItem(ABC):
    def __init__(self, title, author, isbn):
        self._title = title
        self._author = author
        self._isbn = isbn
        self._status = "available"

    @abstractmethod
    def display_info(self):
        pass

    def get_status(self):
        return self._status

    def issue(self):
        if self._status == "available":
            self._status = "issued"
            return True
        return False

    def return_book(self):
        if self._status == "issued":
            self._status = "available"
            return True
        return False


class Book(LibraryItem):
    def display_info(self):
        return f"[BOOK] Title: {self._title}, Author: {self._author}, ISBN: {self._isbn}, Status: {self._status}"


class DigitalBook(Book):
    def display_info(self):
        return f"[E-BOOK] {self._title} by {self._author} (ISBN: {self._isbn}) - {self._status}"


class LibraryInventory:
    def __init__(self, filename="library.csv"):
        self.books = []
        self.filename = filename
        self.load_books()

    def add_book(self, book):
        if any(b._isbn == book._isbn for b in self.books):
            return False
        self.books.append(book)
        self.save_books()
        return True

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b._title.lower()]

    def search_by_isbn(self, isbn):
        return [b for b in self.books if b._isbn == isbn]

    def display_all(self):
        if not self.books:
            print("No books available.")
        for book in self.books:
            print(book.display_info())

    def save_books(self):
        try:
            with open(self.filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['type', 'title', 'author', 'isbn', 'status'])
                for b in self.books:
                    writer.writerow([
                        b.__class__.__name__,
                        b._title,
                        b._author,
                        b._isbn,
                        b._status
                    ])
        except Exception as e:
            print("Error saving books:", e)

    def load_books(self):
        try:
            with open(self.filename, 'r', newline='') as f:
                reader = csv.reader(f)
                next(reader, None)
                self.books = []
                for row in reader:
                    if len(row) == 5:
                        btype, title, author, isbn, status = row
                        if btype == "DigitalBook":
                            book = DigitalBook(title, author, isbn)
                        else:
                            book = Book(title, author, isbn)
                        book._status = status
                        self.books.append(book)
        except FileNotFoundError:
            self.books = []


def main():
    inventory = LibraryInventory()

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Add Digital Book")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. View All")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            title = input("Title: ")
            author = input("Author: ")
            isbn = input("ISBN: ")
            if inventory.add_book(Book(title, author, isbn)):
                print("Book added.")
        elif choice == "2":
            title = input("Title: ")
            author = input("Author: ")
            isbn = input("ISBN: ")
            if inventory.add_book(DigitalBook(title, author, isbn)):
                print("E-Book added.")
        elif choice == "3":
            isbn = input("Enter ISBN to issue: ")
            res = inventory.search_by_isbn(isbn)
            if res and res[0].issue():
                inventory.save_books()
                print("Issued.")
            else:
                print("Cannot issue.")
        elif choice == "4":
            isbn = input("Enter ISBN to return: ")
            res = inventory.search_by_isbn(isbn)
            if res and res[0].return_book():
                inventory.save_books()
                print("Returned.")
            else:
                print("Cannot return.")
        elif choice == "5":
            inventory.display_all()
        elif choice == "6":
            print("Exit")
            break
        else:
            print("Invalid!")


if __name__ == "__main__":
    main()