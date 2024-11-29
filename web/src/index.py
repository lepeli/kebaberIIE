import os
import psycopg2
import secrets
import pathlib
import json

from io import BytesIO
from minio import Minio
from redis import Redis
from flask import Flask, render_template, request, redirect, url_for


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
    # Connexion à la base de données
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        # Requête SQL pour récupérer le nom du restaurant
        cur.execute("SELECT nom FROM Restaurant WHERE id = %s", (restaurant_id,))
        restaurant = cur.fetchone()  # Récupérer un seul résultat (le restaurant)
        cur.close()

        if restaurant:
            nom_du_restaurant = restaurant[0]
        else:
            nom_du_restaurant = "Restaurant introuvable"
    except Exception as e:
        print(f"Erreur lors de la récupération du restaurant : {e}")
        nom_du_restaurant = "Erreur lors de la récupération du nom"

    finally:
        conn.close()

    # Passer restaurant_id et nom_du_restaurant au template
    return render_template('formulaire_avis.html', restaurant_id=restaurant_id, nom_du_restaurant=nom_du_restaurant)


@app.route('/ajout_restaurant')
def formulaire_restaurant():
    return render_template('ajout_restaurant.html')



@app.route('/ajout_avis', methods=['POST'])
def ajout_avis():
    # Récupérer les données du formulaire
    restaurant_id = request.form['restaurant_id']
    commentaire = request.form['commentaire']
    note = request.form['note']

    # Connexion à la base de données
    conn = get_db_connection()  # Utilise la fonction de connexion PostgreSQL
    cursor = conn.cursor()
    picture_url = None
    # Check if a picture has been uploaded by the user

    # Insérer les données dans la table des avis
    try:

        if request.files["photo"].filename != "":
            picture_url = uploadFile(request.files["photo"])# to do stuff with the picture

        cursor.execute("""
            INSERT INTO avis (restaurant, commentaire, note, url_photo)
            VALUES (%s, %s, %s, %s)
        """, (restaurant_id, commentaire, note, picture_url))
        cursor.execute("commit;")
        # Commit la transaction pour valider l'insertion
        conn.commit()  # Cette ligne est nécessaire pour enregistrer l'avis dans la base de données
    except Exception as e:
        print("Erreur lors de l'insertion :", e)
        conn.rollback()  # Si une erreur se produit, on annule les changements
    finally:
        conn.close()

    # Rediriger l'utilisateur vers la page du restaurant après l'ajout de l'avis
    return redirect(url_for('restaurant_details', restaurant_id=restaurant_id))


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
    restaurant_id=None
    conn = get_db_connection()
    try:

        picture_url = None
        # check if files exists

        if request.files["photo"].filename != "":
            picture_url = uploadFile(request.files["photo"])# to do stuff with the picture

        cur = conn.cursor()
        query = """
        INSERT INTO  Restaurant (nom, adresse, code_postal, site_web, url_photo, prix ) VALUES
        (%s, %s, %s, %s, %s, %s)
        RETURNING id
        """
        cur.execute(query, (request.form["nom"], request.form["adresse"], request.form["code_postal"],
                    request.form["site_web"], picture_url, request.form["prix"]))
        restaurant_id=cur.fetchone()[0]
        cur.execute("commit;")
    except psycopg2.Error as e:
        print(f"Erreur lors de l'exécution de la requête SQL : {e}")
    finally:
        conn.close()
    return redirect(url_for('restaurant_details', restaurant_id=restaurant_id))


# Route principale pour afficher les restaurants et leur note moyenne
@app.route('/')
def index():
    query = request.args.get('query')  # Récupérer la requête de recherche depuis l'URL
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        
        if query:
            # Si une requête de recherche est présente, filtrer les restaurants par nom
            query_sql = """
                SELECT r.id, r.nom, r.adresse, r.code_postal, r.site_web, r.url_photo, r.prix,
                       COALESCE(AVG(a.note), 0) AS moyenne_note
                FROM Restaurant r
                LEFT JOIN Avis a ON r.id = a.restaurant
                WHERE r.nom ILIKE %s  -- Utilisation de ILIKE pour une recherche insensible à la casse
                GROUP BY r.id, r.nom, r.adresse, r.code_postal, r.site_web, r.url_photo, r.prix
                ORDER BY moyenne_note DESC;
            """
            cur.execute(query_sql, ('%' + query + '%',))  # Recherche avec les pourcentages pour correspondre à n'importe où dans le nom
        else:
            # Si aucune requête de recherche, récupérer tous les restaurants
            query_sql = """
                SELECT r.id, r.nom, r.adresse, r.code_postal, r.site_web, r.url_photo, r.prix,
                       COALESCE(AVG(a.note), 0) AS moyenne_note
                FROM Restaurant r
                LEFT JOIN Avis a ON r.id = a.restaurant
                GROUP BY r.id, r.nom, r.adresse, r.code_postal, r.site_web, r.url_photo, r.prix
                ORDER BY moyenne_note DESC;
            """
            cur.execute(query_sql)
        
        restaurants = cur.fetchall()
        cur.close()
    except psycopg2.Error as e:
        print(f"Erreur lors de l'exécution de la requête SQL : {e}")
        restaurants = []
    finally:
        conn.close()

    # Passer la liste des restaurants et le terme de recherche au template
    return render_template('index.html', restaurants=restaurants, get_price_range=get_price_range, query=query)



def uploadFile(file):
    """Uploads and add return a URL"""
    mini = Minio(
            endpoint=os.environ["S3_BUCKET_ADDRESS"],
            region=os.environ["S3_BUCKET_REGION"],
            access_key=os.environ["S3_BUCKET_ACCESS_KEY_ID"],
            secret_key=os.environ["S3_BUCKET_SECRET_ACCESS_KEY"]
            )
    extension = "".join(pathlib.Path(file.filename).suffixes)
    filename = secrets.token_urlsafe(10) + extension
    mini.put_object(os.environ["S3_BUCKET_NAME"], filename, file, os.fstat(file.fileno()).st_size)
    askForCompression(filename)
    return os.environ["S3_BUCKET_PUBLIC_ADDRESS"] + "/" + filename    

    pass

def askForCompression(imagePath):
    """Sends the image to be processed into the Redis queue system"""
    r = Redis("redis", port=6379)
    r.rpush("compressing_queue", json.dumps({"image": imagePath}))

# Lancement de l'application Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)