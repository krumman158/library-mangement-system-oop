from datetime import date
from library.storage.base import Storage
from library.domain.LibrarayItem import LibraryItem
from library.domain.loan import Loan
from library.services.loan_policy import LoanPolicy
from library.exceptions import ItemNotFoundError,ItemNotAvailableError,LoanLimitExceededError
from library.domain.book import Book
from library.domain.ebook import EBook
from library.domain.magazine import Magazine
from library.domain.dvd import DVD
from library.domain.members import StaffMember,StudentMember
import math

ITEM_TYPES = {"book": Book, "ebook": EBook, "magazine": Magazine, "dvd": DVD}
MEMBER_TYPES = {"student": StudentMember, "staff": StaffMember}

class Library:
   """Coordinates the collection. Composed with a Storage (injected)."""
   def __init__(self, storage,member_storage) -> None:
     self._storage = storage 
     self._member_storage = member_storage
     self._items: list[LibraryItem] = []
     self._loans: list[Loan] = []
     self._members: dict[str, object] = {}

   def add(self, item: LibraryItem) -> None:
     self._items.append(item)
     records = [item.to_dict() for item in self._items]
     print("Saving records")
     self._storage.save(records)

   def add_member(self, member) -> None:
    self._members[member._member_id] = member
    records = [m.to_dict() for m in self._members.values()]
    print("Saving Members")
    self._member_storage.save(records)

   def display(self):
      records = self._storage.load()
      page_size=math.floor(len(records)/2)
      page1,page2=[],[]
      for i,record in enumerate(records):
         r_cls=ITEM_TYPES.get(record.get("type"))
         if r_cls is None:
            continue
         obj = r_cls.from_dict(record)
         (page1 if i <= page_size else page2).append(obj)

      if not page1:
         print("Nothing To Show")
      else:
         for page in page1:
            print(page)
      page1.clear()      

      if not page2:
         return
      else:
         for page in page2:
            print(page)
      page2.clear()      
                
   

   def get_member(self, member_id: str):
    if member_id not in self._members:
      raise ItemNotFoundError(f"no member with id {member_id}")
    return self._members[member_id]

   def __len__(self) -> int:
     return len(self._items)
   
   def __getitem__(self, item_id: int) -> LibraryItem:
     for item in self._items:
       if item.id == item_id:
         return item
     raise ItemNotFoundError(f"no item with id {item_id}")
   
   def find(self, title: str) -> list[LibraryItem]:
     return [i for i in self._items if title.lower() in i.title.lower()]

   def remove(self, item_id: int) -> None:
    item = self[item_id]
    if not item._available:
      raise ItemNotAvailableError(f"Cannot remove item {item_id}")
    self._items.remove(item)
    records = [item.to_dict() for item in self._items]
    print("Saving records")
    self._storage.save(records)

   def update(self,item_id:int) -> None:
      item=self[item_id]
      if not item._available:
         raise ItemNotAvailableError(f"Can not update item {item_id}")
      choice=input("Enter what you want to update (title/author/year): ").strip().lower()
      if choice=='title':
         t=input("Enter updated title: ").strip().lower()
         item.title=t
         print("Updated!!")
      elif choice=='author':
         a=input("Enter updated author: ").strip().lower()
         item.author=a
         print("Updated!!")
      elif choice=='year':
         y=int(input("Enter updated year: "))
         item._year=y
         print("Updated!!")
      else:
         print('Invalid input!! Try again')   
      records = [item.to_dict() for item in self._items]
      print("Saving records")
      self._storage.save(records)         

   def borrow(self, member, item_id: int) -> None:
     item = self[item_id]
     if not item._available:
        raise ItemNotAvailableError(f"This item {item_id} not available")
     if not LoanPolicy.can_borrow(member):
        raise LoanLimitExceededError(f"{member._member_id} has exceeded loan limit")
     today = date.today()
     due = LoanPolicy.due_date(item, today)
     member.borrow(item_id)
     self.save_members_to_storage() 
     item._available = False
     records = [item.to_dict() for item in self._items]
     self._storage.save(records)
     self._loans.append(Loan(item_id, member._member_id, today, due))
     
   def return_item(self, member, item_id: int) -> None:
     item = self[item_id]
     member.return_item(item_id)
     self.save_members_to_storage() 
     item._available = True
     records = [item.to_dict() for item in self._items]
     self._storage.save(records)
     self._loans = [l for l in self._loans
                    if not (l.item_id == item_id and l.member_id == member._member_id)]
     

   def loan(self):
      if not self._loans:
         print("No loans")
         return
      else:
         for loan in self._loans:
            print(loan)    
     
   def load_from_storage(self) -> None:
        records = self._storage.load()
        for record in records:
            item_cls = ITEM_TYPES.get(record.get("type"))
            if item_cls is None:
                continue
            self._items.append(item_cls.from_dict(record))

   def save_to_storage(self) -> None:
        records = [item.to_dict() for item in self._items]
        print("Saving records")
        self._storage.save(records)

   def load_members_from_storage(self) -> None:
        records = self._member_storage.load()
        for record in records:
            member_cls = MEMBER_TYPES.get(record.get("type"))
            if member_cls is None:
                continue
            member = member_cls.from_dict(record)
            self._members[member._member_id] = member

   def save_members_to_storage(self) -> None:
    records = [m.to_dict() for m in self._members.values()]
    print("Saving Members")
    self._member_storage.save(records)

