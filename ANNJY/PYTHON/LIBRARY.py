class Library:
    def __init__(self, list_of_books, name ):
        self.bookslist = list_of_books
        self.name = name
        self.lendict = {}

    def displayBooks(self):
        print("")