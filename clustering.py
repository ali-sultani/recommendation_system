import pandas as pd
from sklearn.cluster import SpectralClustering
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors
import numpy as np

# Charger le fichier user_profiles.csv
user_profiles = pd.read_csv('user_profiles.csv')

# Sample a subset of the data for demonstration
sub_sample = user_profiles.sample(frac=0.3, random_state=42)

# Calculate the nearest neighbors graph for the sub-sample
nn_graph = NearestNeighbors(n_neighbors=5).fit(sub_sample)
affinity_matrix = nn_graph.kneighbors_graph(sub_sample)

# Create a spectral clustering object with K=2 for the initial 30% of data
spectral = SpectralClustering(n_clusters=2, affinity='nearest_neighbors', n_neighbors=5)
labels_30 = spectral.fit_predict(sub_sample)

# Create a DataFrame with 'userId' and 'cluster' columns
cluster_labels = pd.DataFrame({'userId': sub_sample['userId'], 'cluster': labels_30})

# Merge the cluster labels with the user_profiles DataFrame based on 'userId'
user_profiles = pd.merge(user_profiles, cluster_labels, on='userId', how='left')


print(user_profiles)


# Calculate the centers of the clusters identified with K=2
cluster_centers = []
for label in range(2):
    cluster_centers.append(np.mean(sub_sample[labels_30 == label].iloc[:, 1:], axis=0))  # Exclude userId column

# Assign the remaining 70% of the data to the closest cluster center
remaining_70 = user_profiles.drop(sub_sample.index)
labels_remaining = []

for index, row in remaining_70.iterrows():
    distances = [np.linalg.norm(row[1:] - center) for center in cluster_centers]  # Exclude userId column
    closest_cluster = np.argmin(distances)
    labels_remaining.append(closest_cluster)

cluster_labels = pd.DataFrame({'userId': remaining_70['userId'], 'cluster': labels_remaining})

user_profiles = pd.merge(user_profiles, cluster_labels, on='userId', how='left')

# Write the result to a CSV file
user_profiles.to_csv('clustering_user_profiles.csv', index=False)