from Word import Word
def tail(word: str) -> str:
    return word[1:]
class SimilarityCalculator:
    def __init__(self):
        self.memory: dict[frozenset, int] = {}
        self.words_by_len: dict[int, set[Word]] = {}

    def __find_in_memory_or_calc(self, a: str, b: str) -> int:
        found = self.memory.get(frozenset([a,b]))
        if found is not None:
            return found
        else:
            sim = self.levenshtein_distance(tail(a), tail(b))
            self.memory[frozenset([a,b])] = sim
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

    def old_levenshtein_distance(self, a: str, b: str) -> int:
        if len(b) == 0:
            return len(a)
        elif len(a) == 0:
            return len(b)
        elif a[0] == b[0]:
            return self.old_levenshtein_distance(tail(a), tail(b))
        else:
            return 1+min(self.old_levenshtein_distance(tail(a), b),
                         self.old_levenshtein_distance(a, tail(b)),
                         self.old_levenshtein_distance(tail(a), tail(b)))