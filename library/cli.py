from library.services.library import Library
from library.domain.items import Book, Magazine, DVD, EBook
from library.domain.members import StudentMember, StaffMember
from library.exceptions import LibraryError
from library.protocols import print_catalog

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

def add_item(library: Library) -> None:
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
        print("Unknown type.")
        return
    library.add(item)
    print(f"Added: {item}")

def list_items(library: Library) -> None:
    print_catalog(library._items)

def search_item(library: Library) -> None:
    title = input("Search title: ")
    results = library.find(title)
    if not results:
        print("Item Not found")
        return
    for item in results:
        print(item)


def make_member() -> object:
    role = input("Role (student/staff): ").strip().lower()
    member_id = input("Member ID: ")
    name = input("Name: ")
    email = input("Email: ")
    if role == "staff":
        return StaffMember(member_id, name, email)
    return StudentMember(member_id, name, email)

def register_member(library: Library) -> None:
    member = make_member()
    library.add_member(member)
    print(f"Registered: {member.name} ({member._member_id})")

def borrow_item(library: Library) -> None:
    member_id = input("Member ID: ")
    member = library.get_member(member_id)
    item_id = int(input("Item ID: "))
    library.borrow(member, item_id)
    print("Borrowed successfully.")

def return_item(library: Library) -> None:
    member_id = input("Member ID: ")
    member = library.get_member(member_id)
    item_id = int(input("Item ID: "))
    library.return_item(member, item_id)
    print("Returned successfully.")

def remove_item(library: Library) -> None:
    item_id = int(input("Item ID: "))
    library.remove(item_id)
    print("Removed.")

def run(library: Library) -> None:
    options = {
        "1": add_item,
        "2": list_items,
        "3": search_item,
        "4": register_member,
        "5": borrow_item,
        "6": return_item,
        "7": remove_item,
    }
    while True:
        print(MENU)
        choice = input("Choose: ").strip()
        if choice == "0":
            break
        option = options.get(choice)
        if not options:
            print("Invalid choice.")
            continue
        try:
            option(library)
        except LibraryError as e:
            print(f"Error: {e}")
        except (ValueError, KeyError) as e:
            print(f"Invalid input: {e}")