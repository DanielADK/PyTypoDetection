import WordAnalyzer.Library
from WordAnalyzer.Word import Word
from WordAnalyzer import WordUtilities
from sty import fg, ef, rs


class FileReader:
    def __init__(self, library: WordAnalyzer.Library):
        self.__library__: WordAnalyzer.Library = library
        self.words_save_path: str = "files/cs/words.txt"
        self.words: dict[str,Word] = {}
        self.custom_words_path: str = "files/cs/custom_words.txt"
        self.custom_words: dict[str, Word] = {}

    def read_custom_words(self) -> bool:
        with open(self.custom_words_path, "r") as file:
            while True:
                line = file.readline()
                if not line:
                    break
                # word per line validation
                if line.__contains__(" "):
                    return False

                line = line.replace("\n", "")
                found_word = self.words.get(line)
                if found_word is None:
                    found_word = Word(line)
                    self.words[line] = found_word
                    self.custom_words[line] = found_word
                else:
                    found_word.frequency += 1

        return True
    def read_books(self) -> bool:
        all_books: set = self.__library__.get_books()
        for file in all_books:
            with open(file, "r") as opened_file:

                # Read line by line till the EOF
                start_of_reading: bool = False
                while True:
                    line = opened_file.readline()
                    if not line:
                        break
                    if not start_of_reading:
                        if line == "# START OF READING\n":
                            start_of_reading = True
                        continue

                    words: list[str] = line.split(" ")
                    # Process words => remove non-alphabetic chars
                    pre_word: Word | None = None
                    for word in words:
                        word: str = WordUtilities.process(word)
                        # If empty word
                        if len(word) == 0:
                            continue

                        found_word = self.words.get(word)
                        if found_word is None:
                            found_word = Word(word)
                            self.words[word] = found_word
                        else:
                            found_word.frequency += 1
                            if pre_word is not None:
                                pre_word.post_words.add(found_word)
                                found_word.pre_words.add(pre_word)
                        pre_word = found_word

        return True

    def save_words(self) -> None:
        try:
            with open(self.words_save_path, "w") as file:
                sorted_words: list[str] = sorted(self.words)
                [file.write(word + "\n") for word in sorted_words]
        except EnvironmentError:
            print(fg.red + "Chyba při zápisu do souboru " + fg.rs + self.words_save_path)
    def save_custom_words(self) -> None:
        try:
            with open(self.custom_words_path, "w") as file:
                sorted_words: list[str] = sorted(self.custom_words)
                [file.write(word + "\n") for word in sorted_words]
        except EnvironmentError:
            print(fg.red + "Chyba při zápisu do souboru " + fg.rs + self.custom_words_path)

