"""Wizard, iterates through testing sub directory and requests if to run coverage test to specific module
"""
import glob, os
DIR = os.path.join(os.path.abspath(os.path.curdir),"testing")
to_be_tested_for_coverage = []
for f in glob.glob(DIR+"*/**"):
    if f.__contains__(".py") and f != __file__:
        while (True):
            answer = input("\nTest "+ f + " for coverage? y/n \n")
            if answer == "y" or answer == "yes":
                to_be_tested_for_coverage.append(f)
            if answer == "y" or answer == "n" or answer == "no" or answer =="yes":
                break
            if answer != "y" or answer != "n":
                print("Please enter y/n/yes/no")
                

to_be_tested_for_coverage = [i.replace(DIR,"testing") for i in to_be_tested_for_coverage]
if len(to_be_tested_for_coverage) > 0:
    print("######################### Testing... ############################ \n\n")
[os.system("coverage run "+i+"; coverage report -m") for i in to_be_tested_for_coverage]