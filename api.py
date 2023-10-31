import requests
from googletrans import Translator
import sqlite3

# URL de l'API TheMealDB en français pour obtenir la liste des ingrédients
url = "https://www.themealdb.com/api/json/v1/1/list.php?i=list"

# Effectuez la requête GET
response = requests.get(url)

# Vérifiez si la requête a réussi (code 200)
if response.status_code == 200:
    data = response.json()  # Convertissez la réponse JSON en un dictionnaire Python
    # La clé "meals" contient la liste des ingrédients
    ingredients = data.get("meals", [])
    
    # Créez une instance du traducteur
    translator = Translator()
    
    # Créez une connexion à la base de données SQLite
    conn = sqlite3.connect("ma_base_de_donnees_recettes.db")  # Assurez-vous que le nom de la base de données est correct
    cursor = conn.cursor()
    
    for index, ingredient in enumerate(ingredients, start=1):
        nom_ingredient_en = ingredient.get("strIngredient", "")
        
        try:
            # Essayez de traduire le nom de l'ingrédient de l'anglais au français
            traduction = translator.translate(nom_ingredient_en, dest='fr')
            nom_ingredient_fr = traduction.text
        except Exception as e:
            nom_ingredient_fr = nom_ingredient_en
        
        # Insérez les ingrédients dans la table "ingredient"
        cursor.execute("INSERT INTO ingredient (nom, unité, type) VALUES (?, ?, ?)",
                       (nom_ingredient_fr, '', ''))  # Vous pouvez ajouter les unités et types appropriés
        
        print(f"{index}. {nom_ingredient_fr} inséré dans la base de données.")
    
    # Committez les modifications à la base de données
    conn.commit()
    
    # Fermez la connexion à la base de données
    conn.close()
else:
    print(f"La requête a échoué avec le code d'état {response.status_code}")
