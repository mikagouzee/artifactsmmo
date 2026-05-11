# Utilise une image Python légère
FROM python:3.11-slim

# Définit le dossier de travail dans le container
WORKDIR /app

# Copie le fichier des dépendances (si tu en as un)
# Sinon, on installera les packages manuellement pour l'instant
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout ton code source dans le container
COPY . .

# Commande pour lancer ton bot
CMD ["python", "main.py"]