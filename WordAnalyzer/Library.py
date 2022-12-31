import string
from os import walk, path

class Library:
    def __init__(self, source_folder: string):
        self.__source_folder:set = source_folder
        self.__books: set = set()
        self.__dictionaries: set = set()

    def load_books(self):
        # Load books
        for curr_path, subdirs, files in walk(self.__source_folder+"/books"):
            [self.__books.add(path.join(curr_path, file)) for file in files]

    def get_books(self):
        return self.__books
    def get_dictionaries(self):
        return self.__dictionaries