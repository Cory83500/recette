document.addEventListener('DOMContentLoaded', function() {
    const ingredientList = document.getElementById('ingredient-list');
    const nomIngredientInput = document.getElementById('nom_ingredient');
    const uniteIngredientInput = document.getElementById('unite');
    const quantiteIngredientInput = document.getElementById('quantite');
    const ingredientsValidesInput = document.getElementById('ingredients_valides');

    document.getElementById('add-ingredient').addEventListener('click', function () {
        const nomIngredient = nomIngredientInput.value;
        const uniteIngredient = uniteIngredientInput.value;
        const quantiteIngredient = quantiteIngredientInput.value;

        if (nomIngredient && uniteIngredient && quantiteIngredient) {
            const ingredientItem = document.createElement('li');
            ingredientItem.textContent = `${nomIngredient} ${quantiteIngredient} ${uniteIngredient}`;
            ingredientList.appendChild(ingredientItem);
            
            nomIngredientInput.value = '';
            uniteIngredientInput.selectedIndex = 0;
            quantiteIngredientInput.value = '';

            mettreAJourChampCache();
        } else {
            alert("Veuillez remplir tous les champs d'ingrédients.");
        }
    });

    function mettreAJourChampCache() {
        const ingredients = Array.from(ingredientList.children).map(function (ingredientItem) {
            return ingredientItem.textContent.trim();
        });
    
        const champCache = ingredientsValidesInput;
        champCache.value = ingredients.join(',');
    
        // Ajoutez uniquement le bouton "Supprimer" à côté de chaque ingrédient dans la liste
        ingredientList.innerHTML = '';
        ingredients.forEach(function (ingredient) {
            const ingredientItem = document.createElement('li');
            ingredientItem.textContent = ingredient;
    
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Supprimer';
            deleteButton.addEventListener('click', function () {
                // Implémentez la logique de suppression de l'ingrédient ici
                ingredientList.removeChild(ingredientItem); // Supprimez l'élément de la liste
                mettreAJourChampCache(); // Mettez à jour le champ caché après la suppression
            });
    
            ingredientItem.appendChild(deleteButton);
            ingredientList.appendChild(ingredientItem);
        });
    }
    
    const ingredients = Array.from(ingredientList.children).map(function (ingredientItem) {
        return ingredientItem.textContent.trim();
    });

    const champCache = ingredientsValidesInput;
    champCache.value = ingredients.join(',');

    // Ajoutez des boutons "Modifier" et "Supprimer" à côté de chaque ingrédient dans la liste
    ingredientList.innerHTML = '';
    ingredients.forEach(function (ingredient) {
        const ingredientItem = document.createElement('li');
        ingredientItem.textContent = ingredient;
        
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Supprimer';
        deleteButton.addEventListener('click', function () {
            // Implémentez la logique de suppression de l'ingrédient ici
            ingredientList.removeChild(ingredientItem); // Supprimez l'élément de la liste
            mettreAJourChampCache(); // Mettez à jour le champ caché après la suppression
        });

        ingredientItem.appendChild(deleteButton);

        ingredientList.appendChild(ingredientItem);
    });
});
