from datetime import date, timedelta
from library.domain.LibrarayItem import LibraryItem
from library.domain.members import Member

class LoanPolicy:
    @staticmethod
    def due_date(item: LibraryItem, borrowed_on: date) -> date:
        return borrowed_on + timedelta(days=item.loan_period_days())

    @classmethod
    def can_borrow(cls, member: Member) -> bool:
        return len(member.borrowed) < member.max_loans