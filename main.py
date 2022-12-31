from WordAnalyzer.Library import Library
from WordAnalyzer.FileReader import FileReader
from WordAnalyzer.Corrector import Corrector
import os, sys

if __name__ == "__main__":
    lib = Library("files/cs")
    if not os.path.exists(sys.argv[0]) or not os.path.isfile(sys.argv[0]):
        print("File not found.")
        exit()
    fr = FileReader(lib, sys.argv[0])
    if sys.argv[1] == "-a" or sys.argv[1] == "-analyze":
        lib.load_books()
    else:
        fr.load_words()

    cor = Corrector(fr)
    cor.correct_file(sys.argv[0])



