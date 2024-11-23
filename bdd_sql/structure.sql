--- FICHIER CONTENANT LES DÉFINITIONS DES TABLES

CREATE TABLE IF NOT EXISTS Restaurant(
    id SERIAL PRIMARY KEY NOT NULL,
    nom VARCHAR(40) NOT NULL,
    adresse VARCHAR(200) NOT NULL,
    code_postal VARCHAR(40),
    site_web VARCHAR(60),
    url_photo VARCHAR(200),
    prix FLOAT
);


CREATE TABLE IF NOT EXISTS Avis(
    id SERIAL PRIMARY KEY REFERENCES Restaurant(id) NOT NULL,
    commentaire VARCHAR(500) NOT NULL,,
    restaurant VARCHAR(40) 
	note INT NOT NULL,
    url_photo VARCHAR(200)
);
