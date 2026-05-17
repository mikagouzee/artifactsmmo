class quest_log:
    def __init__(self):
        # La liste qui stocke les tâches. L'index 0 est toujours la tâche active.
        self.queue = []

    def push_next(self, quest):
        """Ajoute une tâche prioritaire au tout début (interruption)."""
        self.queue.insert(0, quest)

    def append_back(self, quest):
        """Ajoute une tâche en fin de file (comme la tâche Default)."""
        self.queue.append(quest)

    def get_current_quest(self):
        """Récupère la tâche en cours d'exécution, ou None si vide."""
        if self.queue:
            return self.queue[0]
        return None

    def pop_current(self):
        """Supprime la tâche actuelle une fois qu'elle est terminée ou failed."""
        if self.queue:
            return self.queue.pop(0)
        return None

    @property
    def is_empty(self) -> bool:
        return len(self.queue) == 0