from library.storage.base import Storage

class MemoryStorage(Storage):
    def __init__(self) -> None:
        self._records:list[dict]=[]

    def load(self) -> list[dict]:
        return self._records
    
    def save(self,records:list[dict]) -> None:
        self._records=records
        