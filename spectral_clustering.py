import pandas as pd
from sklearn.cluster import SpectralClustering
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt

# Charger le fichier user_profiles.csv
user_profiles = pd.read_csv('user_profiles.csv')

# Sample a subset of the data for demonstration
sub_sample = user_profiles.sample(frac=0.3, random_state=42)

# Specify the number of clusters (K) you want to try
K_values = [2, 3, 4, 5]

# Calculate the nearest neighbors graph
nn_graph = NearestNeighbors(n_neighbors=5).fit(sub_sample)
affinity_matrix = nn_graph.kneighbors_graph(sub_sample)

silhouette_scores = []

for k in K_values:
    # Create a spectral clustering object with nearest_neighbors affinity
    spectral = SpectralClustering(n_clusters=k, affinity='nearest_neighbors', n_neighbors=5)

    # Apply clustering to the data
    labels = spectral.fit_predict(sub_sample)

    # Calculate silhouette score
    score = silhouette_score(sub_sample, labels)
    silhouette_scores.append(score)

    # Visualize the clusters (adjust this part based on your data)
    plt.scatter(sub_sample.iloc[:, 0], sub_sample.iloc[:, 1], c=labels, cmap='viridis')
    plt.title(f"Spectral Clustering with {k} clusters")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.show()

# Plot the silhouette scores for different values of K
plt.plot(K_values, silhouette_scores, marker='o')
plt.title("Silhouette Scores for Different K values")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Silhouette Score")
plt.show()
