from library.domain.book import Book
from library.domain.downloadable import Downloadable

class EBook(Book, Downloadable): # multi-level + multiple inheritance
 LOAN_DAYS = 90

 def __init__(self, title: str, author: str, year: int, size_mb: float) -> None:
  super().__init__(title, author, year) # walks the MRO
  self.size_mb = size_mb

 def display_info(self) -> str:
  print(self.download()) 
  return f"{super().display_info()} [e-book, {self.size_mb} MB]"
# EBook.__mro__ -> EBook, Book, LibraryItem, Downloadable, object