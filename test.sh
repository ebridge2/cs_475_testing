#!/bin/bash
#
# a shell script to automate testing. Makes batch testing simpler.
#
# written by Eric Bridgeford
# #ShellFTW
#
# Usage:
# ./test.sh /path/to/your/code/
# Inputs:
#    $1: /path/to/your/code/
#        The path to a directory containing your python code.
#        This directory should contain classify.py,
#        cs_475_types.py, and any files required for new
#        models week to week.  
#
# If you have any comments or suggestions, send me a message or
# make a PR

# add to this array as we add more algorithms for the class
algorithm=(perceptron averaged_perceptron margin_perceptron pegasos)
#your possible datasets
options=(nlp easy hard bio speech finance vision)

echo "option | algorithm | accuracy | duration"

# loop over everything...
for opt in "${options[@]}"; do
    for algo in "${algorithm[@]}"; do
        start=$(($(date +%s%N)/1000000)) # get the time
        python ${1}classify.py --mode train --algorithm $algo --model-file data/${opt}.perceptron.model --data data/${opt}.train

        python ${1}classify.py --mode test --model-file data/${opt}.perceptron.model --data data/${opt}.dev --predictions-file data/${opt}.dev.predictions
        end=$(($(date +%s%N)/1000000))
        duration=$(( end - start ))

        # just store the output here and echo it back formatted
        acc="$(python compute_accuracy.py ${opt}.dev ${opt}.dev.predictions)"

        echo "${opt} | $algo | $acc | $duration (ms)"

    done
done
