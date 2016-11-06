#
# a python script to automate testing
#
# written by Eric Bridgeford
#
# Usage:
# python unsupervised_tests.py /path/to/your/code/
#

from argparse import ArgumentParser
from subprocess import Popen, PIPE
import time
import re


class Test:
    bin_datasets = ["small_clusters", "easy", "hard", "bio", "speech", "finance", "vision"]#, "small_clusters"]
    mc_datasets = ["speech.mc"]
   
    def __init__(self, code, verbose, clean, cmd_full, algorithm):
        print "datasets | variation of info | number of clusters | duration"
        self.code = code
        self.verbose = verbose
        self.cmd_full = cmd_full
        self.algo = algorithm
        if clean:
            clean_cmd = "rm " + self.code + "*.pyc"
            self.execute_cmd(clean_cmd)
            clean_datasets = "rm datasets/*.model datasets/*.predictions"
        pass

    def run(self):

        if self.algo == "lambda_means":
            self.lambda_means()
        elif self.algo == "nb_clustering":
            self.naive_bayes()
        pass

    def lambda_means(self):
        lambdas = [0.0]
        for dataset in (self.bin_datasets + self.mc_datasets):
            for lambd in lambdas:
                print "lambda = " + str(lambd)
                cmd_train = "python " + self.code + "classify.py --mode train --algorithm " +\
                  self.algo + " --model-file datasets/" + dataset +"." + self.algo + ".model --data datasets/" +\
                  dataset + ".train --cluster-lambda " + str(lambd) + " --clustering-training-iterations " + "10"
                cmd_test = "python " + self.code + "classify.py --mode test --model-file datasets/" +\
                    dataset + "." + self.algo + ".model --data datasets/" + dataset + ".dev " +\
                    "--predictions-file datasets/" + dataset + ".dev.predictions"
                start = time.time()
                self.execute_cmd(cmd_train, self.algo)
                self.execute_cmd(cmd_test, self.algo)
                run_time = time.time() - start
                cmd_cmp = "python cluster_accuracy.py datasets/" + dataset + ".dev datasets/" + \
                    dataset + ".dev.predictions"
                (acc, err) = self.execute_cmd(cmd_cmp, self.algo)
                cmd_clus = "python number_clusters.py datasets/" + dataset + ".dev.predictions"
                (nclus, err) = self.execute_cmd(cmd_clus, self.algo)
                nclus = re.split('\n', nclus) 
                print str(dataset + " | " + acc[:-1] + " | " + nclus[-2] + " | " + "%.4f" % (run_time,) + "(s)")
     
        pass

    def naive_bayes(self):
        nclusts = [3]
        for dataset in (self.bin_datasets + self.mc_datasets):
            for n in nclusts:
                print "nclusts = " + str(n)
                cmd_train = "python " + self.code + "classify.py --mode train --algorithm " +\
                  self.algo + " --model-file datasets/" + dataset +"." + self.algo + ".model --data datasets/" +\
                  dataset + ".train --num-clusters " + str(n) + " --clustering-training-iterations " + "10"
                cmd_test = "python " + self.code + "classify.py --mode test --model-file datasets/" +\
                    dataset + "." + self.algo + ".model --data datasets/" + dataset + ".dev " +\
                    "--predictions-file datasets/" + dataset + ".dev.predictions"
                start = time.time()
                self.execute_cmd(cmd_train, self.algo)
                self.execute_cmd(cmd_test, self.algo)
                run_time = time.time() - start
                cmd_cmp = "python cluster_accuracy.py datasets/" + dataset + ".dev datasets/" + \
                    dataset + ".dev.predictions"
                (acc, err) = self.execute_cmd(cmd_cmp, self.algo)
                cmd_clus = "python number_clusters.py datasets/" + dataset + ".dev.predictions"
                (nclus, err) = self.execute_cmd(cmd_clus, self.algo)
                nclus = re.split('\n', nclus) 
                print str(dataset + " | " + acc[:-1] + " | " + nclus[-2] + " | " + "%.4f" % (run_time,) + "(s)")
     
        pass

    def execute_cmd(self, cmd, algorithm=None):
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        if self.cmd_full:
            print cmd
        out, err = p.communicate()
        code = p.returncode
        if code:
            err_mssg = ""
            if algorithm is not None:
                err_mssg += "Your code did not work for algorithm: " + algorithm
            if self.verbose:
                err_mssg += "\nError  " + str(code) + ": \n" + err
            else:
                raise ValueError(err_mssg)
        return out, err


def main():
    parser = ArgumentParser()
    parser.add_argument("--path", "-p", help="The path to your code directory,\
                        containing all relevant\npython dependencies and \
                        classify.py.\n Note that we assume your directory is\
                        passed as /path/to/code/.")
    parser.add_argument("--verbose", "-v", help="Boolean value indicating whether \
                        you want the error messages.\n (0 or 1). (default is 1)", default=1)
    parser.add_argument("--clean", "-c", help="Boolean value indicating whether \
                        you want to eliminate all existing\n*.pyc files in your code \
                        directory. These can somethimes cause issues (0 or 1). (default is 0)", default=0)
    parser.add_argument("--cmd", help="Boolean value indicating whether \
                        you want to output the commands as well (0 or 1). (default is 0)", default=0)
    parser.add_argument("--algorithm", "-a", help="the algorithm to test. Options are (lambda_means)")
    result = parser.parse_args()
    test = Test(result.path, result.verbose, result.clean, result.cmd, result.algorithm)
    test.run()


if __name__ == "__main__":
    main()
