from pathlib import Path


class AutoCompleteData:
    """This class defines the structure of a returning completion"""

    def __init__(self, completed_sentence, source_text, offset, score):
        self.completed_sentence = completed_sentence
        self.source_text = source_text
        self.offset = offset
        self.score = score

    def get_score(self):
        pass

    def __repr__(self):
        return f"{self.completed_sentence[:-1]} ({Path(self.source_text).parts[-1].split('.')[0]} {self.offset})"
