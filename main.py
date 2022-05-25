import logging
import sys
from pathlib import Path

from genetic_algorithm.genetic_algorithm import GeneticAlgorithm
from genetic_algorithm.Function import Function as Func

HELP = '--help'
FUNC_PARAM = '--func'
CHROM_PARAM = '--chrom'
GENER_PARAM = '--gener'
MUT_PARAM = '--mut'
MUT_RANGE_PARAM = '--mut_range'
PATH_PARAM = '--path'
TYPE_PARAM = '--type'
SYSTEM_PARAMS = {'1': FUNC_PARAM, '3': CHROM_PARAM, '5': GENER_PARAM, '7': MUT_PARAM, '9': MUT_RANGE_PARAM,
                 '11': PATH_PARAM, '13': TYPE_PARAM}
TYPES = ['run', 'debug']


def run_genetic_algorithm(function, chromosomes, generation, mut, mut_range, result_path, run_type):
    loging_level = logging.INFO if run_type == 'run' else logging.DEBUG
    logging.basicConfig(filename=f"{result_path}\logfile.log",
                        filemode="w",
                        format="%(levelname)s %(asctime)s - %(message)s",
                        level=loging_level)

    func = Func(function)
    logging.debug("Function create")

    genetic_algorithm = GeneticAlgorithm(func, Path(result_path))
    logging.debug("Optimizer create")

    genetic_algorithm.start_genetic_algorithm(
        chromosomes_number=chromosomes,
        generations_number=generation,
        mutation_range=mut_range,
    )

    print(f'The algorithm was completed successfully, the results are in the directory {result_path}')


if __name__ == '__main__':
    function = ''
    chromosomes = 0
    generation = 0
    mut = False
    mut_range = 0
    result_path = ''
    run_type = ''

    if len(sys.argv) == 2:
        if sys.argv[1] != HELP:
            print(f'System arguments error: use param {HELP} for information')
            exit(1)
        else:
            print('This program implements a genetic algorithm. To start, you need to enter the following parameters:\n'
                  "--func (string) - function of two variables (x1, x2) (Example: --func 'x1 + x2')\n"
                  "--chrom (int) - number of chromosomes in the population (Example: --chrom 1)\n"
                  "--gener (int) - number of algorithm runs (Example: --gener 1)\n"
                  "--mut (int) - are mutations allowed (1) or not (0) (Example: --mut 1)\n"
                  "--mut_range (int) - mutation value (Example: --mut_range 2) \n"
                  "--path (string) - result directory (Example: --path 'results') \n"
                  "--type (string) - running ('run') or debugging ('debug') an algorithm(Example: --type 'run')")
            exit(0)

    if len(sys.argv) != 15:
        print('System arguments error: invalid number of arguments')
        exit(1)

    for index in SYSTEM_PARAMS.keys():
        key = index
        index = int(index)
        if sys.argv[index] != SYSTEM_PARAMS[key]:
            print(f'System arguments error: invalid name of parameter {index + 1}, use {SYSTEM_PARAMS[key]}')
            exit(1)
        if sys.argv[index] == FUNC_PARAM:
            function = sys.argv[index + 1]
        elif sys.argv[index] == CHROM_PARAM:
            chromosomes = int(sys.argv[index + 1])
        elif sys.argv[index] == GENER_PARAM:
            generation = int(sys.argv[index + 1])
        elif sys.argv[index] == MUT_PARAM:
            if int(sys.argv[index + 1]) not in [0, 1]:
                print(f'System arguments error: invalid value of parameter {MUT_PARAM}, value should be 1 or 0')
                exit(1)
            mut = bool(int(sys.argv[index + 1]))
        elif sys.argv[index] == MUT_RANGE_PARAM:
            mut_range = int(sys.argv[index + 1])
        elif sys.argv[index] == PATH_PARAM:
            result_path = sys.argv[index + 1]
        elif sys.argv[index] == TYPE_PARAM:
            run_type = sys.argv[index + 1]
            if run_type not in TYPES:
                print(f'System arguments error: invalid value of parameter {TYPE_PARAM}, value should be in {TYPES}')
                exit(1)

    run_genetic_algorithm(function, chromosomes, generation, mut, mut_range, result_path, run_type)
