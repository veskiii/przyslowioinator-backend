import sqlite3
from sqlite3 import Error
import random
import flask
from flask import request, jsonify

db_name = 'przyslowia.db'

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = "klucz"

current_session_tokens = {}


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


@app.route('/przyslowia', methods=['GET'])
def losuj_przyslowie():
    db_connection = sqlite3.connect(db_name)
    c = db_connection.cursor()

    ret = c.execute('SELECT id, tresc FROM Przyslowia')
    przyslowia_dict = {'przyslowia': []}
    for row in ret:
        przyslowia_dict['przyslowia'].append({'id': row[0], 'tresc': row[1]})
    return jsonify(przyslowia_dict)


@app.route('/addPrzyslowie', methods=['POST'])
def add_przyslowie():
    json = request.json
    przyslowie = json["przyslowie"]

    db_connection = sqlite3.connect(db_name)
    c = db_connection.cursor()

    try:
        c.execute('INSERT INTO Przyslowia (tresc) VALUES (?)', (przyslowie,))
        db_connection.commit()

        return jsonify({
            "success": True
        })
    except sqlite3.Error as err:
        return jsonify({
            "success": False,
            "error": "Wystąpił błąd przy dodawaniu przysłowia"
        })


if __name__ == '__main__':
    create_database()
    app.run()
