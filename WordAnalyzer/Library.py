import string
from os import walk, path

class Library:
    def __init__(self, source_folder: string):
        self.__source_folder__ = source_folder
        self.__books__ = set()
        self.__dictionaries__ = set()

    def load_books(self):
        # Load books
        for curr_path, subdirs, files in walk(self.__source_folder__ + "/books"):
            [self.__books__.add(path.join(curr_path, file)) for file in files]

    def get_books(self):
        return self.__books__
    def get_dictionaries(self):
        return self.__dictionaries__