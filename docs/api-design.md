# API Design - Link Up

Ce document décrit le design de l'API du projet Link Up en suivant les principes de l'architecture REST.

## Conception des entités

Pour ce projet nous avons mis en place les entités suviantes :

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
