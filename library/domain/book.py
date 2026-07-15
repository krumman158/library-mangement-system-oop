from library.domain.LibrarayItem import LibraryItem

class Book(LibraryItem):
  LOAN_DAYS = 21 # class attribute

  def loan_period_days(self) -> int:
   return self.LOAN_DAYS
  
  def display_info(self) -> str:
   return f"ID: {self.id}  Book: {self.title} by {self.author} ({self.year})  Available: {self._available}"
  
  def to_dict(self) -> dict:
        return {
            "type": "book",
            "title": self.title,
            "author": self.author,
            "year": str(self.year),
            "available":self._available,
            "ID":self.id
        }
  
  @classmethod
  def from_dict(cls, data: dict) -> "Book":
    return cls(
      data["title"],
      data["author"],
      int(data["year"]),
      str(data['available']).strip().lower() == "true",
      int(data['ID'])
      )
  
  #coulbe used in sort
  def __lt__(self, other: "Book") -> bool: # enables sorted()
   return self.title.lower() < other.title.lower()
  
  # used in remove
  def __eq__(self, other: object) -> bool:
   return isinstance(other, Book) and self.id == other.id
  
  def __hash__(self) -> int: # pairs with __eq__
   return hash(self.id)