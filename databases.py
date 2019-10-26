class Usr:

    def __init__(self, usr_name, usr_id=0, pref_lang=""):
        self.usr_id = usr_id
        self.usr_name = usr_name
        self.passwd = "password"
        self.lang = "en"
        self.pref_lang = pref_lang

class Users:
    def __init__(self):
        self.users = {1: Usr("usr_name"), 2: Usr("usr_2")}

    def get_usr(self, usr_id):
        return self.users.get(usr_id)

    def login(self, usr_name, passwd):
        return Usr("free-user")

class Books:

    def __init__(self):
        self.books = [["The Way of Shadows", "en", 1257],["The Fellowship of the Ring", "en", 3480],["Le Petit Prince", "fr", 1563]]

    def search(self):
        return self.books

class Reviews:
    
    def __init__(self):
        self.reviews = {1257:[[1,"en","en",5,"this is a good book",5,"C'est une bonne livre"]],
                3480:[[1,"en","en",4,"interesting read",4,"C'est interesant"]],
                1563:[[1,"en","en",5,"a fun book",5,"une livre jouable"],[2,"fr","fr",5,"a great literary work",5,"une bonne oeuvre literare"]]}

    def search(self, book_id):
        return self.reviews[book_id]

if __name__ == "__main__":
    print("This is a module to manage specific databases within a flask app.  It provides no standalone functionality")
