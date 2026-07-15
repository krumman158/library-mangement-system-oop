from library.services.library import Library
from library.domain.book import Book
from library.domain.magazine import Magazine
from library.domain.ebook import EBook
from library.domain.dvd import DVD
from library.domain.members import StudentMember, StaffMember, Member
from library.exceptions import LibraryError
from library.protocols import print_catalog
from abc import ABC,abstractmethod

MENU = """
1. Add item
2. List items
3. Search item
4. Register member
5. Borrow item
6. Return item
7. Remove item
0. Exit
"""

MENU_2 = """
1. Borrow item
2. Return item
0. Exit
"""
class Add_item:

    def add_item(self,library: Library) -> None:
        kind = input("Type (book/ebook/magazine/dvd): ").strip().lower()
        title = input("Title: ")
        author = input("Author: ")
        year = int(input("Year: "))
        if kind == "book":
            item = Book(title, author, year)
        elif kind == "ebook":
            size = float(input("Size (MB): "))
            item = EBook(title, author, year, size)
        elif kind == "magazine":
            item = Magazine(title, author, year)
        elif kind == "dvd":
            item = DVD(title, author, year)
        else:
            print("Unknown type / Please Enter valid Input.")
            return
        library.add(item)
        print(f"Added: {item}")

class List_items:
    def list_items(self,library: Library) -> None:
        print_catalog(library._items)

class Search_item:
    def search_item(self,library: Library) -> None:
        title = input("Search title: ")
        if not title:
            print("Invalid Input Please enter valid title")
            return
        results = library.find(title)
        if not results:
            print("Item Not found")
            return
        for item in results:
            print(item)

class Make_member(ABC):

    @abstractmethod
    def make_member(self):
        pass

class Register_member(Make_member):

    def make_member(self) -> Member:
        role = input("Role (student/staff): ").strip().lower()
        member_id = input("Member ID: ")
        name = input("Name: ")
        email = input("Email: ")
        if role == "staff":
            return StaffMember(member_id, name, email)
        return StudentMember(member_id, name, email)
    
    def register_member(self,library: Library) -> None:
        member = self.make_member()
        library.add_member(member)
        print(f"Registered: {member.name} ({member._member_id})")


class Login(Register_member):
    def login(self,library: Library) -> Member:
        while True: 
            member_id = input("Enter Member ID (type 'new' to register): ").strip().lower()
            if member_id == "new":
                member = self.make_member()
                library.add_member(member)
                print(f"Registered: {member.name} ({member._member_id})")
                return member
            try:
                member = library.get_member(member_id)
                print(f"Welcome back, {member.name}!")
                return member
            except LibraryError:
                print("Member not found. Type 'new' to register.")

class Borrow_item:
    def borrow_item(self,library: Library, member: Member) -> None:
        item_id = int(input("Item ID: "))
        library.borrow(member, item_id)
        print("Borrowed successfully.")

class Return_item:
    def return_item(self,library: Library, member: Member) -> None:
        item_id = int(input("Item ID: "))
        library.return_item(member, item_id)
        print("Returned successfully.")

class Remove_item:
    def remove_item(self,library: Library) -> None:
        item_id = int(input("Item ID: "))
        library.remove(item_id)
        print("Removed.")

a=Add_item()
l=List_items()
lo=Login()
s=Search_item()
r=Register_member()
b=Borrow_item()
re=Return_item()
rm=Remove_item()

def run(library: Library) -> None:
    member = lo.login(library)
    is_staff = isinstance(member, StaffMember)

    options_staff = {
        "1": a.add_item,
        "2": l.list_items,
        "3": s.search_item,
        "4": r.register_member,
        "5": lambda lib: b.borrow_item(lib, member),
        "6": lambda lib: re.return_item(lib, member),
        "7": rm.remove_item,
    }
    options_student = {
        "1": lambda lib: b.borrow_item(lib, member),
        "2": lambda lib: re.return_item(lib, member),
    }

    menu = MENU if is_staff else MENU_2
    options = options_staff if is_staff else options_student

    while True:
        print(menu)
        choice = input("Choose: ").strip()
        if choice == "0":
            break
        option = options.get(choice)
        if not option:
            print("Invalid choice.")
            continue
        try:
            option(library)
        except LibraryError as e:
            print(f"Error: {e}")
        except (ValueError, KeyError) as e:
            print(f"Invalid input: {e}")