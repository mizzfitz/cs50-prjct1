import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import csv;

def usage():
    print("USAGE: csv_to_db.py csv_file_path language")
    sys.exit(1)

class Csv_to_db():
    def __init__(self, path, lang):
        if not os.getenv("DATABASE_URL"):
            print("Environment variable DATABASE_URL must be defined")
            sys.exit(1)

        if lang != 'fr' and lang != 'en':
            usage()

        try:
            self.f = open(path)
        except:
            usage()
        self.reader = csv.reader(self.f)
        self.lang = lang
        self.engine = create_engine(os.getenv("DATABASE_URL"))
        self.db = scoped_session(sessionmaker(bind=self.engine))

    def upload_to_db(self):
        for isbn, title, author, year in self.reader:
            if isbn == "isbn" and title == "title" and author == "author" and year == "year":
                print("Formated")
            else:
                print(f"Adding {isbn}, {title}, {author}, {year}, {self.lang} to database...")
                self.db.execute("INSERT INTO books (isbn, title, author, year, lang) VALUES (:isbn, :title, :author, :year, :lang)", {"isbn": isbn, "title": title, "author": author, "year": int(year), "lang": self.lang})
        self.db.commit()

    def clean_up(self):
        self.f.close()

def main():
    if len(sys.argv) < 3 or len(sys.argv) > 3:
        usage()

    db_update = Csv_to_db(sys.argv[1], sys.argv[2])
    db_update.upload_to_db()
    db_update.clean_up()

if __name__ == "__main__":
    main()
