# Recommendation System

Un système de recommandation des films basé sur le contenu et la collaboration (les interactions et les préférences des utilisateurs pour faire des suggestions personnalisées).

## Instructions pour exécuter le programme :

1. Créez un environnement virtuel (si ce n'est pas déjà fait) :
   
    ```bash
    python3 -m venv myenv  # créez un nouvel environnement virtuel nommé 'myenv'
    ```

2. Activez l'environnement virtuel :

    ```bash
    source myenv/bin/activate  # pour Linux/macOS
    ```

    ou

    ```bash
    .\myenv\Scripts\activate  # pour Windows
    ```

3. Installez les packages requis à partir du fichier requirements.txt :

    ```bash
    pip install -r requirements.txt
    ```

    Cela installera tous les packages Python requis avec les mêmes versions que celles spécifiées dans le fichier requirements.txt.

4. Ce système de recommandation se base sur les données téléchargées à partir de MovieLens. Téléchargez les données à partir du lien suivant et placez les fichiers movies.csv et ratings.csv dans un répertoire nommé data dans le répertoire du programme :
   [MovieLens Dataset](https://grouplens.org/datasets/movielens/25m/)

5. Ensuite, pour nettoyer les données et créer la matrice des profils utilisateurs, exécutez la commande suivante :

    ```bash
    python data_preprocessing.py
    ```

6. À cette étape, le programme affiche un diagramme à barres illustrant le nombre de films par genre :

    ![Nombre de films par genre](/photos/pic1.png)

