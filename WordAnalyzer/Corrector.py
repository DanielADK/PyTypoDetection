import os
from queue import Queue

from WordAnalyzer.Word import Word
from WordAnalyzer.FileReader import FileReader
from WordAnalyzer.WordUtilities import process
from WordAnalyzer.SimilarityCalculator import SimilarityCalculator
from collections import defaultdict
from sty import fg, ef, rs
import threading

class Corrector:
    class UnknownWord:
        def __init__(self, word: str, line: int, possible_words=None):
            if possible_words is None:
                possible_words = set()
            self.line = line
            self.word = word
            self.possible_words: set = possible_words

    def __init__(self, fr: FileReader):
        self.words: dict[str,Word] = fr.words
        self.words_by_len: dict[int, set[str]] = defaultdict(set)
        self.parse_words_by_len()
        self.custom_words: dict[str, Word] = fr.custom_words
        self.similarity_calc: SimilarityCalculator = SimilarityCalculator()

        # file corrector data
        self.__word_queue: Queue[Corrector.UnknownWord] = Queue()
        self.__line_counter: int = 0
        self.__reading = False


    def parse_words_by_len(self):
        [self.words_by_len[len(word.word)].add(word.word) for word in self.words.values()]

    def __corrector(self, file) -> None:
        while self.__reading:
            line = file.readline()
            if not line:
                self.__reading = False
                break
            self.__line_counter += 1
            words = line.split(" ")
            for word in words:
                word = process(word)
                if len(word) == 0:
                    continue
                if word not in self.words_by_len[len(word)]:
                    possible_word: Corrector.UnknownWord = Corrector.UnknownWord(word, self.__line_counter)
                    if len(word) > 2 and self.words_by_len.get(len(word)-1) is not None:
                        for possible in self.words_by_len.get(len(word)-1):
                            if self.similarity_calc.levenshtein_distance(word, possible) > 1:
                                continue
                            possible_word.possible_words.add(possible)
                    if len(word) > 1 and self.words_by_len.get(len(word)) is not None:
                        for possible in self.words_by_len.get(len(word)):
                            if self.similarity_calc.levenshtein_distance(word, possible) > 1:
                                continue
                            possible_word.possible_words.add(possible)
                    if len(word) > 0 and self.words_by_len.get(len(word)+1) is not None:
                        for possible in self.words_by_len.get(len(word)+1):
                            if self.similarity_calc.levenshtein_distance(word, possible) > 1:
                                continue
                            possible_word.possible_words.add(possible)
                    self.__word_queue.put(possible_word)


    def __typo_ask(self):
        while self.__reading:
            if not self.__word_queue.empty():
                word: Corrector.UnknownWord = self.__word_queue.get()
                print("Našli jsme pravděpodobný překlep ve slově:")
                print(word.word)
                print("Nalezené podobnosti:")
                print(word.possible_words)
                print()


    def correct_file(self, to_correct: str):
        # clean shared data of correcting file
        self.__word_queue = Queue() # new queue
        self.__line_counter = 0

        # correction
        corrector_threads: list[threading.Thread] = []
        with open(to_correct, "r") as file:
            self.__reading = True
            for _ in range(int(os.cpu_count()/2)-1):
                corrector_threads.append(
                        threading.Thread(target=self.__corrector, args=(file,))
                )
            corrector_threads.append(
                    threading.Thread(target=self.__typo_ask)
            )

            for t_x in corrector_threads:
                t_x.start()

            for t_x in corrector_threads:
                t_x.join()
