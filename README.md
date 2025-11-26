# Flask + SQLAlchemy Exercise

Ce dépôt est un gabarit pour un exercice Flask / SQLAlchemy — application minimale avec modèles `User` et `Post` et routes CRUD basiques.

## Installation

1. Créez un environnement virtuel (optionnel) et installez les dépendances:

```
python -m venv venv
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

2. Lancer l'application (développement):

```
python app.py
```

L'application écoute par défaut sur `http://127.0.0.1:5000`.

## Endpoints API

Les routes principales exposées par l'application sont :

- `GET /users` — lister tous les utilisateurs (renvoie une liste JSON)
- `POST /adduser` — créer un nouvel utilisateur (envoyer JSON)
- `GET /posts` — lister tous les posts (inclut le `username` de l'auteur)
- `POST /addpost` — créer un post lié à un utilisateur existant (valide `user_id`)
- `GET /verify` — rapport détaillé des relations users/posts (diagnostic)

### Ajouter un utilisateur (Add user)

Utilisez `POST /users` pour créer un utilisateur avec JSON. Exemple :

```
curl -X POST http://127.0.0.1:5000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "nouvel_util", "email": "nouvel@example.com"}'
```

Réponse attendue (201 Created):

```json
{
  "id": 10,
  "username": "nouvel_util",
  "email": "nouvel@example.com"
}
```

### Ajouter un post (Add post)

Utilisez `POST /posts` pour créer un post lié à un `user_id` existant. Exemple :

```
curl -X POST http://127.0.0.1:5000/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "Mon titre", "content": "Le contenu", "user_id": 1}'
```

Réponse attendue (201 Created):

```json
{
  "id": 5,
  "title": "Mon titre",
  "content": "Le contenu",
  "user_id": 1,
  "username": "alice"
}
```

Si `user_id` ne référence pas un utilisateur existant, l'API retourne `400` avec un message d'erreur.

## Tests

Les tests sont fournis dans le dossier `tests/`. Pour exécuter les tests unitaires :

```
python -m pytest tests/ -v
```

Tous les tests devraient passer (`12 passed`).

## Remarques

- Pendant le développement, l'application peut pré-remplir des données d'exemple. Lors des tests, l'initialisation automatique est désactivée pour garantir un état propre.
- Les routes CRUD exposées sont minimalistes et renvoient du JSON pour faciliter les tests.

Si vous souhaitez que j'ajoute des exemples HTML de formulaires `adduser` / `addpost`, dites-le et je peux les ajouter.
