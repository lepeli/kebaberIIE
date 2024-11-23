
INSERT INTO Restaurant (id, nom, adresse, code_postal, site_web, url_photo, prix)
VALUES
    (1,'Klassiker',' 12 Cr Mgr Roméro, 91000 Évry-Courcouronnes',
    '91000', 'https://theklassiker.fr/','https://b3386818.smushcdn.com/3386818/wp-content/uploads/2021/11/The-Klassiker-Logo-e1636226243760.png?lossy=1&strip=1&webp=1', 12.90),
    ('Restaurant Anatolia', '14 Cr Mgr Roméro, 91000 Évry-Courcouronnes',
    '91000', NULL, 'https://lh3.googleusercontent.com/p/AF1QipObPLGRXtUaslQIwDI2VSs2EsOU8MeSqgktUpY5=s680-w680-h510',9.00)
    ;

INSERT INTO Avis (restaurant, commentaire, note, url_photo)
VALUES
    (2,'Klassiker', 'Très bon restaurant. Service agréable et rapide', 9,
    NULL),
    ('Klassiker', 'Très bon rapport qualité prix. Service rapide si on commande par internet', 8,
    NULL),
    ('Restaurant Anatolia', 'Bon kebab', 6,NULL)
    ;