from flask import Flask, request, render_template
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configurez le répertoire d'upload pour les photos
app.config["UPLOAD_FOLDER"] = "uploads"

# Fonction pour obtenir les informations de la recette depuis la base de données
def obtenir_recette_de_la_base_de_donnees(recette_id):
    conn = sqlite3.connect("ma_base_de_donnees_recettes.db")
    cursor = conn.cursor()

    # Récupérez les données de base de la recette
    cursor.execute("SELECT * FROM recette WHERE id = ?", (recette_id,))
    recette = cursor.fetchone()

    # Récupérez les ingrédients liés à cette recette
    cursor.execute("SELECT nom_ingredient, unite, quantite FROM recette_ingredients WHERE recette_id = ?", (recette_id,))
    ingredients_data = cursor.fetchall()

    ingredients = []

    for ingredient_data in ingredients_data:
        ingredient = {
            'nom': ingredient_data[0],
            'unite': ingredient_data[1],
            'quantite': ingredient_data[2]
        }
        ingredients.append(ingredient)

    # Récupérez le processus de préparation lié à cette recette
    cursor.execute("SELECT process FROM process WHERE recette_id = ?", (recette_id,))
    process_recette = cursor.fetchone()

    conn.close()

    # Créez un dictionnaire pour stocker toutes les données
    recette_data = {
        'nom': recette[1],  # Le nom est en deuxième position (index 1) dans la table recette
        'photo': recette[2],  # La photo est en troisième position (index 2) dans la table recette
        'categorie' : recette[3],
        'ingredients': ingredients,
        'process': process_recette[0] if process_recette else None  # Le processus est dans la première colonne (index 0) de la table process
    }

    return recette_data

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/nouvelle_recette/creation_recette', methods=['GET', 'POST'])
def creation_recette():
    if request.method == 'POST':
        # Créez une connexion à la base de données
        conn = sqlite3.connect("ma_base_de_donnees_recettes.db")
        cursor = conn.cursor()

        # Récupérez le nom de la recette
        nom_recette = request.form['nom_recette']

        # Récupérez catégorie de la recette
        categorie_recette = request.form['categorie']

        # Récupérez la photo téléchargée depuis le formulaire
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo.filename != '':
                nom_photo = secure_filename(photo.filename)
                chemin_photo = os.path.join(app.config['UPLOAD_FOLDER'], nom_photo)
                photo.save(chemin_photo)
            else:
                nom_photo = ""  # Utilisez une chaîne vide comme valeur par défaut si aucune photo n'est téléchargée
        else:
            nom_photo = ""  # Utilisez une chaîne vide comme valeur par défaut si aucune photo n'est téléchargée

        # Récupérez la liste des ingrédients valides depuis le champ caché
        ingredients_valides = request.form['ingredients_valides'].split(',')

        # Insérez la recette dans la table "recette"
        cursor.execute("INSERT INTO recette (nom, photo, categorie) VALUES (?, ?, ?)", (nom_recette, nom_photo, categorie_recette))
        recette_id = cursor.lastrowid

        # Récupérez le champ process_recette depuis le formulaire
        process_recette = request.form['process_recette']

        # Insérez les ingrédients valides dans la table "recette_ingredients"
        for ingredient in ingredients_valides:
            # Séparez l'ingrédient en trois parties : nom, quantité et unité
            parts = ingredient.split()

            # Vérifiez si l'ingrédient contient les trois parties attendues
            if len(parts) == 3:
                nom, quantite, unite = parts
                cursor.execute("INSERT INTO recette_ingredients (recette_id, nom_ingredient, unite, quantite) VALUES (?, ?, ?, ?)",
                            (recette_id, nom, unite, quantite))
            else:
                # Gérez le cas où l'ingrédient ne contient pas les trois parties attendues
                # Vous pouvez choisir de le ignorer ou de le gérer d'une autre manière
                print(f"Ignoré : {ingredient}")

        # Insérez le processus dans la table "process"
        cursor.execute("INSERT INTO process (recette_id, process) VALUES (?, ?)", (recette_id, process_recette))

        # Committez les modifications à la base de données et fermez la connexion
        conn.commit()
        conn.close()

        # Obtenez à nouveau les données de la recette depuis la base de données
        recette = obtenir_recette_de_la_base_de_donnees(recette_id)

        # Renvoyez la page "recette_template.html" avec les données de la recette
        return render_template('recette_template.html', recette=recette)

    elif request.method == 'GET':
        # Renvoyer la page "form_recette.html" lorsque la requête est de type GET
        return render_template('form_recette.html')

    if request.method == 'POST':
        # Créez une connexion à la base de données
        conn = sqlite3.connect("ma_base_de_donnees_recettes.db")
        cursor = conn.cursor()

        # Récupérez le nom de la recette
        nom_recette = request.form['nom_recette']

        # Récupérez catégorie de la recette
        categorie_recette = request.form['categorie']

        # Récupérez la photo téléchargée depuis le formulaire
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo.filename != '':
                nom_photo = secure_filename(photo.filename)
                chemin_photo = os.path.join(app.config['UPLOAD_FOLDER'], nom_photo)
                photo.save(chemin_photo)
            else:
                nom_photo = ""  # Utilisez une chaîne vide comme valeur par défaut si aucune photo n'est téléchargée
        else:
            nom_photo = ""  # Utilisez une chaîne vide comme valeur par défaut si aucune photo n'est téléchargée

       # Récupérez la liste des ingrédients valides depuis le champ caché
        ingredients_valides = request.form['ingredients_valides'].split(',')

        # Insérez la recette dans la table "recette"
        cursor.execute("INSERT INTO recette (nom, photo, categorie) VALUES (?, ?, ?)", (nom_recette, nom_photo, categorie_recette))
        recette_id = cursor.lastrowid

        # Récupérez le champ process_recette depuis le formulaire
        process_recette = request.form['process_recette']

        # Insérez les ingrédients valides dans la table "recette_ingredients"
        for ingredient in ingredients_valides:
            nom, quantite, unite = ingredient.split()
            cursor.execute("INSERT INTO recette_ingredients (recette_id, nom_ingredient, unite, quantite) VALUES (?, ?, ?, ?)",
                        (recette_id, nom, unite, quantite))
       # Insérez le processus dans la table "process"
        cursor.execute("INSERT INTO process (recette_id, process) VALUES (?, ?)", (recette_id, process_recette))

        # Committez les modifications à la base de données et fermez la connexion
        conn.commit()
        conn.close()

        # Obtenez à nouveau les données de la recette depuis la base de données
        recette = obtenir_recette_de_la_base_de_donnees(recette_id)

        # Renvoyez la page "recette_template.html" avec les données de la recette
        return render_template('recette_template.html', recette=recette)

    elif request.method == 'GET':
        # Renvoyer la page "form_recette.html" lorsque la requête est de type GET
        return render_template('form_recette.html')
    
@app.route('/recettes', methods=['GET', 'POST'])
def liste_recettes():
    conn = sqlite3.connect("ma_base_de_donnees_recettes.db")
    cursor = conn.cursor()

    # Récupérez toutes les catégories distinctes depuis la base de données
    cursor.execute("SELECT DISTINCT categorie FROM recette")
    categories = [row[0] for row in cursor.fetchall()]

    # Récupérez la catégorie sélectionnée depuis le formulaire
    selected_category = request.args.get('categorie')

    # Construisez la requête SQL pour récupérer les recettes en fonction de la catégorie sélectionnée
    if selected_category:
        cursor.execute("SELECT id, nom, photo FROM recette WHERE categorie = ?", (selected_category,))
    else:
        cursor.execute("SELECT id, nom, photo FROM recette")

    recettes = [{'id': row[0], 'nom': row[1], 'photo': row[2]} for row in cursor.fetchall()]

    conn.close()

    return render_template('liste_recettes.html', categories=categories, recettes=recettes)



@app.route('/recette/<int:recette_id>')
def afficher_recette(recette_id):
    recette = obtenir_recette_de_la_base_de_donnees(recette_id)
    return render_template('recette_template.html', recette=recette)


if __name__ == '__main__':
    app.run(debug=True)