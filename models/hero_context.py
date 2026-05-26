from helpers.inventory import check_bag_weight
from managers import item_manager


class hero_context:
    """Conteneur stable qui lie un héros et sa file d'attente."""
    def __init__(self, initial_hero_obj, item_manager:item_manager):
        from townhall.quest_log import quest_log  # Import local pour éviter les dépendances circulaires
        self.current_hero = initial_hero_obj  # La référence qui va changer souvent
        self.quest_log = quest_log()
        self.next_action_time=0
        self.item_manager = item_manager

    def get_equiped_healing_potions(self):
        hero = self.current_hero
        slots = [
            (hero.utility1_slot, hero.utility1_slot_quantity),
            (hero.utility2_slot, hero.utility2_slot_quantity),
        ]
        potions = []
        for code, qty in slots:
            if not code or qty <= 0:
                continue
            # imhp = self.item_manager.healing_potions
            if code in self.item_manager.healing_potions:
                potions.append({"code":code,"quantity":qty,"restore":self.item_manager.healing_potions[code]})
        return potions
    
    
    def is_ready_for_fight(self):
        hero = self.current_hero
        if check_bag_weight(hero.inventory) == hero.inventory_max_items:
            return False
        current_potions = self.get_equiped_healing_potions()
        if not current_potions:
            return False
        
        return True