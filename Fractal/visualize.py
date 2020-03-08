
import numpy as np
import cv2
import os

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def main():
    inputDirectory = "C:\Pictures"
    dir_list = os.listdir(inputDirectory)
    images = list(filter(lambda x: "layer(" in x, dir_list))
    listImages = list()
    for image in images:
        path = os.path.join(inputDirectory, image)
        img = cv2.imread(path, 1)
        listImages.append(img)

    xs = list()
    ys = list()
    zs = list()

    for i, img in enumerate(listImages):
        indexes = np.argwhere(np.all(img < 10, axis=2))
        z = np.ones(indexes.shape[0]) * i
        print(indexes[:, 0])
        xs.append(indexes[:, 0])
        ys.append(indexes[:, 1])
        zs.append(z)

    print(xs)
    xs = np.hstack(xs)
    print(xs)
    ys = np.hstack(ys)
    zs = np.hstack(zs)

    ax = Axes3D(plt.figure(figsize=(50, 50)))

    ax.scatter(xs=xs, ys=ys, zs=zs, marker='o', c='r')
    plt.show()
    # plt.savefig('fig.png')


main()
