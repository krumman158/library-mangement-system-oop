from library.domain.LibrarayItem import LibraryItem

class Magazine(LibraryItem):
 LOAN_DAYS=10

 def loan_period_days(self) -> int:
   return self.LOAN_DAYS
  
 def display_info(self) -> str:
  return f"Magazine: {self.title} ({self.year})"
 