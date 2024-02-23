import numpy as np
import math
import matplotlib.pyplot as plt

# # Load the data from MNIST-5-6-Subset.txt
data_file_path = "/Users/jack/Documents/Folder/School/Copenhagen/Semester 1/MLA/Assignment 1/MNIST-5-6-Subset/MNIST-5-6-Subset.txt"
data_matrix = np.loadtxt(data_file_path).reshape(1877, 784)
# # Load the labels from MNIST-5-6-Labels.txt
labels_file_path = "/Users/jack/Documents/Folder/School/Copenhagen/Semester 1/MLA/Assignment 1/MNIST-5-6-Subset/MNIST-5-6-Subset-Labels.txt"
labels = np.loadtxt(labels_file_path)

varienceVectors = []

# test_point = data_matrix[0]
# test_label = 5

def euclidian_distance(point_a, point_b):
    value = 0
    for d in range(len(point_a)):
        value += (point_a[d] - point_b[d]) ** 2

    return math.sqrt(value)


def knn(training_points, training_labels, test_point, test_label):
    return_vector = []

    test_label = 1.0 if test_label == 5 else -1.0

    training_labels[training_labels == 5] = 1.0
    training_labels[training_labels == 6] = -1.0

    m = training_labels.shape[0]
    distances = []

    for k in range(m):
        distance_tuple = (training_labels[k], euclidian_distance(test_point, training_points[k]))
        distances.append(distance_tuple)

    sorted_distances = sorted(distances, key = lambda x: x[1])

    for k in range(m):
        accuracy = 0
        for i in range(k+1):
            if sorted_distances[i][0] == test_label:
                accuracy += 1

        accuracy /= (k + 1)
        return_vector.append(1-accuracy)

    return return_vector

def validation_sets(m, n, i):
    lower_bound = m + (i*n) + 1
    upper_bound = m + (i+1) * n
    return (lower_bound, upper_bound)

def run_validation(m, n):
    errorVectors = []
    for i in range(1, 6):
        lower_bound = validation_sets(m, n, i)[0]
        upper_bound = validation_sets(m, n, i)[1]

        testing_points = data_matrix[lower_bound:upper_bound]
        testing_labels = labels[lower_bound:upper_bound]

        error_vector = np.zeros(m)
        for x in range(len(testing_points)):
            error_vector += np.array(knn(data_matrix[:m], labels[:m], testing_points[x], testing_labels[x]))
        error_vector /= n

        errorVectors.append(error_vector)
        plt.plot(error_vector, label=f"Validation Set #{i}")

    vv = []
    for i in range(m):
        vv.append(np.var([errorVectors[0][i], errorVectors[1][i], errorVectors[2][i], errorVectors[3][i], errorVectors[4][i]]))
    varienceVectors.append(vv)

    plt.xlabel("k")
    plt.ylabel("error")
    plt.legend()
    plt.show()


### Part 1 ###
ns = [10, 20, 40, 80]
for n in ns:
    plt.title(f"Validation Error (n={n})")
    run_validation(50, n)

for vv in range(len(varienceVectors)):
    plt.plot(varienceVectors[vv], label=f"n={ns[vv]}")
plt.title("Variance of the Validation Error")
plt.ylabel("Variance")
plt.xlabel("K")
plt.legend()
plt.show()


### Part 2 ###
paths = ["MNIST-5-6-Subset", "MNIST-5-6-Subset-Light-Corruption", "MNIST-5-6-Subset-Moderate-Corruption", "MNIST-5-6-Subset-Heavy-Corruption"]

for p in paths:
    data_file_path = f"/Users/jack/Documents/Folder/School/Copenhagen/Semester 1/MLA/Assignment 1/MNIST-5-6-Subset/{p}.txt"
    data_matrix = np.loadtxt(data_file_path).reshape(1877, 784)
    plt.title(f"Validation Error for {p} (n=80)")
    run_validation(50, 80)