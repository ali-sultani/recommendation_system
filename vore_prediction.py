# Ali shoja Sultani sula3002 
import pandas as pd
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.cluster import SpectralClustering
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score

def divide_files():
    # Chargement du fichier ratings1.csv
    ratings = pd.read_csv('ratings1.csv')

    # Séparation des données en train, évaluation et test avec stratification basée sur les notes
    train_data, temp_data = train_test_split(ratings, test_size=0.4, random_state=42, stratify=ratings['rating'])
    eval_data, test_data = train_test_split(temp_data, test_size=0.5, random_state=42, stratify=temp_data['rating'])

    # Enregistrement des fichiers
    train_data.to_csv('ratings_train.csv', index=False)
    eval_data.to_csv('ratings_evaluation.csv', index=False)
    test_data.to_csv('ratings_test.csv', index=False)

# Function to find the 5 nearest neighbors for each user based on their profiles
def find_nearest_neighbors(user_profiles):
    nn_model = NearestNeighbors(n_neighbors=6).fit(user_profiles.drop('userId', axis=1))
    distances, indices = nn_model.kneighbors(user_profiles.drop('userId', axis=1))
    return distances[:, 1:], indices[:, 1:]  

def main():
    #divide_files()

    # Chargement du fichier ratings_train.csv
    ratings_train = pd.read_csv('ratings_train.csv')

    ratings_evaluation = pd.read_csv('ratings_evaluation.csv')
    ratings_test = pd.read_csv('ratings_test.csv')

    # Chargement du fichier user_profiles.csv
    user_profiles = pd.read_csv('user_profiles.csv')

    distances, indices = find_nearest_neighbors(user_profiles)

    print("distances", distances)
    print("indices", indices)

     
   # Construction des caractéristiques et des étiquettes pour l'entraînement et l'évaluation
    train_features = []
    train_labels = []
    eval_features = []
    eval_labels = []

    for idx, neighbors in enumerate(indices):
        # Récupération des profils des 5 utilisateurs les plus proches
        nearest_profiles = user_profiles.iloc[neighbors]

        print("nearest_profiles", nearest_profiles)

    
        # Récupération des votes correspondants
        user_votes = ratings_train[ratings_train['userId'] == idx + 1]['rating'].values
        nearest_votes = ratings_train[ratings_train['userId'].isin(nearest_profiles['userId'])]['rating'].values

        if idx < len(ratings_evaluation):  # Utilisation des données d'évaluation
            eval_features.append(nearest_profiles.drop('userId', axis=1).values)
            eval_labels.append(user_votes)
        else:  # Utilisation des données d'entraînement
            train_features.append(nearest_profiles.drop('userId', axis=1).values)
            train_labels.append(user_votes)

    # Entraînement du modèle d'arbre de décision
    decision_tree = DecisionTreeClassifier()
    decision_tree.fit(train_features, train_labels)

    # Prédiction sur les données d'évaluation
    predictions = decision_tree.predict(eval_features)

    # Évaluation du modèle avec F1-score
    f1 = f1_score(eval_labels, predictions, average='weighted')
    print(f"F1-score: {f1}") 


if __name__ == "__main__":
    main()
