import string
from os import walk, path

class Library:
    def __init__(self, source_folder: string):
        self.source_folder = source_folder
        self.books = set()

    def load_files(self):
        # Load books
        for curr_path, subdirs, files in walk(self.source_folder + "/books"):
            for file in files:
                self.books.add(path.join(curr_path, file))