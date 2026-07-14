from library.services.library import Library
from library.domain.items import Book, Magazine, DVD, EBook
from library.domain.members import StudentMember, StaffMember, Member
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

MENU_2 = """
1. Borrow item
2. Return item
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

def make_member() -> Member:
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

def login(library: Library) -> Member:
    while True:
        member_id = input("Enter Member ID (or type 'new' to register): ").strip()
        if member_id.lower() == "new":
            member = make_member()
            library.add_member(member)
            print(f"Registered: {member.name} ({member._member_id})")
            return member
        try:
            member = library.get_member(member_id)
            print(f"Welcome back, {member.name}!")
            return member
        except LibraryError:
            print("Member not found. Type 'new' to register.")

def borrow_item(library: Library, member: Member) -> None:
    item_id = int(input("Item ID: "))
    library.borrow(member, item_id)
    print("Borrowed successfully.")

def return_item(library: Library, member: Member) -> None:
    item_id = int(input("Item ID: "))
    library.return_item(member, item_id)
    print("Returned successfully.")

def remove_item(library: Library) -> None:
    item_id = int(input("Item ID: "))
    library.remove(item_id)
    print("Removed.")

def run(library: Library) -> None:
    member = login(library)
    is_staff = isinstance(member, StaffMember)

    options_staff = {
        "1": add_item,
        "2": list_items,
        "3": search_item,
        "4": register_member,
        "5": lambda lib: borrow_item(lib, member),
        "6": lambda lib: return_item(lib, member),
        "7": remove_item,
    }
    options_student = {
        "1": lambda lib: borrow_item(lib, member),
        "2": lambda lib: return_item(lib, member),
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