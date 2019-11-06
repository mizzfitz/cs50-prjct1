import hashlib

from sqlalchemy.orm import scoped_session

def escape_chars(text):
    """ function for escaping single quotes in user input into sql """
    return text.replace("'", "''")

def encrypt(string):
    """ this function manages string encryption used for storing and checking user passwords against the database.
    It's contained in its own function for readability and to facilitate easier maintenance in the event of a change to encryption type """
    return hashlib.sha256(string.encode("utf-8")).hexdigest()

class Usr:
    """ the most basic user object.  This is what is stored in session variables and does not include a password """

    def __init__(self, usr_name, pref_lang="", usr_id=0):
        self.usr_name = usr_name
        self.pref_lang = pref_lang
        self.usr_id = usr_id

class User(Usr):
    """ this class is only used for creating user accounts so it contains a password variable.
    It was only writen as an easier to use data type and should probably be phased out in maintenance """

    def __init__(self, usr_name, passwd, pref_lang="", lang="", usr_id=0):
        super().__init__(usr_name, pref_lang)
        self.passwd = passwd
        self.lang = lang
        self.usr_id = usr_id

class Users:
    """ the main class for interacting with the user database """

    def __init__(self, db):
        # set database engine
        self.db = db

    def check_new_usr(self, form, passwd2):
        """ this function checks a new user entry form taking as input a User object (form) and a string (passwd2) and returning a string.
        String evaluates as a key for an error message displayed to the user identifying why the form was not accepted.
        NOTE:  this function does not actually add a user to the database, only evaluates the form entry for correctness """

        # escape singlequote from username for database purposes
        form.usr_name = escape_chars(form.usr_name)
        # require user to select prefered language and first language
        if form.lang == None or form.pref_lang == None:
            return "err-no-lang"
        # require original user name
        elif form.usr_name == "" or self.db.execute("SELECT * FROM users WHERE usr_name = :usr_name", {"usr_name": form.usr_name}).fetchall().rowcount != 0:
            return "err-usr-name"
        # password requirements
        elif form.passwd == "" or form.passwd != passwd2 or len(form.passwd) < 6:
            return "err-passwd"
        # new user form appears to be correct
        else:
            return "success"

    def add_usr(self, form):
        """ this function actually adds a new user to the database, taking a User object as input.
        Placed inside a try catch to manage any potential race conditions. """

        # escape singlequote from username for sql purposes
        form.usr_name = escape_chars(form.usr_name)
        try:
            self.db.execute("INSERT INTO users (usr_name, passwd, lang_nat, lang_pref) VALUES (:usr_name, :passwd, :lang_nat, :lang_pref)", {"usr_name": form.usr_name, "passwd": encrypt(form.passwd), "lang_nat": form.lang, "lang_pref": form.pref_lang})
            self.db.commit()
        except:
            return False
        return True

    def check_login(self, usr_name, passwd):
        """ function to check user credentials for login. Returns true or false """

        # escape singlequote from username for sql purposes
        usr_name = escape_chars(usr_name)
        acct_info = self.db.execute("SELECT usr_name, passwd FROM users WHERE usr_name = :usr_name", {"usr_name": usr_name}).fetchone()
        if acct_info == None:
            return False
        elif acct_info.passwd != encrypt(passwd):
            return False
        return True

    def login(self, usr_name):
        """ function to login a user. Returns Usr object to be stored in session variable """

        # escape singlequote from username for sql purposes
        usr_name = escape_chars(usr_name)
        acct_info = self.db.execute("SELECT id, usr_name, lang_pref FROM users WHERE usr_name = :usr_name", {"usr_name": usr_name}).fetchone()
        return Usr(acct_info.usr_name, acct_info.lang_pref, acct_info.id)

class Books:
    """ this class manages interaction with the books and reviews databases. """

    def __init__(self, db):
        # set database engine
        self.db = db

    def search(self, search):
        """ function to search for a book based on a single search term.
        Returns search results by title first, then author, then isbn """

        search = escape_chars(search)
        db_namespc = ["title","author","isbn"]
        result = []
        for i in db_namespc:
            command = f"SELECT isbn, title, author, year, lang FROM books WHERE {i} LIKE '%{search.lower()}%' LIMIT 20;"
            result = result + self.db.execute(command).fetchall()
        return result

    def get_id_by_isbn(self, isbn):
        """ return book id based on book isbn """
        return self.db.execute("SELECT id FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone().id

    def get_by_isbn(self, isbn):
        """ return book info (including review stats) based on isbn """

        keys = ["first_lang_stars", "second_lang_stars"]
        response = {"book": self.db.execute("SELECT id, isbn, title, author, year, lang FROM books WHERE isbn = :isbn;", {"isbn": isbn}).fetchone()}
        command = f"SELECT COUNT(*) FROM reviews WHERE book_id = {response['book'].id} GROUP BY book_id;"
        count = self.db.execute(command).fetchone()
        
        # format review count
        if count:
            response["review_count"] = count.count
        else:
            response["review_count"] = 0

        for k in keys:
            command = f"SELECT AVG({k}) FROM reviews WHERE book_id = {response['book'].id} GROUP BY book_id;"
            value = self.db.execute(command).fetchone()

            # if we have a response, format it into a user friendly string
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
        """ returns an iterable of reviews for a given book_id """
        return self.db.execute("SELECT first_lang_stars, second_lang_stars, first_lang_review, second_lang_review, usr_name, lang_nat FROM reviews JOIN users ON reviews.usr_id = users.id WHERE reviews.book_id = :book_id;", {"book_id": book_id}).fetchall()

    def check_reviewer(self, usr_id, book_id):
        """ check if a user has already submited a review in order to disallow individual users from submiting multiple reviews """

        command = f"SELECT COUNT(*) FROM reviews WHERE book_id = {book_id} AND usr_id = {usr_id};"
        check = self.db.execute(command).fetchone()
        if check.count == 0:
            return True;
        else:
            return False;

    def add_review(self, book_id, usr_id, review_form):
        """ insert a book review into the database """
        review = review_form.copy()
        review['1st_lang_review'] = escape_chars(review['1st_lang_review'])
        review['2nd_lang_review'] = escape_chars(review['2nd_lang_review'])
        command = f"INSERT INTO reviews (usr_id, book_id, first_lang_stars, second_lang_stars, first_lang_review, second_lang_review) VALUES ({usr_id}, {book_id}, {review['1st_lang_star']}, {review['2nd_lang_star']}, '{review['1st_lang_review']}', '{review['2nd_lang_review']}')"
        self.db.execute(command)
        self.db.commit()
        return 0

if __name__ == "__main__":
    print("This is a module to manage specific databases within a flask app.  It provides no standalone functionality")
