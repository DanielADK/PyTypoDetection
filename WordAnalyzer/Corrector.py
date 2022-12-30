import os
import time
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
        self.file_reader: FileReader = fr
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

    def __corrector(self, to_do: list[str]) -> None:
        print(fg.li_green + "Starting corrector thread: " + threading.current_thread().name + fg.white)
        for word in to_do:
            word = process(word)
            if len(word) == 0:
                continue
            if self.words_by_len.get(len(word)) is not None and word not in self.words_by_len.get(len(word)):
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
                for possible in self.words_by_len.get(len(word)+1):
                    if self.similarity_calc.levenshtein_distance(word, possible) > 1:
                        continue
                    possible_word.possible_words.add(possible)
                self.__word_queue.put(possible_word)


    def __typo_ask(self):
        print(fg.li_green + "Starting UI thread: " + threading.current_thread().name + fg.rs)
        while self.__reading:
            if not self.__word_queue.empty():
                word: Corrector.UnknownWord = self.__word_queue.get()
                print("Našli jsme pravděpodobný překlep na řádku " + str(word.line) + " ve slově:")
                print(word.word)
                if len(word.possible_words) > 0:
                    print("Nalezené podobnosti:")
                    print(word.possible_words)
                print()
            time.sleep(0.1)


    def correct_file(self, to_correct: str):
        # clean shared data of correcting file
        self.__word_queue = Queue() # new queue

        # correction
        corrector_threads: list[threading.Thread] = []
        with open(to_correct, "r") as file:
            self.__reading = True
            cpu_count = int(os.cpu_count()/2)-1
            for i in range(cpu_count):
                corrector_threads.append(
                    threading.Thread(
                        target=self.__corrector,
                        args=(self.file_reader.to_correct_content[i::cpu_count],)
                    )
                )

            typo_thread: threading.Thread = threading.Thread(target=self.__typo_ask)

            for t_x in corrector_threads:
                t_x.start()
            typo_thread.start()

            for t_x in corrector_threads:
                t_x.join()
            self.__reading = False
