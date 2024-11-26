
INSERT INTO Restaurant (id, nom, adresse, code_postal, site_web, url_photo, prix)
VALUES
    (1,'Klassiker',' 12 Cr Mgr Roméro, 91000 Évry-Courcouronnes',
    '91000', 'https://theklassiker.fr/','https://b3386818.smushcdn.com/3386818/wp-content/uploads/2021/11/The-Klassiker-Logo-e1636226243760.png?lossy=1&strip=1&webp=1', 12.90),
    (2,'Restaurant Anatolia', '14 Cr Mgr Roméro, 91000 Évry-Courcouronnes',
    '91000', NULL, 'https://lh3.googleusercontent.com/p/AF1QipObPLGRXtUaslQIwDI2VSs2EsOU8MeSqgktUpY5=s680-w680-h510',9.00)
    ;

ALTER SEQUENCE restaurant_id_seq RESTART WITH 3;

INSERT INTO Avis (restaurant, commentaire, note, url_photo)
VALUES
    (1, 'Très bon restaurant. Service agréable et rapide', 9,NULL),
    (1, 'Très bon rapport qualité prix. Service rapide si on commande par internet', 8, NULL),
    (2, 'Bon kebab', 6,NULL);

ALTER SEQUENCE avis_id_seq RESTART WITH 4;
