import numpy as np
import pandas as pd

def initial_centroids(X,number_cluster):
    centroid_indexes=np.random.choice(range(len(X)),number_cluster,replace=False)
    centroids=X[centroid_indexes]
    return np.array(centroids)
    
def calc_distance(X1, X2):
    return sum(np.abs(X1 - X2))
               
def assign_clusters(X, centroids):
    clusters = []
    for i in range(len(X)):
        distances = []
        for centroid in centroids:
            distances.append(calc_distance(centroid,X[i,:]))
        cluster = distances.index(min(distances))
        clusters.append(cluster)
    return np.array(clusters)

def calc_centroids(X,clusters):
    new_centroids = []
    for c in set(clusters):
        current_cluster = X[clusters==c]
        cluster_median = np.median(current_cluster, axis=0)
        new_centroids.append(cluster_median)
    return np.array(new_centroids)

def calc_total_variance(X,clusters,centroids):
    Wks=[]
    for c in set(clusters):
        current_cluster = X[clusters==c]
        Wk=0
        for i in range(len(current_cluster)):
            Wk=Wk + calc_distance(current_cluster[i,:], centroids[c,:])
        Wks.append(Wk)
    return np.sum(Wks)

def k_median_clustering(X,number_cluster,replication_number,epsilon):
    np.random.seed(42)
    best_cost=float('inf')
    for i in range(replication_number):
        difference=1000
        centroids=initial_centroids(X,number_cluster)
        clusters=assign_clusters(X,centroids)
        variance=calc_total_variance(X,clusters,centroids)
        while difference>epsilon:
            centroids=calc_centroids(X,clusters)
            clusters=assign_clusters(X,centroids)
            newvariance=calc_total_variance(X,clusters,centroids)
            difference=np.abs(variance-newvariance)
            variance=newvariance
        if variance<=best_cost:
            best_cluster=clusters
            best_centroid=centroids
            best_cost=variance
    return best_cost,best_cluster,best_centroid


X = np.genfromtxt('K_Medians_Clustering_Data.csv', delimiter=',')

cost, clusters, centroids = k_median_clustering(X, number_cluster=3, replication_number=25, epsilon=0.01)

print("Cost: ", cost)
print("Clusters: ", clusters)
print("Centroids: ", centroids)