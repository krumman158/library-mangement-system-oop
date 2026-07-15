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
   