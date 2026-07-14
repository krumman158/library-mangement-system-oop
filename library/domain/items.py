from abc import ABC, abstractmethod
class LibraryItem(ABC):
   """Contract for anything the library lends."""
   _next_id: int = 0 # class attribute (shared counter)
   def __init__(self, title: str, author: str, year: int) -> None:
     LibraryItem._next_id += 1
     self.id: int = LibraryItem._next_id # instance attribute
     self.title = title
     self.author = author
     self.year = year # runs the setter below
     self._available = True # protected state

   @property
   def year(self) -> int:
    return self._year
   
   @year.setter
   def year(self, value: int) -> None:
    if not 0 < value <= 2100:
      raise ValueError(f"invalid year: {value}")
    self._year = value
   
   @abstractmethod
   def loan_period_days(self) -> int:
    """How long this item may be borrowed."""

   @abstractmethod
   def display_info(self) -> str:
    """One-line description for the catalogue."""

   def __str__(self) -> str:
    state = "available" if self._available else "on loan"
    return f"ID: {self.id}   Title: {self.title}   Author:  {self.author}   State: {state}"
   
   def __repr__(self) -> str:
    return f"{type(self).__name__}(id={self.id}, title={self.title!r})"
   

class Book(LibraryItem):
  LOAN_DAYS = 21 # class attribute

  def loan_period_days(self) -> int:
   return self.LOAN_DAYS
  
  def display_info(self) -> str:
   return f"Book: {self.title} by {self.author} ({self.year})"
  
  def to_dict(self) -> dict:
        return {
            "type": "book",
            "title": self.title,
            "author": self.author,
            "year": str(self.year),
        }
  
  @classmethod
  def from_dict(cls, data: dict) -> "Book":
   """Factory constructor — rebuild a Book from a stored record."""
   return cls(data["title"], data["author"], int(data["year"]))
  
  #coulbe used in sort
  def __lt__(self, other: "Book") -> bool: # enables sorted()
   return self.title.lower() < other.title.lower()
  
  # used in remove
  def __eq__(self, other: object) -> bool:
   return isinstance(other, Book) and self.id == other.id
  
  def __hash__(self) -> int: # pairs with __eq__
   return hash(self.id)

class Downloadable:
 """Mixin: adds a capability, not an identity."""

 def download(self) -> str:
  return f"Downloading {self.title}..." # relies on the host class


class EBook(Book, Downloadable): # multi-level + multiple inheritance
 LOAN_DAYS = 90

 def __init__(self, title: str, author: str, year: int, size_mb: float) -> None:
  super().__init__(title, author, year) # walks the MRO
  self.size_mb = size_mb

 def display_info(self) -> str:
  print(self.download()) 
  return f"{super().display_info()} [e-book, {self.size_mb} MB]"
# EBook.__mro__ -> EBook, Book, LibraryItem, Downloadable, object

class Magazine(LibraryItem):
 LOAN_DAYS=10

 def loan_period_days(self) -> int:
   return self.LOAN_DAYS
  
 def display_info(self) -> str:
  return f"Magazine: {self.title} ({self.year})"
 
class DVD(LibraryItem):
 LOAN_DAYS=10

 def loan_period_days(self) -> int:
  return self.LOAN_DAYS
  
 def display_info(self) -> str:
  return f"DVD: {self.title} ({self.year})"
