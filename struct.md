project_root/
│
├── main.py                 # Point d'entrée, initialise le client HTTP et les workers
├── data/
│   ├── recipes.json        # Cache local des recettes (chargé par RecipeManager)
│   └── shared_needs.json   # Fichier de communication pour la "Task List"
│
├── models/                 # Dataclasses
│   ├── hero.py
│   ├── item.py             # Inclut la structure de la recette
│   └── world_map.py
│
├── controllers/            # Interaction API pure
│   └── action_controller.py
│
├── core/                   # Logique métier et cerveau
│   ├── recipe_manager.py   # Charge le JSON, cherche la meilleure recette par level
│   ├── bank_manager.py     # Gère l'inventaire de la banque, calcule les retraits
│   └── task_board.py       # Lit/Ecrit les besoins en ressources pour les autres
│
├── routines/               # Fonctions asynchrones réutilisables (Composants)
│   ├── go_fight.py
│   ├── go_gather.py
│   ├── go_craft.py         # Mis à jour pour accepter une recette dynamique
│   └── go_bank_logic.py    # Gère le cycle (déposer tout / retirer ingrédients)
│
└── workers/                # Les boucles infinies par personnage
    ├── farm_chickens.py    # Combattant
    ├── farm_gatherer.py    # Récolteur (lit le TaskBoard)
    └── master_crafter.py   # Le nouveau worker qui planifie et craft