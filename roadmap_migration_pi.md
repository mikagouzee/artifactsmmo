# Roadmap Technique : Migration & Déploiement Artifacts MMO

Ce document récapitule la stratégie de déploiement et d'évolution de l'infrastructure vers une architecture robuste sur Raspberry Pi avec persistence MongoDB.


## 1. Architecture de Contrôle (Workers)
Évolution du `ActionController` vers un modèle multi-instances.
- **Centralisation du Cooldown** : Utilisation d'un lock distribué (ou simple vérification en base) pour s'assurer qu'un perso ne tente pas une action avant la fin de son cooldown global.
- **Logs & Monitoring** : Conservation du `_request_wrapper` pour suivre la consommation réelle du quota face au whitelist IP.


## 2. Persistence MongoDB
Remplacer le chargement mémoire systématique par une base de données pour économiser le quota API.
- **Schéma WorldMap** : Stockage des données de `get_all_maps`.
    - Un script de synchronisation hebdomadaire ou manuel pour mettre à jour la collection.
- **Suivi des Héros & Stocks** :
    - Sauvegarde de l'état de l'inventaire et des niveaux pour permettre une reprise après crash sans appels API de vérification.
    - Centralisation des données de banque.


## 3. Sécurisation & Environnement
L'objectif est d'isoler les secrets et de préparer l'environnement de production.
- **Gestion des Secrets** : Déplacer l'API Token et les identifiants de base de données dans un fichier `.env` (exclu de Git) ou utiliser les GitHub Secrets.
- **Configuration Docker** : Création d'un `docker-compose.yml` incluant :
    - Le service `bot-artifacts` (Python 3.11+).
    - Le service `mongodb` (image officielle compatible ARM pour la Raspberry).

## 4. Déploiement Continu (CI/CD)
Automatisation de la mise à jour du code sur la Raspberry Pi.
- **GitHub Actions** : Configuration d'un workflow `.github/workflows/deploy.yml`.
- **Méthode de Déploiement** : Utilisation de `SSH` pour pull le code sur la Pi et relancer les containers :
    ```bash
    docker-compose up -d --build
    ```

## 5. Maintenance Raspberry Pi
Optimisations spécifiques pour le matériel :
- **Optimisation des écritures** : Configurer MongoDB avec `storage.wiredTiger.engineConfig.journal.enabled: false` ou utiliser un montage RAM pour les logs si nécessaire afin de préserver la carte SD.
- **Auto-restart** : Configuration de Docker pour redémarrer les services automatiquement après une coupure de courant.
