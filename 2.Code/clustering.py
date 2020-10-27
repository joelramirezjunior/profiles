# Clustering
# Author: Joel Ramirez Jr.
# ------------------------
# V 1.0

import matplotlib.pyplot as plt
import csv, collections, math, numpy
import random
import glob
from numpy import genfromtxt
from kneed import KneeLocator
from scipy.signal import argrelextrema
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from utilities import returnCleanNPArray, returnClusterMeasures
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_moons
from sklearn.metrics import adjusted_rand_score

path = "70thpercentile/*.csv"

cluster_measures = []


#Iterating through all Subjects in the path above, here we grab each respective
#participants AWC above their respective 70th percentile
for fname in glob.glob(path):
    subject, time, value = returnCleanNPArray(fname, "AWC")

    #needed to emphasize similarities in AWC as apposed to Time.
    time = 10000000*numpy.vstack(time)
    value = numpy.vstack(value)

    features = numpy.concatenate((time, value), axis = 1)


    kmeans_kwargs = {
        "init": "random",
        "n_init": 10,
        "max_iter": 300,
        "random_state": 42,
    }


    # A list holds the silhouette coefficients for each k. Here, this measures
    # Basically tells you how good it would be to have k clusters for a certain participant
    silhouette_coefficients = []

    # Notice you start at 2 clusters for silhouette coefficient, as 1 cluster would
    # just group all the points which is pointless.
    for k in range(2, len(time)-1):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(features)
        score = silhouette_score(features, kmeans.labels_)
        silhouette_coefficients.append(score)


    # plt.style.use("fivethirtyeight")
    # plt.plot(range(2, len(time)-1), silhouette_coefficients)
    # plt.xticks(range(2, len(time)-1))
    # plt.xlabel("Number of Clusters")
    # plt.ylabel("Silhouette Coefficient")
    # plt.show()


    ###making it at least 2 segments per cluster

    minima = argrelextrema(numpy.array(silhouette_coefficients), numpy.less)


    labels = []
    old_labels = []
    for min in list(minima)[0]:

        kmeans_silhouette = silhouette_coefficients[min]

        #dictates to use the previous min, as the current one does not keep consectuive
        #lena awcs

        minToUse = min
        previousMin = False

        kmeans = KMeans(
            init="random",
            n_clusters= min+1,
            n_init=500,
            max_iter=300,
            random_state=42
        )

        if kmeans_silhouette >= .25:

            kmeans.fit(features)
            labels, old_labels = kmeans.labels_, labels



            clusterSize = []

            newNum = 0
            for i in range(len(labels)-1):
                # print(i)
                used = set()


                if i != 1:
                    if labels[i] in used:
                        previousMin = True
                        break

                    if labels[i] != labels[i+1]:
                        used.add(int(labels[i]))
                        newNum = 0

                    if labels[i] != labels[i+1] and newNum == 1:
                        previousMin = True
                        break
                    newNum += 1



        if previousMin:
            labels = old_labels
            break

    # fig, (ax1) = plt.subplots(
    #     1, 1, figsize=(8, 6), sharex=True, sharey=True
    # )
    # fig.suptitle(f"Clustering Algorithm Comparison: Pockets of Language for {fname}", fontsize=16)
    # r = lambda: random.randint(0,255)
    # fte_colors = ['#%02X%02X%02X' % (r(),r(),r()) for i in range(0,300)]
    # # The k-means plot
    # km_colors = [fte_colors[label] for label in labels]
    #
    # print(labels)
    #
    #
    # ax1.set_title(f"k-means\nSilhouette: {kmeans_silhouette}, whith {min+1} clusters", fontdict={"fontsize": 12} )
    # ax1.scatter(features[:, 0], features[:, 1], c=km_colors)
    # ax1.grid()
    # plt.show()

    clusterNum, clusterAvgSize = returnClusterMeasures(labels)

    cluster_measures.append([subject, clusterNum, clusterAvgSize])


print(cluster_measures)


with open('clusterMeasures.csv', 'w') as csvfile:

        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        header = ['SUBJECT', 'nclusters', 'avgclustersize']
        csvwriter.writerow(header)

        for i in cluster_measures:

            sub = i[0]
            nclus = i[1]
            mclussize = i[2]
            csvwriter.writerow([sub, nclus, mclussize])




    # kmeans = KMeans(
    #     init="random",
    #     n_clusters=3,
    #     n_init=500,
    #     max_iter=300,
    #     random_state=42
    # )
    #
#
# sse = []
# for k in range(1, len(time)):
#     print(f"Currently on cluster {k}")
#     kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
#     kmeans.fit(features)
#     sse.append(kmeans.inertia_)
#
# plt.style.use("fivethirtyeight")
# plt.plot(range(1,len(time)), sse)
# plt.xticks(range(1, len(time)))
# plt.xlabel("Number of Clusters")
# plt.ylabel("SSE")
# plt.show()
#
# kl = KneeLocator(
#     range(1, len(time)), sse, curve="convex", direction="decreasing"
# )
#
# print(kl.elbow)
