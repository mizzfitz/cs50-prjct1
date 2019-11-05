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
        self.db = db

    def escape_chars(self, text):
        return text.replace("'", "''")

    def search(self, search):
        search = self.escape_chars(search)
        db_namespc = ["isbn","title","author"]
        result = []
        for i in db_namespc:
            command = f"SELECT isbn, title, author, year, lang FROM books WHERE {i} LIKE '%{search.lower()}%' LIMIT 20;"
            result = result + self.db.execute(command).fetchall()
        return result

    def get_id_by_isbn(self, isbn):
        return self.db.execute("SELECT id FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone().id

    def get_by_isbn(self, isbn):
        keys = ["first_lang_stars", "second_lang_stars"]
        response = {"book": self.db.execute("SELECT id, isbn, title, author, year, lang FROM books WHERE isbn = :isbn;", {"isbn": isbn}).fetchone()}
        command = f"SELECT COUNT(*) FROM reviews WHERE book_id = {response['book'].id} GROUP BY book_id;"
        count = self.db.execute(command).fetchone()
        if count:
            response["review_count"] = count.count
        else:
            response["review_count"] = 0
        for k in keys:
            command = f"SELECT AVG({k}) FROM reviews WHERE book_id = {response['book'].id} GROUP BY book_id;"
            value = self.db.execute(command).fetchone()
            # if we have a response, format it into a readable string
            if value:
                response[k] = str(value.avg)
                # truncate avg rating to 1 decimal place or the last digit before a zero
                if ".0" in response[k]:
                    response[k] = response[k][0:3]
                elif "0" in response[k]:
                    i = response[k].find("0")
                    response[k] = response[k][0:i]
            else:
                response[k] = value
        return response

    def get_review_by_book_id(self, book_id):
        return self.db.execute("SELECT first_lang_stars, second_lang_stars, first_lang_review, second_lang_review, usr_name, lang_nat FROM reviews JOIN users ON reviews.usr_id = users.id WHERE reviews.book_id = :book_id;", {"book_id": book_id}).fetchall()

    def check_reviewer(self, usr_id, book_id):
        command = f"SELECT COUNT(*) FROM reviews WHERE book_id = {book_id} AND usr_id = {usr_id};"
        check = self.db.execute(command).fetchone()
        if check.count == 0:
            return True;
        else:
            return False;

    def add_review(self, book_id, usr_id, review_form):
        review = review_form.copy()
        review['1st_lang_review'] = self.escape_chars(review['1st_lang_review'])
        review['2nd_lang_review'] = self.escape_chars(review['2nd_lang_review'])
        command = f"INSERT INTO reviews (usr_id, book_id, first_lang_stars, second_lang_stars, first_lang_review, second_lang_review) VALUES ({usr_id}, {book_id}, {review['1st_lang_star']}, {review['2nd_lang_star']}, '{review['1st_lang_review']}', '{review['2nd_lang_review']}')"
        self.db.execute(command)
        self.db.commit()
        return 0

if __name__ == "__main__":
    print("This is a module to manage specific databases within a flask app.  It provides no standalone functionality")
