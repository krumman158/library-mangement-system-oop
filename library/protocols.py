from typing import Protocol, runtime_checkable

@runtime_checkable
class Displayable(Protocol):
   """Structural interface — no inheritance required."""
   def display_info(self) -> str: ...
   
   
def print_catalog(items: list[Displayable]) -> None:
     for item in items: # duck typing: anything with display_info() fits
        print(item.display_info())
