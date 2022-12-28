from WordAnalyzer.Word import Word
from WordAnalyzer.FileReader import FileReader
from collections import defaultdict
def tail(word: str) -> str:
    return word[1:]
class SimilarityCalculator:
    def __init__(self):
        self.memory: defaultdict[str, dict[str, int]] = defaultdict(dict)

    def __find_in_memory_or_calc(self, a: str, b: str) -> int:
        if a < b:
            found = self.memory.get(a)
            if found is not None:
                found = found.get(b)

        else:
            found = self.memory.get(b)
            if found is not None:
                found = found.get(a)
        if found is not None:
            return found
        else:
            sim = self.levenshtein_distance(tail(a), tail(b))
            if a < b:
                self.memory[a][b] = sim
            else:
                self.memory[b][a] = sim
            return sim


    def levenshtein_distance(self, a: str, b: str) -> int:
        if len(b) == 0:
            return len(a)
        elif len(a) == 0:
            return len(b)
        elif a[0] == b[0]:
            return self.__find_in_memory_or_calc(a, b)

        else:
            return 1 + min(self.__find_in_memory_or_calc(tail(a), b),
                           self.__find_in_memory_or_calc(a, tail(b)),
                           self.__find_in_memory_or_calc(tail(a), tail(b)))