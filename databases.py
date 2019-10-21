class Usrs:

    def __init__(self):
        self.usr_name = "usr_name"
        self.passwd = "password"
        self.lang = "en"
        self.pref_lang = "en"

    def login(self, usr, passwd):
        if (usr == self.usr_name) and (passwd == self.passwd):
            return True
        else:
            return False

    def usr_lang(self):
        return {"1st_lang":self.lang, "pref_lang":self.pref_lang}

class Books:

    def __init__(self):
        self.books = [["The Way of Shadows", "en", 1257],["The Fellowship of the Ring", "en", 3480],["Le Petit Prince", "fr", 1563]]

    def search(self):
        return self.books

class Reviews:
    
    def __init__(self):
        self.reviews = {1257:[["usr_name","en","en",5,"this is a good book",5,"C'est une bonne livre"]],
                3480:[["usr_name","en","en",4,"interesting read",4,"C'est interesant"]],
                1563:[["usr_name","en","en",5,"a fun book",5,"une livre jouable"],["other_usr","fr","fr",5,"a great literary work",5,"une bonne oeuvre literare"]]}

    def search(self, book_id):
        return self.reviews[book_id]

