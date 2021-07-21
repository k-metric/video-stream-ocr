# TODO: Support regexes
# TODO: Escape comma and move to a better interchange format
# Rudimentary text detection.
class TextProcessor:

    def __init__(self, terms_csv):
        self.terms = terms_csv.split(',')

    # Look for the terms in the text.
    def search(self, text):
        for term in self.terms:
            if term in text:
                return True
            else:
                return False
