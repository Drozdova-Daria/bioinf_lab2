import logging
import numpy.random as rd
import numpy as np
import pandas as pd
from operator import itemgetter
from pathlib import Path
from collections import OrderedDict


class GeneticAlgorithm:
    def __init__(self, function, output: Path = Path("results")):
        self.chromosomes = None
        self.function = function
        self.res_dir = output

        self.stats_file = self.res_dir / "genetic_algorithm_result.txt"
        self.stats_file.parent.mkdir(parents=True, exist_ok=True)
        self.stats_file.unlink(missing_ok=True)

        self.generations_dir = Path(self.res_dir / "generations")
        self.generations_dir.mkdir(parents=True, exist_ok=True)

    def generate_new_part(self, chromosomes: np.ndarray, mutation=False, mutation_range=2, optimizer="min"):
        values = [self.function(*chromosome) for chromosome in chromosomes]
        chromosomes_dict = dict(zip([str(i) for i in range(4)], values))

        if optimizer == "min":
            chromosomes_dict = OrderedDict(sorted(chromosomes_dict.items(), key=lambda t: t[1]))
        elif optimizer == "max":
            chromosomes_dict = OrderedDict(sorted(chromosomes_dict.items(), key=lambda t: -t[1]))
        else:
            raise ValueError(f"{str(optimizer)} should be max or min")

        chromosome_indexes = list(chromosomes_dict.keys())
        good_chromosome = chromosomes[int(chromosome_indexes[2])]
        better_chromosome = chromosomes[int(chromosome_indexes[1])]
        best_chromosome = chromosomes[int(chromosome_indexes[0])]

        return np.array(
            [
                [better_chromosome[0] + float(mutation_range * mutation * rd.rand(1) - (mutation_range / 2)),
                 best_chromosome[1], ],
                [good_chromosome[0] + float(mutation_range * mutation * rd.rand(1) - (mutation_range / 2)),
                 best_chromosome[1], ],
                [best_chromosome[0],
                 better_chromosome[0] + float(mutation_range * mutation * rd.rand(1) - (mutation_range / 2)), ],
                [best_chromosome[0],
                 good_chromosome[1] + float(mutation_range * mutation * rd.rand(1) - (mutation_range / 2)), ],
            ]
        )

    def next_generation(self, mutation=False, mutation_range=2, optimizer="min"):
        part = np.array([self.chromosomes[j] for j in range(0, 4)])
        new_population = self.generate_new_part(part, mutation, mutation_range, optimizer)

        for parts_number in range(1, int(len(self.chromosomes) / 4)):
            part = np.array([self.chromosomes[j] for j in range(parts_number * 4, (parts_number + 1) * 4)])
            new_part = self.generate_new_part(part, mutation, mutation_range, optimizer)
            new_population = np.append(new_population, new_part, axis=0)

        return new_population

    def calculate(self, optimizer="min"):
        if optimizer == "min":
            return min(self.function(*chromosome) for chromosome in self.chromosomes)
        elif optimizer == "max":
            return max(self.function(*chromosome) for chromosome in self.chromosomes)
        else:
            raise ValueError(optimizer + " should be max or min")

    def start_genetic_algorithm(
            self,
            chromosomes_number=64,
            generations_number=10,
            mutation=False,
            mutation_range=2,
            optimizer="min",
    ):
        logging.info("Starting main optimizer method")

        self.chromosomes = np.array(
            [(mutation_range * rd.rand(self.function.args_count) - int(mutation_range / 2)) for _ in
             range(chromosomes_number)])
        logging.debug(f"Chromosomes array\n: {self.chromosomes}")

        x_dict = {'x1': 0, 'x2': 0}

        generations_value = []
        for idx in range(generations_number):
            logging.info(f"Starting iteration number {idx}")

            self.chromosomes = self.next_generation(mutation, float(mutation_range / (idx + 1)), optimizer, )
            logging.debug(f"Current chromosomes array\n {self.chromosomes}")

            df = pd.DataFrame(self.chromosomes, columns=[list(x_dict.keys())])
            for key in x_dict:
                x_dict[key] = np.array(df[key])
                if x_dict[key].shape[0] != 1:
                    x_dict[key] = x_dict[key].flatten()
            df['f(x1, x2)'] = self.function(*list(x_dict.values()))

            logging.debug(f"Current DataFrame:\n {df}")

            logging.debug(f"Dumping generation {idx + 1} DataFrame to file")
            df.to_csv(self.generations_dir / f"generation_{idx + 1}.csv")

            logging.debug("Writing stats to file")

            with self.stats_file.open("a") as sf:
                sf.write("_" * 70)
                sf.write(f"\nGeneration {idx + 1} info:\n")
                for chromosome in self.chromosomes:
                    sf.write(f"Chromosome {chromosome} gives value: {self.function(*chromosome)}\n")
                sf.write(f"{optimizer} value for this generation: {self.calculate(optimizer)}\n")

            generations_value.append(self.calculate(optimizer))

        with self.stats_file.open("a") as sf:
            sf.write(f"\nMinimum value {min(enumerate(generations_value), key=itemgetter(1))[1]}"
                     f" is reached at iteration {min(enumerate(generations_value), key=itemgetter(1))[0] + 1}")

        logging.info("Finishing main optimizer method")
