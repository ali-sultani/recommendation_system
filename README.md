# Recommendation System

Un système de recommandation des films basé sur le contenu et la collaboration (les interactions et les préférences des utilisateurs pour faire des suggestions personnalisées). 

Le programme utilise un jeu de données extraits de MovieLens, un service de recommendation de films. Le programme fait usage de 2 fichiers movies.csv (un tableau des films. chaque film possède un id, un titre et un ensemble de genres) et ratings.csv (un fichier contenant les évaluations des utilisateurs pour chacun des films.).

## Instructions pour démarrer le programme :

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

4. Ce système de recommandation se base sur les données téléchargées à partir de MovieLens. Téléchargez les données à partir du lien suivant et placez les fichiers movies.csv et ratings.csv dans un répertoire nommé **data** dans le répertoire racine du programme :
   [MovieLens Dataset](https://grouplens.org/datasets/movielens/25m/)

5. Ensuite, la première étape du programme consiste à nettroyer les données. Ce processus consiste à enlever les films n'ayant pas de genre (genre non listé). 

    On crée aussi la matrice des profils utilisateurs qui est une combinaison linéaire de l'historique de ses votes.

    ![Nombre de films par genre](/photos/user_profils.png)

    Exécutez la commande suivante :

    ```bash
    python data_preprocessing.py
    ```
    Les profils utilisateurs sont stockés dans un fichier nommé **user_profiles.csv.**
    
    À cette étape, le programme affiche aussi un diagrame en bâton illustrant le nombre de films que l’on a par genre :

    ![Nombre de films par genre](/photos/pic1.png)

6. Ensuite, dans le but d'optimiser la recherche d'items et d'utilisateurs, on aimerait trouver les groupes d'utilisateurs et d'items présentant les mêmes caractéristiques. 

    La méthode de regroupement spectral a été utilisé ici. pour trouver la valeur du k(nombre de groupe) présentant le score de silhoutte le plus élévé. Voici les différents nuages de points pour chacune des valeurs de k testé : 

    ![k=2](/photos/spectral_clustering_k2.png)
    ![k=3](/photos/spectral_clustering_k3.png)
    ![k=4](/photos/spectral_clustering_k4.png)
    ![k=5](/photos/spectral_clustering_k5.png)

    Voici le graphique illustrant le score de silhouette pour chacune des valeurs de k :

    ![silhouette score graphique](/photos/silhouette_score_graphique.png)

    On voit que k=2 a le meilleur score de silhoutte. 
    
    Pour exécuter cette partie du programme, faites la commande suivante : 

    ```bash
    python spectral_clustering.py
    ```
7. Maintenant que nous avons décidé de diviser les profils dans 2 clusters étant donnée que k=2 a le score de silhoutte le plus élévé, il s'agit ici simplement d'effectuer le spectral clustering et de placer les profils utilisateurs dans le cluster approprié en utilisant leur distance par rapport au centre du cluster. Pour ce faire, exécuter la commande suivante :
    ```bash
    python clustering.py
    ```
8. Dans cette étape, on veut construire une fonction de classificaiton D() qui est capable de prédire le vote d'un utilisateur U sur un film I en prenant en entrée les votes eds cinq utilisateurs qui sont le lui sont le plus proche. 

    Pour ce faire, On prends le votes du fichier ratings1.csv et on le subdiviser en trois fichiers distincts, ratings_train.csv, ratings_evaluation.csv et ratings_test.csv.
    
    Le fichier ratings_train.csv contient 60% des données de ratings1.csv tandis que ratings_evaluation.csv et ratings_test.csv contiennent chacun 20% des données.

    exécuter la commande suivante :
    ```bash
    python vote_prediction.py
    ```    

    Noter que cette partie peut prendre beaucoup du temps à rouler car le volume des données est énorme.