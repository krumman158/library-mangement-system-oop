class LibraryError(Exception):
    def __init__(self, message):
        self.message=message
        super().__init__(self.message)

class ItemNotFoundError(LibraryError):
 """No item matches the given id."""

class ItemNotAvailableError(LibraryError):
 """The item is already on loan."""

class LoanLimitExceededError(LibraryError):
 """The member is at their borrowing limit."""