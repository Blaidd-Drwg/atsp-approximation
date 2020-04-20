import matplotlib.pyplot as plt
from csv import DictReader
import sys
import os

# Script to plot both algorithms' multibeta results

instances = ['br17', 'ft53', 'ft70', 'ftv170', 'ftv33', 'ftv35', 'ftv38', 'ftv44', 'ftv47', 'ftv55',
             'ftv64', 'ftv70', 'kro124p', 'p43', 'rbg323', 'rbg358', 'rbg403', 'rbg443', 'ry48p']
single_plot = True
save_plot = True


def main():
    if len(sys.argv) == 1:
        print("Usage: python3 plot_results.py resultdir")
        print("This script plots the results of multibeta experiments. The input filenames are hardcoded as '{resultdir}/{instance}.atsp.{c/t}'. The plots are saved in resultdir.")
        exit()

    directory = sys.argv[1]
    for instance in instances:
        if single_plot:
            _, ax1 = plt.subplots(1, 1, figsize=(8, 4))
            ax2 = ax1
        else:
            _, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
        plot_experiment(os.path.join(directory, f'{instance}.atsp.c'), ax1, 'o', 'Generalized Christofides algorithm')
        plot_experiment(os.path.join(directory, f'{instance}.atsp.t'), ax2, 's', 'Generalized tree-doubling algorithm')
        adjust_ax_limits(ax1, ax2)
        plt.title(instance)
        plt.tight_layout()
        plt.legend()

        if save_plot:
            plt.savefig(os.path.join(directory, f'{instance}_atsp.pdf'))
        else:
            plt.show()


def plot_experiment(filename, ax, marker, label):
    ax.set_xlabel('approximation factor')
    ax.set_ylabel('kernel size')

    try:
        with open(filename) as f:
            data = list(DictReader(f, delimiter=',', skipinitialspace=True))[:-1]
    except FileNotFoundError:
        print(f"Warning: file '{filename}' does not exist")
        return

    try:
        tour_lengths = [int(d['tour_cost']) for d in data]
        opt_tour_length = tour_lengths[0]
        relative_tour_lengths = [l / opt_tour_length for l in tour_lengths]
        kernel_sizes = [int(d['kernel_size']) for d in data]
    except Exception:
        print(f"Error: Failed to plot file '{filename}'")
        return

    ax.scatter(relative_tour_lengths[1:-1], kernel_sizes[1:-1], marker=marker, label=label)
    ax.set_ylim(bottom=-3)
    ax.set_xlim(left=0.98)
    # quick hack because in this one plot the legend covers a data point:
    if 'ry48p' in filename:
        ax.set_ylim(top=53)


def adjust_ax_limits(ax1, ax2):
    ylim = (min(ax1.get_ylim()[0], ax2.get_ylim()[0]), max(ax1.get_ylim()[1], ax2.get_ylim()[1]))
    xlim = (min(ax1.get_xlim()[0], ax2.get_xlim()[0]), max(ax1.get_xlim()[1], ax2.get_xlim()[1]))
    ax1.set_ylim(ylim)
    ax2.set_ylim(ylim)
    ax1.set_xlim(xlim)
    ax2.set_xlim(xlim)


if __name__ == '__main__':
    main()
