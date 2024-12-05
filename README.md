# Link Up 🙌

> [!NOTE]
> Le projet Link Up est développé dans le cadre du module 4DESA et sert de projet d'évaluation.

Link Up est une plateforme de réseaux sociaux qui vise à être un système backend évolutif et efficace pouvant être intégré à n'importe quelle interface frontend, offrant une expérience de gestion de contenu transparente.

## Fonctionnalités

* Gestion des utilisateurs
* Gestion des posts
  * Possibilité d'ajouter des médias (images, GIFs et vidéos)

## Installation locale

Pour développer le projet en local, suivre les étapes suivantes :

1. Cloner le repo Git :

```bash
git clone https://github.com/matheodrd/linkup.git
cd linkup
```

2. Créer et activer un environnement virtuel Python :

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

3. Installer les dépendances :

```bash
pip3.12 install -r requirements.txt
```

4. Démarrer l'application :
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

## Reference API

### Endpoints

#### Utilisateurs

| Méthode | Endpoint        | Description                           |
|---------|-----------------|---------------------------------------|
| GET     | /users          | Récupérer tous les utilisateurs       |
| POST    | /users          | Créer un nouvel utilisateur           |
| GET     | /users/{user_id}| Récupérer les informations d'un utilisateur spécifique |
| PATCH   | /users/{user_id}| Mettre à jour les informations d'un utilisateur spécifique |
| DELETE  | /users/{user_id}| Supprimer un utilisateur spécifique   |
| GET     | /users/{user_id}/posts | Récupérer tous les posts d'un utilisateur spécifique |

##### Paramètres

| Méthode | Endpoint        | Paramètre | Type   | Obligatoire | Description                |
|---------|-----------------|-----------|--------|-------------|----------------------------|
| GET     | /users/{user_id}| user_id   | string | Oui         | Id de l'utilisateur        |
| PATCH   | /users/{user_id}| user_id   | string | Oui         | Id de l'utilisateur        |
| DELETE  | /users/{user_id}| user_id   | string | Oui         | Id de l'utilisateur        |
| GET     | /users/{user_id}/posts | user_id | string | Oui | Id de l'utilisateur |

#### Posts

| Méthode | Endpoint        | Description                           |
|---------|-----------------|---------------------------------------|
| GET     | /posts          | Récupérer tous les posts              |
| POST    | /posts          | Créer un nouveau post                 |
| GET     | /posts/{post_id}| Récupérer les informations d'un post spécifique |
| PATCH   | /posts/{post_id}| Mettre à jour les informations d'un post spécifique |
| DELETE  | /posts/{post_id}| Supprimer un post spécifique          |

##### Paramètres

| Méthode | Endpoint        | Paramètre | Type   | Obligatoire | Description                |
|---------|-----------------|-----------|--------|-------------|----------------------------|
| GET     | /posts/{post_id}| post_id   | string | Oui         | Id du post                 |
| PATCH   | /posts/{post_id}| post_id   | string | Oui         | Id du post                 |
| DELETE  | /posts/{post_id}| post_id   | string | Oui         | Id du post                 |

### Définition des Schémas

#### UserPublic

| Propriété        | Type        | Obligatoire | Description                    |
|------------------|-------------|-------------|--------------------------------|
| email            | string      | Oui         | Email de l'utilisateur         |
| username         | string      | Oui         | Nom d'utilisateur (3-50 caractères) |
| bio              | string      | Non         | Biographie (par défaut: "Hello!, I'm new here") |
| profile_picture  | string/null | Non         | Image de profil                |
| is_private       | boolean     | Non         | Privé (par défaut: false)      |
| id               | string      | Oui         | Id de l'utilisateur (UUID)     |

#### UserCreate

| Propriété        | Type    | Obligatoire | Description                    |
|------------------|---------|-------------|--------------------------------|
| email            | string  | Oui         | Email de l'utilisateur         |
| username         | string  | Oui         | Nom d'utilisateur (3-50 caractères) |

#### UserUpdate

| Propriété        | Type       | Obligatoire | Description                    |
|------------------|------------|-------------|--------------------------------|
| email            | string/null| Non         | Email de l'utilisateur         |
| username         | string/null| Non         | Nom d'utilisateur (3-50 caractères) |
| bio              | string/null| Non         | Biographie                     |
| profile_picture  | string/null| Non         | Image de profil                |
| is_private       | boolean/null | Non       | Privé                          |

#### PostPublic

| Propriété        | Type    | Obligatoire | Description                    |
|------------------|---------|-------------|--------------------------------|
| content          | string  | Oui         | Contenu du post (max 2200 caractères) |
| created_at       | string  | Oui         | Date de création (format date-heure) |
| updated_at       | string/null | Non     | Date de mise à jour (format date-heure) |
| id               | string  | Oui         | Id du post (UUID)              |
| user_id          | string  | Oui         | Id de l'utilisateur (UUID)     |
| medias           | array   | Oui         | Liste de médias (MediaPublic)  |

#### Création d'un post

| Propriété        | Type    | Obligatoire | Description                    |
|------------------|---------|-------------|--------------------------------|
| content          | string  | Oui         | Contenu du post                |
| user_id          | string  | Oui         | Id de l'utilisateur (UUID)     |
| files            | array/null | Non      | Liste de fichiers (type binaire) |

#### Mise à jour d'un post

| Propriété        | Type    | Obligatoire | Description                    |
|------------------|---------|-------------|--------------------------------|
| content          | string/null | Non     | Contenu du post                |
| files            | array/null | Non      | Liste de fichiers (type binaire) |

#### MediaPublic

| Propriété        | Type    | Obligatoire | Description                    |
|------------------|---------|-------------|--------------------------------|
| media_url        | string  | Oui         | URL du média                   |
| media_type       | string  | Oui         | Type MIME de média             |
| id               | string  | Oui         | Id du média (UUID)             |
| post_id          | string  | Oui         | Id du post (UUID)              |