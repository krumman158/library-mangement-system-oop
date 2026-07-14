from dataclasses import dataclass, field
from datetime import date
@dataclass
class Metadata:
 """Owned by an item — composition (created and destroyed with it)."""
 isbn: str = ""
 publisher: str = ""
 pages: int = 0

@dataclass
class Loan:
 """References an item and a member — aggregation (they outlive it)."""
 item_id: int
 member_id: str
 borrowed_on: date
 due_on: date