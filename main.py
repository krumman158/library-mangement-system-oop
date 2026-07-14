from library.storage.file_storage import FileStorage
from library.services.library import Library
from library.cli import run

if __name__ == "__main__":
 storage = FileStorage("data/library.txt")
 library = Library(storage) 
 library.load_from_storage()  
 run(library)
 library.save_to_storage()