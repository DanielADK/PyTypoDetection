import string
import WordAnalyzer.Library
from WordAnalyzer import WordUtilities
from sty import fg, ef, rs


class FileReader:
    def __init__(self, library: WordAnalyzer.Library):
        self.__library__ = library
        self.words_save_path = "files/cs/words.txt"
        self.words = set()
        self.custom_words_path = "files/cs/custom_words.txt"
        self.custom_words = set()

    def read_custom_words(self) -> bool:
        with open(self.custom_words_path, "r") as file:
            while True:
                line = file.readline()
                if not line:
                    break
                # word per line validation
                if line.__contains__(" "):
                    self.custom_words.clear()
                    return False
                self.custom_words.add(line.replace("\n", ""))
        return True
    def read_books(self) -> bool:
        all_books = self.__library__.get_books()
        for file in all_books:
            with open(file, "r") as opened_file:

                # Read line by line till the EOF
                start_of_reading = False
                while True:
                    line = opened_file.readline()
                    if not line:
                        break
                    if not start_of_reading:
                        if line == "# START OF READING\n":
                            start_of_reading = True
                        continue

                    words = line.split(" ")
                    # Process words => remove non-alphabetic chars
                    for word in words:
                        word = WordUtilities.process(word)
                        if len(word) != 0:
                            self.words.add(word)
        return True
    def save_words(self) -> None:
        try:
            with open(self.words_save_path, "w") as file:
                sorted_words = sorted(list(self.words))
                [file.write(word + "\n") for word in sorted_words]
        except EnvironmentError:
            print(fg.red + "Chyba při zápisu do souboru " + fg.rs + self.custom_words_path)
    def save_custom_words(self) -> None:
        try:
            with open(self.custom_words_path, "w") as file:
                sorted_words = sorted(list(self.custom_words))
                [file.write(word + "\n") for word in sorted_words]
        except EnvironmentError:
            print(fg.red + "Chyba při zápisu do souboru " + fg.rs + self.custom_words_path)

    def read_and_correct(self, to_correct: string) -> None:
        with open(to_correct, "r") as file:
            all_words = self.words.union(self.custom_words)
            line_counter = 1
            while True:
                line = file.readline()
                if not line:
                    break
                line_counter += 1
                words = line.split(" ")
                for word in words:
                    word = WordUtilities.process(word)
                    if len(word) == 0:
                        continue
                    if not word in all_words:
                        while True:
                            print(fg.blue + "Řádek " + str(line_counter))
                            print(ef.bold + "Následujicí slovo nemáme v databázi. Chcete jej přidat? (ANO/NE)" + fg.rs)
                            response = input(fg.li_yellow + word + " ").lower()
                            if response == "a" or response == "ano":
                                self.custom_words.add(word)
                                all_words.add(word)
                                print(fg.li_green + "Slovo úspěšně přidáno!")
                                break
                            elif response == "n" or response == "ne":
                                print(fg.yellow + "Přeskakuji slovo!!")
                                break
                            else:
                                print(fg.red + "Neplatná akce!")
        self.save_custom_words()