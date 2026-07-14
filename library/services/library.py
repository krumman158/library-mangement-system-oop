from datetime import date
from library.storage.base import Storage
from library.domain.items import LibraryItem
from library.domain.loan import Loan
from library.services.loan_policy import LoanPolicy
from library.exceptions import ItemNotFoundError,ItemNotAvailableError,LoanLimitExceededError
from library.domain.items import Book, EBook, Magazine, DVD

ITEM_TYPES = {"book": Book, "ebook": EBook, "magazine": Magazine, "dvd": DVD}


class Library:
   """Coordinates the collection. Composed with a Storage (injected)."""
   def __init__(self, storage) -> None:
     self._storage = storage 
     self._items: list[LibraryItem] = []
     self._loans: list[Loan] = []
     self._members: dict[str, object] = {}

   def add(self, item: LibraryItem) -> None:
     self._items.append(item)

   def add_member(self, member) -> None:
    self._members[member._member_id] = member

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

   def borrow(self, member, item_id: int) -> None:
     item = self[item_id]
     if not item._available:
        raise ItemNotAvailableError(f"This item {item_id} not available")
     if not LoanPolicy.can_borrow(member):
        raise LoanLimitExceededError(f"{member._member_id} has exceeded loan limit")
     today = date.today()
     due = LoanPolicy.due_date(item, today)
     member.borrow(item_id)
     item._available = False
     self._loans.append(Loan(item_id, member._member_id, today, due))
     
   def return_item(self, member, item_id: int) -> None:
     item = self[item_id]
     member.return_item(item_id)
     item._available = True
     self._loans = [l for l in self._loans
                    if not (l.item_id == item_id and l.member_id == member._member_id)]
     
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
