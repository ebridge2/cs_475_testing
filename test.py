#
# a python script to automate testing
#
# written by Eric Bridgeford
#
# Usage:
# python test.py /path/to/your/code/
#

from argparse import ArgumentParser
from subprocess import Popen, PIPE
import time


class Test:
    algorithms = {"perceptron" : 0, "averaged_perceptron" : 0, "margin_perceptron" : 0,
                 "pegasos" : 0, "knn" : 1}
    bin_datasets = ["easy", "hard", "bio", "speech", "finance", "vision", "nlp"]
    mc_datasets = ["speech.mc"]
   
    def __init__(self, code, verbose):
        print "algorithm | accuracy | duration"
        self.code = code
        self.verbose = verbose
        pass

    def run(self):
        for algorithm in self.algorithms:
            try:
                print algorithm    
                for dataset in self.bin_datasets:
                    self.run_dataset(algorithm, dataset)
                if self.algorithms[algorithm] > 0:
                    for dataset in self.mc_datasets:
                        self.run_dataset(algorithm, dataset)
            except ValueError as e:
                print str(e)
        pass

    def run_dataset(self, algo, dataset):
        cmd_train = "python " + self.code + "classify.py --mode train --algorithm " +\
              algo + " --model-file datasets/" + dataset + "." + algo + ".model --data datasets/" +\
              dataset + ".train"
        cmd_test = "python " + self.code + "classify.py --mode test --model-file datasets/" +\
              dataset + "." + algo + ".model --data datasets/" + dataset + ".dev " +\
              "--predictions-file datasets/" + dataset + ".dev.predictions"
        start = time.time()
        self.execute_cmd(cmd_train, algo)
        self.execute_cmd(cmd_test, algo)
        run_time = time.time() - start
        cmd_cmp = "python compute_accuracy.py datasets/" + dataset + ".dev datasets/" + \
                  dataset + ".dev.predictions"
        (acc, err) = self.execute_cmd(cmd_cmp, algo)
        print str(dataset + " | " + acc[:-2] + " | " + '%.4f' % (run_time,) + "(s)")
        pass

    def execute_cmd(self, cmd, algorithm):
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        out, err = p.communicate()
        code = p.returncode
        if code:
            err_mssg = "Your code did not work for algorithm: " + algorithm
            if self.verbose:
                raise ValueError(err_mssg + "\nError  " + str(code) + ": \n" + err)
            else:
                raise ValueError(err_mssg)
        return out, err


def main():
    parser = ArgumentParser()
    parser.add_argument("--code", "-c", help="The path to your code directory,\
                        containing all relevant\npython dependencies and \
                        classify.py.\n Note that we assume your directory is\
                        passed as /path/to/code/.")
    parser.add_argument("--verbose", "-v", help="Boolean value indicating whether \
                        you want the error messages.\n (0 or 1).")
    result = parser.parse_args()
    test = Test(result.code, result.verbose)
    test.run()


if __name__ == "__main__":
    main()
