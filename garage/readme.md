# Garage

Simple S3 Storage.

## Production

Actuellement en production, l'instance de garage utilisée est celle déjà mise à disposition au sein de la collocation d'Yvan (la 56k).

## Installation en local

Garage est déjà pré-installé dans le fichier `docker-compose.yml`.

Pour l'installer localement, vous pouvez lancer le docker compose.

```bash
docker compose up -d
```

Une fois le conteneur lancé, on peut passer à la configuration de garage.

Heureusement on doit faire cette étape seulement une fois.

Cette commande va nous simplifier la tâche, afin d'accéder à la cli de garage qui est disponible au sein du conteneur.

```bash
alias garage="docker exec -ti kebaberiie-garage-1 /garage"
```

Désormais on peut passer à la configuration :)

## Configuration

Pour configurer notre noeud garage, on doit d'abord récupérer son id.
```bash
garage status

```
```
==== HEALTHY NODES ====
ID                Hostname       Address         Tags  Zone  Capacity          DataAvail
d7479a2fb3cd2634  yvan-inspiron  127.0.0.1:3901              NO ROLE ASSIGNED
```

Dans notre cas, nous avons le noeud avec l'id `d7479a2fb3cd2634`.

Désormais, pour le rendre opération, il faut lui assigner un rôle, dans le cas de garage, il faut indiquer la zone dans laquelle notre noeud se situe et la capacité de celui-ci.

```bash
garage layout assign -z dc1 -c 2G <ID>
```

L'argument `-z` correspond à la zone de notre serveur et `-c` correspond à la capacité du noeud.

Une fois la commande exécutée, il faut simplement appliquer la layout

```bash
garage layout apply --version 1
```

## Configuration du bucket

Le bucket va être l'endroit dans lequel seront stockés les données de notre site web. 

On commence par créer un bucket.

```bash
garage bucket create kebaberiie
```

Pour pouvoir rendre les données accessibles depuis un lien, on peut faire la commande suivante

```bash
garage bucket website kebaberiie --allow
```

Maintenant, on peut gérer les accès à notre bucket.

On vient créer un token qui va nous permettre de créer et d'accéder aux fichiers de notre bucket `kebaberiie`
```bash
garage key create kebaberiie-key
```

> **Il est important de noter les données retournées par la commande**

```bash
Key name: kebaberiie-key
Key ID: GK9ac645fc4c8efdcab20278c3
Secret key: 8eaede8e9fbb6925c76a9ac44716c953de8c02232a7067a90deacd351195422d
Can create buckets: false
```

Maintenant qu'on les a bien notés, on peut donner les permissions de lecture et d'écriture sur notre bucket `kebaberiie`.

```bash
garage bucket allow --read --write kebaberiie --key kebaberiie-key
```
