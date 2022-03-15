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
def getPrzyslowia():
    db_connection = sqlite3.connect(db_name)
    c = db_connection.cursor()

    ret = c.execute('SELECT id, tresc FROM Przyslowia')
    przyslowia = []
    for row in ret:
        przyslowia.append({'id': row[0], 'content': row[1]})
    return jsonify(przyslowia)

@app.route('/przyslowie/<id>', methods=['GET'])
def getPrzyslowie(id):
    db_connection = sqlite3.connect(db_name)
    c = db_connection.cursor()

    ret = c.execute('SELECT id, tresc FROM Przyslowia WHERE id LIKE \"' + id + '\"')
    for row in ret:
        wiktionary_uri = "https://pl.wiktionary.org/wiki/" + row[1].replace(' ', '_') + "#pl"
        return jsonify( {'id': row[0], 'content': row[1], 'wiktionary': wiktionary_uri} )

    return "", 404

@app.route('/randomPrzyslowie', methods=['GET'])
def getRandomPrzyslowie():
    db_connection = sqlite3.connect(db_name)
    c = db_connection.cursor()

    ret = c.execute('SELECT id, tresc FROM Przyslowia ORDER BY RANDOM() LIMIT 1')
    row = ret.fetchall()[0]
    print(row)
    przyslowia_dict = {'id': row[0], 'content': row[1]}
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
