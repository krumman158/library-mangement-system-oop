from abc import ABC, abstractmethod
class Storage(ABC):
 """Persistence interface. High-level code depends on THIS, not on files."""
 @abstractmethod
 def load(self) -> list[dict]:
   """Return all stored records."""

 @abstractmethod
 def save(self, records: list[dict]) -> None:
   """Persist all records."""
