import json
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

    def read_and_correct(self, to_correct: str) -> None:
        with open(to_correct, "r") as file:
            line_counter = 1
            new_word: Word | None = None
            words: list[str] = []
            # Merge words and custom_words
            all_words: dict[str, Word] = self.words.copy()
            for key, word in self.custom_words:
                found_word: Word | None = self.words.get(key)
                if found_word is None:
                    all_words[key] = word

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
                    if not word in self.words or not word in self.custom_words:
                        while True:
                            print(fg.blue + "Řádek " + str(line_counter))
                            print(ef.bold + "Následujicí slovo nemáme v databázi. "
                                            "Chcete jej přidat? (ANO/NE)" + fg.rs)
                            response = input(fg.li_yellow + word + " ").lower()
                            if "a" in response or "ano" in response:
                                new_word = Word(word)
                                self.custom_words[word] = new_word
                                all_words[word] = new_word
                                print(fg.li_green + "Slovo úspěšně přidáno!")
                                break
                            elif "n" in response or "ne" in response:
                                print(fg.yellow + "Přeskakuji slovo!!")
                                break
                            else:
                                print(fg.red + "Neplatná akce!")
        self.save_custom_words()
