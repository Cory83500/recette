import sqlite3

# Créez une connexion à la base de données (elle sera créée si elle n'existe pas)
conn = sqlite3.connect("ma_base_de_donnees_recettes.db")  # Remplacez "ma_base_de_donnees_recettes.db" par le nom que vous souhaitez utiliser
cursor = conn.cursor()

# Créez la table "recette"
cursor.execute("""
    CREATE TABLE IF NOT EXISTS recette (
        id INTEGER PRIMARY KEY,
        nom TEXT,
        photo BLOB,
        categorie TEXT
    )
""")

# Créez la table de liaison "recette_ingredients"
cursor.execute("""
    CREATE TABLE IF NOT EXISTS recette_ingredients (
        recette_id INTEGER,
        nom_ingredient TEXT,
        unite TEXT,
        quantite REAL,
        FOREIGN KEY (recette_id) REFERENCES recette (id)
    )
""")

# Créez la table "process"
cursor.execute("""
    CREATE TABLE IF NOT EXISTS process (
        recette_id INTEGER,
        process TEXT,
        FOREIGN KEY (recette_id) REFERENCES recette (id)
    )
""")

# Committez les modifications à la base de données
conn.commit()

# Fermez la connexion à la base de données
conn.close()

print("Base de données initialisée avec succès.")
