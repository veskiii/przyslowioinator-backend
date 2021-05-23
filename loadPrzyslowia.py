import sqlite3
from sqlite3 import Error

db_name = 'przyslowia.db'


def create_database():
    try:
        db_connection = sqlite3.connect(db_name)
        c = db_connection.cursor()

        c.execute('CREATE TABLE Przyslowia (id INTEGER PRIMARY KEY AUTOINCREMENT, tresc varchar(4095))')

        db_connection.commit()

    except Error as e:
        print(e)
    finally:
        pass


def main():
    db_connection = sqlite3.connect(db_name)
    c = db_connection.cursor()

    with open('przyslowia.txt', 'r') as f:
        przyslowia = f.readlines()

    for przyslowie in przyslowia:
        try:
            c.execute('INSERT INTO Przyslowia (tresc) VALUES (?)', (przyslowie[:-1],))
            db_connection.commit()

        except sqlite3.Error as err:
            print("Błąd przy dodawaniu")


if __name__ == '__main__':
    create_database()
    main()