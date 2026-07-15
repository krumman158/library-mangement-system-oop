from library.domain.LibrarayItem import LibraryItem

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