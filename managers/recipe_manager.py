import json
import os

class RecipeManager:
    def __init__(self, recipes_path="data/recipes.json"):
        self.recipes_path = recipes_path
        self.recipes = {}
        self.load_recipes()

    def load_recipes(self):
        """Charge le cache local des recettes."""
        if os.path.exists(self.recipes_path):
            with open(self.recipes_path, 'r') as f:
                self.recipes = json.load(f)
        else:
            print(f"⚠️ {self.recipes_path} non trouvé. Le manager est vide.")

    def get_recipes_for_skill(self, skill_name):
        """Retourne toutes les recettes d'un métier (ex: 'gearcrafting')."""
        return self.recipes.get(skill_name, [])

    def get_best_recipe(self, skill_name, current_level):
        """
        Trouve la recette la plus haut niveau accessible pour le perso.
        """
        available = [
            r for r in self.get_recipes_for_skill(skill_name) 
            if r['level'] <= current_level
        ]
        
        if not available:
            return None
            
        # On trie par niveau décroissant pour avoir le 'meilleur' en premier
        return sorted(available, key=lambda x: x['level'], reverse=True)[0]

    def get_recipe_details(self, item_code):
        """Retrouve une recette spécifique par le code de l'item."""
        for skill in self.recipes:
            for recipe in self.recipes[skill]:
                if recipe['code'] == item_code:
                    return recipe
        return None