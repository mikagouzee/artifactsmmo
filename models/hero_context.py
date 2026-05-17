
class hero_context:
    """Conteneur stable qui lie un héros et sa file d'attente."""
    def __init__(self, initial_hero_obj):
        from townhall.quest_log import quest_log  # Import local pour éviter les dépendances circulaires
        self.current_hero = initial_hero_obj  # La référence qui va changer souvent
        self.quest_log = quest_log()