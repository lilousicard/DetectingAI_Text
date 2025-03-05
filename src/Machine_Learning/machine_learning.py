import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.ensemble import IsolationForest
from sklearn.mixture import GaussianMixture
from scipy.spatial.distance import cdist
from sklearn.neighbors import NearestNeighbors


def perform_kmeans(data, num_clusters, seed=10, n_init=10, algorithm="lloyd"):
    # Extract vectors for clustering
    x = np.array(list(data.values()))

    # Initialize and fit KMeans
    kmeans = KMeans(n_clusters=num_clusters, random_state=seed, n_init=n_init, algorithm=algorithm)
    kmeans.fit(x)

    # Create a new dictionary to store results with cluster labels
    labeled_data = {key: {'vector': data[key], 'cluster': label} for key, label in zip(data.keys(), kmeans.labels_)}

    return kmeans, labeled_data


def fit_kmeans(kmeans, data):
    # Extract vectors for clustering
    x = np.array(list(data.values()))

    # Predict the cluster labels
    labels = kmeans.predict(x)

    # Create a new dictionary to store results with cluster labels
    labeled_data = {key: {'vector': data[key], 'cluster': label} for key, label in zip(data.keys(), labels)}

    return labeled_data


def perform_hierarchical(data, num_clusters, linkage="ward", compute_full_tree="auto", distance_threshold=None):
    """
    Performs hierarchical (agglomerative) clustering on the given data.

    Parameters:
    - data (dict): A dictionary where keys are identifiers and values are feature vectors.
    - num_clusters (int): The number of clusters to form.
    - linkage (str): The linkage criterion to use ("ward", "complete", "average", "single").
    - compute_full_tree (bool or "auto"): Whether to compute the full tree. "auto" optimizes for speed.
    - distance_threshold (float or None): Threshold for clustering instead of specifying num_clusters.

    Returns:
    - tuple:
        - dict: Mapping of original keys to their vectors and assigned cluster labels.
        - dict: Cluster centroids for assigning new data.
    """

    if not data:
        return {}, {}  # Handle empty input

    # Convert dictionary values into a NumPy array
    keys = list(data.keys())
    x = np.array(list(data.values()))

    # Initialize and fit Agglomerative Clustering
    hierarchical = AgglomerativeClustering(
        n_clusters=num_clusters if distance_threshold is None else None,
        linkage=linkage,
        compute_full_tree=compute_full_tree,
        distance_threshold=distance_threshold
    )
    hierarchical.fit(x)

    # Assign clusters
    cluster_labels = hierarchical.labels_
    labeled_data = {key: {'vector': data[key], 'cluster': label} for key, label in zip(keys, cluster_labels)}

    # Compute cluster centroids dynamically
    unique_clusters = np.unique(cluster_labels)
    centroids = {}
    for cluster_id in unique_clusters:
        cluster_points = np.array([data[key] for key, label in zip(keys, cluster_labels) if label == cluster_id])
        if cluster_points.size > 0:
            centroids[cluster_id] = np.mean(cluster_points, axis=0)  # Compute centroid

    return labeled_data, centroids


def test_hierarchical(new_data, centroids):
    """
    Assigns new data points to the nearest cluster based on the precomputed centroids.

    Parameters:
    - new_data (dict): A dictionary where keys are identifiers and values are feature vectors.
    - centroids (dict): Precomputed centroids from training data.

    Returns:
    - dict: Mapping of original keys to their vectors and assigned cluster labels.
    """

    if not new_data or not centroids:
        return {}  # Handle empty input

    # Convert centroids to an array
    centroid_keys = list(centroids.keys())
    centroid_vectors = np.stack(list(centroids.values()))

    assigned_clusters = {}
    for key, vector in new_data.items():
        vector = np.array(vector).reshape(1, -1)  # Reshape to match dimensions
        distances = cdist(vector, centroid_vectors, metric="euclidean")  # Compute distances
        closest_cluster = centroid_keys[np.argmin(distances)]  # Find nearest centroid

        assigned_clusters[key] = {'vector': vector.flatten().tolist(), 'cluster': closest_cluster}

    return assigned_clusters


def perform_dbscan(data, eps=0.5, min_samples=5):
    # Extract vectors for clustering
    x = np.array(list(data.values()))

    # Initialize and fit DBSCAN
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    dbscan.fit(x)

    # Create a new dictionary to store results with cluster labels
    labeled_data = {key: {'vector': data[key], 'cluster': label} for key, label in zip(data.keys(), dbscan.labels_)}

    return dbscan, labeled_data


def assign_dbscan_clusters(dbscan, data, existing_data):
    # Extract vectors
    x_new = np.array(list(data.values()))
    x_existing = np.array(list(existing_data.values()))  # Data used to train DBSCAN

    # Use nearest neighbors to find the closest DBSCAN-labeled points
    nn = NearestNeighbors(n_neighbors=1).fit(x_existing)
    distances, indices = nn.kneighbors(x_new)

    # Assign cluster labels based on nearest neighbor
    new_labels = [dbscan.labels_[idx[0]] if dist[0] < dbscan.eps else -1 for idx, dist in zip(indices, distances)]

    # Store the new data labels
    labeled_data = {key: {'vector': data[key], 'cluster': label} for key, label in zip(data.keys(), new_labels)}

    return labeled_data


def perform_gmm(data, num_clusters, seed=10, n_init=10):
    # Extract vectors for clustering
    x = np.array(list(data.values()))

    # Initialize and fit Gaussian Mixture Model
    gmm = GaussianMixture(n_components=num_clusters, random_state=seed, n_init=n_init)
    gmm.fit(x)

    # Create a new dictionary to store results with cluster labels
    labeled_data = {key: {'vector': data[key], 'cluster': label} for key, label in zip(data.keys(), gmm.predict(x))}

    return gmm, labeled_data


def fit_gmm(gmm, data):
    # Extract vectors for clustering
    x = np.array(list(data.values()))

    # Predict the cluster labels
    labels = gmm.predict(x)

    # Create a new dictionary to store results with cluster labels
    labeled_data = {key: {'vector': data[key], 'cluster': label} for key, label in zip(data.keys(), labels)}

    return labeled_data


def train_isolation_forest(human_data, seed=10, n_estimators=100, contamination=0.1):
    # Extract vectors for training (only human-written text)
    x_train = np.array(list(human_data.values()))

    # Initialize and fit Isolation Forest
    isolation_forest = IsolationForest(n_estimators=n_estimators, random_state=seed, contamination=contamination)
    isolation_forest.fit(x_train)

    return isolation_forest


def test_isolation_forest(isolation_forest, data):
    # Extract vectors for testing
    x_test = np.array(list(data.values()))

    # Predict anomaly scores (-1 for AI-generated text, 1 for human-written)
    labels = isolation_forest.predict(x_test)

    # Create a dictionary storing the results
    labeled_data = {key: {'vector': data[key], 'is_human': label == 1} for key, label in zip(data.keys(), labels)}

    return labeled_data
