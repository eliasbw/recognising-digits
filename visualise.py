from matplotlib import pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap

from hopfield_logic import train


def generate_figures(pattern_from_gui, colors):
    cmap = ListedColormap(colors)
    patches = [
        Patch(color=colors[i], label="Zeros" if i == 0 else "Ones") for i in [0, 1]
    ]

    plt.imshow(pattern_from_gui, cmap=cmap)
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
    plt.title("The input data")
    plt.show()

    iterated_pattern = train(pattern_from_gui)
    plt.imshow(iterated_pattern, cmap=cmap)
    plt.title("The pattern found")
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
    plt.show()
