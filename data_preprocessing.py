import pandas as pd
import matplotlib.pyplot as plt

# Fonctions de prétraitement des données

def load_data(movies_path, ratings_path):
    """
    Charge les données des films et des notes.

    Args:
        movies_path (str): Chemin vers le fichier CSV des films.
        ratings_path (str): Chemin vers le fichier CSV des notes.

    Returns:
        pandas.DataFrame: DataFrame des films.
        pandas.DataFrame: DataFrame des notes.
    """

    movies = pd.read_csv(movies_path)
    ratings = pd.read_csv(ratings_path)

    return movies, ratings

def clean_data(movies, ratings):
    """
    Nettoie les données des films et des notes.

    Args:
        movies (pandas.DataFrame): DataFrame des films.
        ratings (pandas.DataFrame): DataFrame des notes.

    Returns:
        pandas.DataFrame: DataFrame des films nettoyés.
        pandas.DataFrame: DataFrame des notes nettoyées.
    """

    # Supprimer les films sans genre
    movies = movies[movies['genres'] != '(no genres listed)']
    # Enregistrer le nouveau fichier movies1.csv
    movies.to_csv('./data/movies1.csv', index=False)

    # Split genres and count the number of movies per genre
    genre_count = movies['genres'].str.split('|', expand=True).stack().value_counts()

    # Plot a bar chart
    plt.figure(figsize=(10, 6))
    genre_count.plot(kind='bar')
    plt.title('Number of Movies by Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Filtrer les ratings de valeurs 5.5, 4.5, 3.5, 2.5, 1.5, 0.5 et les changer selon les spécifications
    ratings['rating'] = ratings['rating'].replace({5.5: 5, 4.5: 4, 3.5: 3, 2.5: 2, 1.5: 1, 0.5: 1})
    
    # Enregistrer le nouveau fichier ratings1.csv
    ratings.to_csv('./data/ratings1.csv', index=False)

    return movies, ratings

def create_content_matrix(movies):
    # Filtrer les films sans genre
    movies_filtered = movies[movies['genres'] != '(no genres listed)']

    # Créer une colonne pour chaque genre
    genres = set(g for sublist in movies_filtered['genres'].str.split('|') for g in sublist)
    for genre in genres:
        movies_filtered[genre] = movies_filtered['genres'].str.contains(genre).astype(int)

    # Sélectionner seulement les colonnes de genre et movieId
    movie_genres = movies_filtered[['movieId'] + list(genres)]

    # Définir movieId comme l'index et supprimer la colonne movieId
    movie_genres.set_index('movieId', inplace=True)

    # Affichage de la matrice binaire de contenu
    print(movie_genres)
    return movie_genres

def create_profile_matrix(ratings, content_matrix):
    # Suppression de la colonne 'timestamp'
    ratings.drop('timestamp', axis=1, inplace=True)

    # Fusion des données de ratings avec la matrice binaire de contenu
    merged_data = pd.merge(ratings, content_matrix, on='movieId')

    # Calcul de la matrice de profil des utilisateurs P
    # Groupement par userId et somme pondérée des vecteurs binaires de film par le rating
    user_profiles = merged_data.groupby('userId').apply(lambda x: x.iloc[:, 3:].mul(x['rating'], axis=0).sum())

    # Réinitialisation de l'index pour rétablir 'userId' comme une colonne
    user_profiles = user_profiles.reset_index()

    # Affichage de la matrice de profil des utilisateurs P
    print(user_profiles)

    #Exporter la matrice de profiles utilisateurs dans un fichier csv
    user_profiles.to_csv('./data/user_profiles.csv', index=False)

# Exécution des fonctions
movies, ratings = load_data('./data/movies.csv', './data/ratings.csv')
movies, ratings = clean_data(movies, ratings)
content_matrix = create_content_matrix(movies)
profile_matrix = create_profile_matrix(ratings, content_matrix)
