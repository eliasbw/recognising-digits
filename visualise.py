from matplotlib import pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap

from logic import train


def visualise(pattern_from_gui, colors):
    cmap = ListedColormap(colors)


    plt.imshow(pattern_from_gui, cmap=cmap)
    patches = [Patch(color=colors[i], label="Zeros" if i == 1 else "Ones") for i in [0, 1]]
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title("The input data")
    plt.show()

    iterated_pattern = train(pattern_from_gui)

    plt.imshow(iterated_pattern, cmap=cmap)
    plt.title("The pattern found")
    patches = [Patch(color=colors[i], label="Zeros" if i == 1 else "Ones") for i in [0, 1]]
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()
