# API Design - Link Up

Ce document décrit le design de l'API du projet Link Up en suivant les principes de l'architecture REST.

## Conception des entités

Pour ce projet nous avons mis en place les entités suivantes :

* `User`
  * Nom d'utilisateur unique
  * Bio ("biographie")
  * Adresse e-mail unique
  * URL de la photo de profil
  * Booléen qui indique si le profil est privé

* `Post`
  * Contenu textuel du post
  * Date de création
  * Date de dernière modification
  * ID de l'auteur

* `Media`
  * URL du média (chemin en local si environnement de développement)
  * Type MIME de média (limité à quelques formats vidéos/images et aussi GIF)
  * ID du post

Chacune de ces entités possède un champ ID. Nous avons opté pour des IDs de type UUID (v4) pour plusieurs raisons :
* Les UUIDs garantissent l'unicité à travers des systèmes distribués et évite les conflits dans un système scalable, sans avoir besoin de coordination centralisée pour la création des IDs.
* Ils sont difficiles à deviner, ce qui ajoute une couche de sécurité.
* Ils permettent de générer des identifiants indépendamment de l'état actuel de la base de données, ce qui est utile pour les opérations asynchrones.

## Relations entre les entités

* Un `User` peut créer plusieurs `Post`.
* Un `Post` appartient à un seul `User`.
* Un `Post` peut contenir plusieurs `Media`.
* Un `Media` appartient à un seul `Post`.

## Opérations sur les entités

Nous utilisons l'architecture REST pour structurer les interactions entre le client et le serveur de manière standardisée.
Chaque resource est identifiée par une URL et les actions sur ces ressources sont définies par les verbes HTTP.

### GET
Le verbe GET est utilisé pour récupérer des données sans modifier l'état de la ressource. Par exemple :
- **GET /users** : Récupère la liste de tous les utilisateurs.
- **GET /users/{user_id}** : Récupère les informations d'un utilisateur spécifique.
- **GET /users/{user_id}/posts** : Récupère tous les posts d'un utilisateur spécifique.
- **GET /posts** : Récupère la liste de tous les posts.
- **GET /posts/{post_id}** : Récupère les informations d'un post spécifique.

### POST
Le verbe POST est utilisé pour créer une nouvelle ressource. Par exemple :
- **POST /users** : Crée un nouvel utilisateur avec les informations fournies.
- **POST /posts** : Crée un nouveau post pour un utilisateur spécifique.

### PATCH
Le verbe PATCH est utilisé pour mettre à jour partiellement une ressource existante. Par exemple :
- **PATCH /users/{user_id}** : Met à jour les informations d'un utilisateur spécifique.
- **PATCH /posts/{post_id}** : Met à jour les informations d'un post spécifique.

### DELETE
Le verbe DELETE est utilisé pour supprimer une ressource existante. Par exemple :
- **DELETE /users/{user_id}** : Supprime un utilisateur spécifique.
- **DELETE /posts/{post_id}** : Supprime un post spécifique.

## Paramètres des requêtes

### Format des paramètres de requête

Les paramètres de requête sont utilisés pour passer des informations supplémentaires à une requête HTTP. Ils peuvent être inclus dans l'URL, dans le corps de la requête ou dans les en-têtes HTTP. Dans notre API, nous utilisons principalement les paramètres suivants :

#### Paramètres d'URL

Les paramètres d'URL sont inclus directement dans l'URL et sont utilisés pour identifier des ressources spécifiques. Par exemple :
- **GET /posts/{post_id}** : Récupère les informations d'un post spécifique en utilisant son `post_id`.
- **PATCH /posts/{post_id}** : Met à jour les informations d'un post spécifique en utilisant son `post_id`.
- **DELETE /posts/{post_id}** : Supprime un post spécifique en utilisant son `post_id`.

#### Paramètres de formulaire

Les paramètres de formulaire sont envoyés dans le corps de la requête et sont utilisés pour créer ou mettre à jour des ressources. Par exemple :
- **POST /posts** : Crée un nouveau post avec le contenu et l'ID de l'utilisateur fournis.
- **PATCH /posts/{post_id}** : Met à jour un post existant avec le nouveau contenu fourni.

### Upload de fichiers

Pour les opérations qui nécessitent l'upload de fichiers, nous utilisons le type `UploadFile` de FastAPI. Les fichiers peuvent être inclus dans la requête en tant que paramètres de formulaire avec le type `File`. Par exemple :
- **POST /posts** : Permet de créer un post et d'uploader des fichiers (images, vidéos, GIFs) associés au post.
- **PATCH /posts/{post_id}** : Permet de mettre à jour un post existant et d'uploader de nouveaux fichiers associés au post.

### Gestion des fichiers

Lorsqu'un fichier est uploadé, nous vérifions le type MIME du fichier pour nous assurer qu'il est pris en charge avant de le sauvegarder en utilisant un fournisseur de stockage.

## Réponses aux requêtes

### Structure des réponses

Les réponses aux requêtes de l'API respectent les conventions REST et utilisent les codes de statut HTTP pour indiquer le résultat de l'opération demandée. Chaque réponse contient également des données structurées en JSON pour fournir des informations détaillées sur la ressource concernée.

#### Codes de statut HTTP

- **200 OK** : La requête a été traitée avec succès et la réponse contient les données demandées.
- **201 Created** : Une nouvelle ressource a été créée avec succès. La réponse contient généralement un lien vers la ressource créée.
- **204 No Content** : La requête a été traitée avec succès, mais il n'y a pas de contenu à renvoyer.
- **400 Bad Request** : La requête est mal formée ou les données fournies sont invalides.
- **404 Not Found** : La ressource demandée n'a pas été trouvée.
- **500 Internal Server Error** : Une erreur interne au serveur s'est produite.

#### Format des données de réponse

Les données de réponse sont renvoyées au format JSON pour une compatibilité et une lisibilité maximales. Par exemple, une réponse pour récupérer un utilisateur pourrait ressembler à ceci :

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "username": "john_doe",
  "email": "john@example.com",
  "bio": "Hello, I'm John!",
  "profile_picture": "http://example.com/images/john.jpg",
  "is_private": false
}
```

Les créations de ressource retournent la ressource fraîchement créée.
