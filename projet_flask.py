import sqlite3
from flask import Flask
from flask import jsonify, request
from flask_marshmallow import Marshmallow
import pymysql
from pymysql import Error, cursors

app = Flask(__name__)


def db_connexion():
    conn = None
    try:
      conn = pymysql.connect(
    host="localhost",
    database="prj_flask",
    user="root",
    password="primatologue",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)
    except pymysql.error as e:
        print(e)
    return conn


@app.route("/api/article", methods=['GET', 'POST'])
def ajouter_article():
    conn = db_connexion()
    cursor = conn.cursor()

    if request.method == 'GET':
       reque = "SELECT * FROM article"
       cursor.execute(reque)
       article = [
            dict(id=row['id'], nom=row['nom'],description=row['description'], prix=row['prix'], quantite=row['quantite'])
            for row in cursor.fetchall()
        ]
       if article is not None:
            return jsonify(article)

    if request.method == 'POST':
        new_nom = request.form.get('nom')
        new_description = request.form.get('description')
        new_prix = request.form.get('prix')
        new_quantite = request.form.get('quantite')
        

        sql_query = """ INSERT INTO article ( nom, description, prix, quantite)
        VALUES (%s,%s,%s,%s)"""
        cursor.execute(sql_query, ( new_nom, new_description, new_prix, new_quantite))
        conn.commit()
        return f"L'Article: {cursor.lastrowid} a été bien crée", 201

@app.route("/api/categorie", methods=['GET', 'POST'])
def ajouter_categorie():
    conn = db_connexion()
    cursor = conn.cursor()

    if request.method == 'GET':
       reque = "SELECT * FROM categorie"
       cursor.execute(reque)
       categorie = [
            dict(id=row['id'], nom=row['nom'])
            for row in cursor.fetchall()
        ]
       if categorie is not None:
            return jsonify(categorie)

    if request.method == 'POST':
       
        new_nom = request.form.get('nom')
       
        

        sql_query = """ INSERT INTO categorie (nom)
        VALUES (%s)"""
        cursor.execute(sql_query, (new_nom))
        conn.commit()
        return f"La categorie: {cursor.lastrowid} a été bien crée", 201


@app.route('/article/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def update_article(id):
    conn = db_connexion()
    cursor = conn.cursor()
    article = None
    if request.method == 'GET':
        cursor.execute("SELECT * FROM article WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            article = r
            if article is not None:
                return jsonify(article), 200
            else:
                return "Erreur", 404

    if request.method == 'PUT':
        sql_query = """UPDATE article
        SET nom=?,
            description=?,
            prix=?
            quantite=?
        WHERE id=?

        """
        nom = request.form.get('nom')
        description = request.form.get('description')
        prix = request.form.get('prix')
        quantite = request.form.get('quantite')
        updated_article = {
            "id": id,
            "nom": nom,
            "description": description,
            "prix": prix,
            "quantite": quantite
        }
        conn.execute(sql_query, (nom, description, prix,quantite , id))
        conn.commit()
        return jsonify(updated_article)

    if request.method == 'DELETE':
        sql_query = """DELETE FROM article WHERE id=?"""
        conn.execute(sql_query, (id,))
        return "L'article avec id: {} a été bien supprimé ".format(id), 200
    
    
@app.route('/categorie/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def update_categorie(id):
    conn = db_connexion()
    cursor = conn.cursor()
    article = None
    if request.method == 'GET':
        cursor.execute("SELECT * FROM categorie WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            article = r
            if article is not None:
                return jsonify(article), 200
            else:
                return "Erreur", 404

    if request.method == 'PUT':
        sql_query = """UPDATE categorie
        SET nom=?,
           
        WHERE id=?

        """
        nom = request.form.get('nom')
        
        updated_article = {
            "id": id,
            "nom": nom,
           
        }
        conn.execute(sql_query, (nom, id))
        conn.commit()
        return jsonify(updated_article)

    if request.method == 'DELETE':
        sql_query = """DELETE FROM article categorie id=?"""
        conn.execute(sql_query, (id,))
        return "La categorie avec id: {} a été bien supprimé ".format(id), 200        

@app.route('/article/<string:nom>', methods=['GET'])
def chercher_article(nom):
    conn = db_connexion()
    cursor = conn.cursor()
    article = None
    if request.method == 'GET':
        cursor.execute("SELECT * FROM article WHERE nom=?", (nom,))
        rows = cursor.fetchall()
        for r in rows:
            article = r
            if article is not None:
                return jsonify(article), 200
            else:
                return "Erreur", 404
if __name__ == "__main__":
    app.run(debug=True)
