from library.exceptions import LoanLimitExceededError
from abc import ABC,abstractmethod
class Member(ABC):
  max_loans: int = 5 # class attribute (default limit)
  def __init__(self, member_id: str, name: str, email: str) -> None:
   self._member_id = member_id # protected
   self.name = name # public
   self.__borrowed: list[int] = [] # private 
   self.email = email # via setter

  @property
  def email(self) -> str:
   return self._email
  
  @email.setter
  def email(self, value: str) -> None:
   if "@" not in value:
    raise ValueError("invalid email")
   self._email = value

  @abstractmethod
  def role(self) -> str:
   pass

  def to_dict(self) -> dict:
    return {
        "type": self.role(),
        "member_id": self._member_id,
        "name": self.name,
        "email": self.email,
        "borrowed": ",".join(str(i) for i in self.__borrowed),
    }
  
  @classmethod
  def from_dict(cls, data: dict) -> "Member":
    m = cls(data["member_id"], data["name"], data["email"])
    raw = data.get("borrowed", "")
    m._Member__borrowed = [int(x) for x in raw.split(",") if x]
    return m
  
  @property
  def borrowed(self) -> tuple[int, ...]:
   return tuple(self.__borrowed) # read-only view, encapsulation
  
  def borrow(self, item_id: int) -> None:
   if len(self.__borrowed)>=self.max_loans:
    raise LoanLimitExceededError(f"{self._member_id} has exceed loan limit {self.max_loans}")
   self.__borrowed.append(item_id)
   
  def return_item(self, item_id: int) -> None:
    if item_id not in self.__borrowed:
        raise ValueError(f"Item {item_id} not borrowed.")
    self.__borrowed.remove(item_id)

class StudentMember(Member):
 max_loans = 3 # polymorphism via class attribute

 def role(self) -> str:
        return "student"

class StaffMember(Member):
 max_loans = 10

 def role(self) -> str:
        return "staff"
