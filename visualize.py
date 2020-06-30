import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import os


def plot_fitness_graph(statistics, population):
    # Prepare data
    generation_number = range(0, population.generation)
    best_fitness = [genome.fitness for genome in statistics.most_fit_genomes]

    # Format graph
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(MultipleLocator(base=1.0))

    # Plot graph
    plt.plot(generation_number, statistics.get_fitness_mean(), label='Mean')
    plt.plot(generation_number, best_fitness, label='Best')
    plt.plot(generation_number, statistics.get_fitness_stdev(), label="Standard Deviation")
    plt.plot(generation_number, statistics.get_fitness_median(), label="Median")

    # Set labels
    plt.title("Fitness per generation")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(loc='best')
    
    # Save figure
    plt.savefig(os.path.join("models", "winner.png"), format='png')

    # Close
    plt.close()
