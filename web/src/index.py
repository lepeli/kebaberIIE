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

# Fonction pour déterminer la fourchette de prix
def get_price_range(prix):
    if prix < 10:
        return "Moins de 10€"
    elif 10 <= prix < 20:
        return "10€ à 20€"
    elif 20 <= prix < 30:
        return "20€ à 30€"
    elif 30 <= prix < 50:
        return "30€ à 50€"
    else:
        return "Plus de 50€"        

@app.route('/formulaire_avis/<int:restaurant_id>')
def formulaire_avis(restaurant_id):
    return render_template('formulaire_avis.html', restaurant_id=restaurant_id)

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

@app.route('/restaurant/<int:restaurant_id>')
def restaurant_details(restaurant_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        # Récupérer les informations du restaurant
        cur.execute("""
            SELECT id, nom, adresse, code_postal, site_web, url_photo, prix
            FROM Restaurant WHERE id = %s;
        """, (restaurant_id,))
        restaurant = cur.fetchone()

        # Récupérer les avis du restaurant
        cur.execute("""
            SELECT id, restaurant, commentaire, note, url_photo
            FROM Avis WHERE restaurant = %s;
        """, (restaurant_id,))
        avis = cur.fetchall()

        cur.close()
    except Exception as e:
        print(f"Erreur lors de la récupération des données du restaurant : {e}")
        return "Erreur lors de la récupération des données.", 500
    finally:
        conn.close()

    # Vérifier si le restaurant existe
    if not restaurant:
        return "Restaurant introuvable.", 404

    # Passer les données et la fonction au template
    return render_template('restaurant.html', restaurant=restaurant, avis=avis, get_price_range=get_price_range)



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
        cur.execute(query, (request.form["nom"], request.form["adresse"], request.form["code_postal"],
                    request.form["site_web"], request.form["url_photo"], request.form["prix"]))
        cur.execute("commit;")
    except psycopg2.Error as e:
        print(f"Erreur lors de l'exécution de la requête SQL : {e}")
    finally:
        conn.close()
    return render_template("formulaire_avis.html")


# Route principale pour afficher les restaurants et leur note moyenne
@app.route('/')
def index():
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        # Requête SQL pour récupérer les restaurants avec leur note moyenne
        query = """
        SELECT r.id, r.nom, r.adresse, r.code_postal, r.site_web, r.url_photo, r.prix,
               COALESCE(AVG(a.note), 0) AS moyenne_note
        FROM Restaurant r
        LEFT JOIN Avis a ON r.id = a.restaurant
        GROUP BY r.id, r.nom, r.adresse, r.code_postal, r.site_web, r.url_photo, r.prix
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
    return render_template('index.html', restaurants=restaurants, get_price_range=get_price_range)




# Lancement de l'application Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)