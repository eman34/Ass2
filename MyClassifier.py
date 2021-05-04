import sys
from node import Node
import csv
import math

def calc_pdf(x , mu, sig) -> float:
    result = 1.0/(sig*math.sqrt(2*math.pi)) * math.exp((-(x - mu)**2) / (2*sig**2)) 
    return result  

def calc_mean_NB(training_data: list) -> list:
    means = []
    

def NB(training_data: list, test: list) -> None:




def main(args: list) -> None:

    arguments = ["Path" , "Path" , "Type of Algo"]
    training_data = []
    test_data = []

    with open(arguments[0]) as training_file:
        training_reader = csv.reader(training_file, delimiter = ",")
        for row in training_reader:


    with open(arguments[1]) as test_file:
        test_reader = csv.reader(test_file, delimiter = ",")
        ncol = len(next(test_reader))               #Reads the first line and counts number of cols
        test_file.seek(0)                           #Goes back to the beginning of the file

        if arguments[2] == "NB":
            for row in test_reader:

    


        if arguments[2] == "KNN":
            for row in test_reader:
                #TODO Heidi
    


if __name__ == "__main__":
    main(sys.argv[1:])