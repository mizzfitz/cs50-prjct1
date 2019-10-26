class Usr:

    def __init__(self, usr_name, pref_lang="", usr_id=0):
        self.usr_name = usr_name
        self.pref_lang = pref_lang
        self.usr_id = usr_id

class User(Usr):
    def __init__(self, usr_name, passwd, pref_lang="", lang="", usr_id=0):
        super().__init__(usr_name, pref_lang)
        self.passwd = passwd
        self.lang = lang
        self.usr_id = usr_id

class Users:
    def __init__(self):
        self.users = {1: Usr("utilisateur", "fr", 1), 2: Usr("user", "en", 2)}

    def check_new_usr(self, form, passwd2):
        if form.lang == None or form.pref_lang == None:
            return "err-no-lang"
        elif form.usr_name == "":
            return "err-usr-name"
        elif form.passwd == "" or form.passwd != passwd2:
            return "err-passwd"
        else:
            return "success"

    def add_usr(self, form):
        return True

    def check_login(self, usr_name, passwd):
        return 2

    def login(self, usr_id):
        return self.users[usr_id]

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
