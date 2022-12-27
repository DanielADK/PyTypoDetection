class Word:
    def __init__(self, word: str):
        self.word: str = word
        self.frequency: int = 1
        self.pre_words: set[Word] = set()
        self.post_words: set[Word] = set()