import hashlib

from sqlalchemy.orm import scoped_session

def encrypt(string):
    return hashlib.sha256(string.encode("utf-8")).hexdigest()

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
    def __init__(self, db):
        self.users = {1: Usr("utilisateur", "fr", 1), 2: Usr("user", "en", 2)}
        self.db = db

    def check_new_usr(self, form, passwd2):
        if form.lang == None or form.pref_lang == None:
            return "err-no-lang"
        elif form.usr_name == "" or self.db.execute("SELECT * FROM users WHERE usr_name = :usr_name", {"usr_name": form.usr_name}).rowcount != 0:
            return "err-usr-name"
        elif form.passwd == "" or form.passwd != passwd2 or len(form.passwd) < 6:
            return "err-passwd"
        else:
            return "success"

    def add_usr(self, form):
        try:
            self.db.execute("INSERT INTO users (usr_name, passwd, lang_nat, lang_pref) VALUES (:usr_name, :passwd, :lang_nat, :lang_pref)", {"usr_name": form.usr_name, "passwd": encrypt(form.passwd), "lang_nat": form.lang, "lang_pref": form.pref_lang})
            self.db.commit()
        except:
            return False
        return True

    def check_login(self, usr_name, passwd):
        acct_info = self.db.execute("SELECT usr_name, passwd FROM users WHERE usr_name = :usr_name", {"usr_name": usr_name}).fetchone()
        if acct_info == None:
            return False
        elif acct_info.passwd != encrypt(passwd):
            return False
        return True

    def login(self, usr_name):
        acct_info = self.db.execute("SELECT id, usr_name, lang_pref FROM users WHERE usr_name = :usr_name", {"usr_name": usr_name}).fetchone()
        return Usr(acct_info.usr_name, acct_info.lang_pref, acct_info.id)

class Books:

    def __init__(self, db):
        self.books = [["The Way of Shadows", "en", 1257],["The Fellowship of the Ring", "en", 3480],["Le Petit Prince", "fr", 1563]]

    def search(self, search):
        return self.books

class Reviews:
    
    def __init__(self, db):
        self.reviews = {1257:[[1,"en","en",5,"this is a good book",5,"C'est une bonne livre"]],
                3480:[[1,"en","en",4,"interesting read",4,"C'est interesant"]],
                1563:[[1,"en","en",5,"a fun book",5,"une livre jouable"],[2,"fr","fr",5,"a great literary work",5,"une bonne oeuvre literare"]]}

    def search(self, book_id):
        return self.reviews[book_id]

    def add(self, book_id, usr_id, review):
        return 0

if __name__ == "__main__":
    print("This is a module to manage specific databases within a flask app.  It provides no standalone functionality")
