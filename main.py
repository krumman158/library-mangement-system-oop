from library.storage.file_storage import FileStorage
from library.services.library import Library
from library.cli import run

if __name__ == "__main__":
    storage = FileStorage("data/library.txt")
    member_storage = FileStorage("data/members.txt")

    library = Library(storage, member_storage)
    library.load_from_storage()
    library.load_members_from_storage()

    run(library)
    
    library.save_to_storage()
    library.save_members_to_storage()