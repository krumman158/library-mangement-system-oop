# Library Management System — OOP Edition

A console-based Library Management System written in Python, re-architected using
Object-Oriented Programming, SOLID principles, and clean-code practices.

This is an OOP re-design of an earlier functional version of the same system —
same domain, new architecture: classes, inheritance, composition, and dependency
injection instead of functions and dictionaries.

## Features

- Add, list, search, and remove library items
- Item types: `Book`, `EBook`, `Magazine`, `DVD`
- Register members (`StudentMember`, `StaffMember`) with different loan limits
- Borrow and return items with due-date tracking (`LoanPolicy`)
- File-based persistence — the catalogue is saved to disk and reloaded on the
  next run
- Custom exception hierarchy for clear error handling (`ItemNotFoundError`,
  `ItemNotAvailableError`, `LoanLimitExceededError`)

## Project Structure

```
library-management-system/
├── README.md
├── requirements.txt
├── main.py                     # entry point: builds objects, starts the CLI
├── data/
│   └── library.txt             # persisted item records
│
└── library/
    ├── __init__.py
    ├── domain/                 # entities & value objects
    │   ├── items.py            # LibraryItem (ABC), Book, EBook, Magazine, DVD
    │   ├── members.py          # Member, StudentMember, StaffMember
    │   └── loan.py             # Loan, Metadata (dataclasses)
    ├── storage/                 # persistence layer (DIP boundary)
    │   ├── base.py              # Storage (ABC)
    │   ├── file_storage.py      # FileStorage(Storage)
    │   └── memory_storage.py    # MemoryStorage(Storage)
    ├── services/                # application logic
    │   ├── library.py           # Library — composition + orchestration
    │   └── loan_policy.py       # LoanPolicy — due dates, loan limits
    ├── protocols.py             # Displayable protocol, duck-typed print_catalog
    ├── exceptions.py            # LibraryError hierarchy
    └── cli.py                   # console UI
```

## Requirements

- Python 3.10+ (standard library only — no external dependencies)

