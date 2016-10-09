# Repository for 600.475 automated testing

Make a PR, post an issue, or send us a message if you have issues running this. 

## Usage:
```
# standard usage

$ python test.py --path /path/to/your/code/ --verbose 0 --cmd 0 --clean 1

# Detailed Usage Information

$ python test.py --help

usage: test.py [-h] [--path PATH] [--verbose VERBOSE] [--clean CLEAN]
               [--cmd CMD]

optional arguments:
  -h, --help            show this help message and exit
  --path PATH, -p PATH  The path to your code directory, containing all
                        relevant python dependencies and classify.py. Note
                        that we assume your directory is passed as
                        /path/to/code/.
  --verbose VERBOSE, -v VERBOSE
                        Boolean value indicating whether you want the error
                        messages. (0 or 1). (default is 1)
  --clean CLEAN, -c CLEAN
                        Boolean value indicating whether you want to eliminate
                        all existing *.pyc files in your code directory. These
                        can somethimes cause issues (0 or 1). (default is 0)
  --cmd CMD             Boolean value indicating whether you want to output
                        the commands as well (0 or 1). (default is 0)



```

Note that if you want to clear intermediate files produced by your runs (ie, if you wanted to just have the same repo for every homework, and are lazy like me and don't want to manually delete the model files and stuff in between, or just to reset the repo if you play around with the shell script), you can call:

```
git reset --hard origin/master
```

To reset the branch to the latest commit. 

## Disclaimers
 
This repo is not guaranteed to be up to date with homeworks on the day they come out (ie, it may not test the latest algorithm additions), but expect it to be generally updated within a day or two of each homework release.
