# Guide de déploiement sur Azure

## Azure Container Registry

* Permet de stocker l'image de l'application Linkup

```bash
az acr create --resource-group linkup-rg --name linkupacr --sku Basic --location francecentral
```

## Azure Service Plan

* Nécessaire pour la création de l'App Service

```bash
az appservice plan create --name linkup-asp --resource-group linkup-rg --sku B1 --is-linux --location francecentral
```

## App Service

* Permet d'héberger l'API Link Up

```bash
az webapp create --resource-group linkup-rg --plan linkup-asp --name linkup-web-svc
```

## Virtual Network

* Permet une connectivité privée entre les services

```bash
az network vnet create --resource-group linkup-rg --name linkup-vnet --location francecentral \
    --address-prefix 10.0.0.0/16 --subnet-name default --subnet-prefix 10.0.0.0/24
```

## Flexible PostgreSQL Server

* Base de données utilisée pour Link Up

```bash
az postgres flexible-server create --resource-group linkup-rg --name linkup-database \
    --location francecentral --vnet linkup-vnet --subnet default --sku-name Standard_B1ms \
    --storage-size 32 --admin-user <ADMIN_USERNAME> --admin-password <PASSWORD>
```

## Azure Key Vault

* Utilisé pour gérer les secrets, tels que les mots de passe et les chaînes de connexion.

```bash
az keyvault create --resource-group linkup-rg --name linkup-keyvault-1 --location francecentral
```

## Storage Account

* Utilisé pour créer un container de stockage Blob

```bash
az storage account create --name linkupsa --resource-group linkup-rg --location francecentral --sku Standard_LRS --kind StorageV2
```

## Configuration

1. Push l'image linkup sur Azure ACR
2. Créer les secrets dans le Key Vault :
   * DatabaseUrl : Url de connexion à la BDD postgres contenant le mot de passe et le username
   * ConnectionStringSA : Connexion String du container blob utilisé pour les médias
3. Ajouter les variables d'environnement dans l'App Service:
   * Ajouter les secrets du vault en utilisant la syntaxe de référence
