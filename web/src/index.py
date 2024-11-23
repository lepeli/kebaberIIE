import os
import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)

# Fonction pour établir une connexion à la base de données PostgreSQL
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host='postgres',  # Nom du service pour le conteneur Docker, ou adresse de votre base
            database=os.environ['POSTGRES_USER'],  # Utiliser le nom de la base de données définie dans Docker ou dans votre configuration PostgreSQL
            user=os.environ['POSTGRES_USER'],  # Utilisateur de la base de données
            password=os.environ['POSTGRES_PASSWORD']  # Mot de passe de l'utilisateur
        )
        print("Connexion réussie à la base de données")
        return conn
    except Exception as e:
        print(f"Erreur de connexion à la base de données : {e}")
        raise

@app.route('/formulaire_avis/<int:id>')
def formulaire_avis(id:int):
    print(id)
    return render_template('formulaire_avis.html')

@app.route('/ajout_restaurant')
def formulaire_restaurant():
    return render_template('ajout_restaurant.html')


@app.post('/ajout_avis/<int:id>')
def ajout_avis(id:int):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        query = """
        INSERT INTO  Avis (restaurant, commentaire, note, url_photo) VALUES
        (%s, %s, %s, %s)

        """
        cur.execute(query, (id, request.form["commentaire"], request.form["note"], request.form["url_photo"]))
    except psycopg2.Error as e:
        print(f"Erreur lors de l'exécution de la requête SQL : {e}")
    finally:
        conn.close()
    return render_template("restaurant.html", id =id)

@app.post('/ajout_restaurant')
def ajout_restaurant():
    print(request.form)
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        query = """
        INSERT INTO  Restaurant (nom, adresse, code_postal, site_web, url_photo, prix ) VALUES
        (%s, %s, %s, %s, %s, %s)

        """
        cur.execute(query, (id, request.form["nom"], request.form["adresse"], request.form["code_postal"],
                    request.form["site_web"], request.form["url_photo"], request.form["prix"]))
    except psycopg2.Error as e:
        print(f"Erreur lors de l'exécution de la requête SQL : {e}")
    finally:
        conn.close()
    return render_template("formulaire_avis.html")

# Route principale pour afficher les restaurants et leurs avis
@app.route('/')
def index():
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        # Requête SQL pour récupérer les restaurants avec leurs informations et note moyenne
        query = """
        SELECT r.id, r.nom, r.adresse, r.site_web, r.url_photo,
               COALESCE(AVG(a.note), 0) AS moyenne_note
        FROM "Restaurant" r
        LEFT JOIN "Avis" a ON r.nom = a.restaurant
        GROUP BY r.id, r.nom, r.adresse, r.site_web, r.url_photo
        ORDER BY moyenne_note DESC;
        """
        cur.execute(query)
        restaurants = cur.fetchall()
        cur.close()
    except psycopg2.Error as e:
        print(f"Erreur lors de l'exécution de la requête SQL : {e}")
        restaurants = []
    finally:
        conn.close()

    # Passer la liste des restaurants au template
    return render_template('index.html')

# Lancement de l'application Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)