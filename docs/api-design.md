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
