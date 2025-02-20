import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.ensemble import IsolationForest
from sklearn.mixture import GaussianMixture


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


def perform_hierarchical(data, num_clusters):
    # Extract vectors for clustering
    x = np.array(list(data.values()))

    # Initialize and fit Agglomerative Clustering
    hierarchical = AgglomerativeClustering(n_clusters=num_clusters, linkage='ward')
    hierarchical.fit(x)

    # Create a new dictionary to store results with cluster labels
    labeled_data = {key: {'vector': data[key], 'cluster': label} for key, label in
                    zip(data.keys(), hierarchical.labels_)}

    return labeled_data


def run_DBSCAN(data, eps, min_samples):
    # Extract vectors for clustering
    x = np.array(list(data.values()))

    # Initialize and fit DBSCAN
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    dbscan.fit(x)

    # Create a new dictionary to store results with cluster labels
    labeled_data = {key: {'vector': data[key], 'cluster': label} for key, label in zip(data.keys(), dbscan.labels_)}

    return labeled_data


def Gaussian_Mixture_Models(data, num_clusters):
    # Extract vectors for clustering
    x = np.array(list(data.values()))

    # Initialize and fit Gaussian Mixture Models
    gmm = GaussianMixture(n_components=num_clusters)
    gmm.fit(x)

    # Create a new dictionary to store results with cluster labels
    labeled_data = {key: {'vector': data[key], 'cluster': label} for key, label in zip(data.keys(), gmm.predict(x))}

    return labeled_data


def Isolation_Forest(data, num_clusters):
    # Extract vectors for clustering
    x = np.array(list(data.values()))

    # Initialize and fit Isolation Forest
    isolation_forest = IsolationForest(n_estimators=num_clusters)
    isolation_forest.fit(x)

    # Create a new dictionary to store results with cluster labels
    labeled_data = {key: {'vector': data[key], 'cluster': label} for key, label in
                    zip(data.keys(), isolation_forest.predict(x))}

    return labeled_data
