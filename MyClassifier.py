import sys
from node import Node
import csv
import math

def calc_pdf(x , mu, sig) -> float:
    result = 1.0/(sig*math.sqrt(2*math.pi)) * math.exp((-(x - mu)**2) / (2*sig**2)) 
    return result  
    
def NB(training_data: list, test: list) -> None:
    
    ncol = len(training_data[0])
    yes_sum = [0]*(ncol-1)
    no_sum=[0]*(ncol-1)
    num_examples = 0
    num_yes = 0
    num_no = 0
    for rows in training_data:
        if rows[ncol-1] == "yes":       #if last column is "yes"
            for i in range(ncol-1):     #range of ncol-1
                yes_sum[i] += float(rows[i])
            num_yes += 1
        if rows[ncol-1] == "no":
            for i in range(ncol-1):
                no_sum[i] += float(rows[i])
            num_no += 1
        num_examples += 1

    if num_examples != num_yes + num_no:
        print("There is an error with data")
        sys.exit()


    #ATTR MEANS & CLASS PROBS
    yes_means = [x/num_yes for x in yes_sum]
    no_means = [x/num_no for x in no_sum]
    pYes = num_yes / num_examples
    pNo = 1-pYes


    yes_dev = [0]*(ncol-1)
    no_dev =[0]*(ncol-1)
    for rows in training_data:
        if rows[ncol-1] == "yes":               #if last column is "yes"
            for i in range(ncol-1):             #range of ncol-1
                yes_dev[i] += (float(rows[i]) - yes_means[i])**2
        if rows[ncol-1] == "no":
            for i in range(ncol-1):
                no_dev[i] += (float(rows[i]) - no_means[i])**2

    #ATTR STDDEV
    yes_stddev = [math.sqrt(x / (num_yes-1)) for x in yes_dev]
    no_stddev = [math.sqrt(x / (num_no-1)) for x in no_dev]

    for t in test:
        resultYes = 1
        resultNo = 1
        for index in range(len(t)):
            print(t[index])
            #resultYes *= calc_pdf(float(t[index]), yes_means[index], yes_stddev[index])
            #resultNo *= calc_pdf(float(t[index]), no_means[index], no_stddev[index])
        resultYes *= pYes
        resultNo *= pNo

        #ONLY NEED TO COMPARE NUMERATOR
        """
        if resultYes >= resultNo:
            print("yes")
        else:
            print("no")
        """

#TODO  
def main(args: list) -> None:       

    arguments = ["pima.csv" , "test.csv" , "NB"]
    training_data = []
    test_data = []

    #PARSES TRAINING SET INTO 2D ARRAY "training_data"
    with open(arguments[0]) as training_file:
        training_reader = csv.reader(training_file, delimiter = ",")
        ncol = len(next(training_reader))
        training_file.seek(0)

        for row in training_reader:
            training_data_row = []
            for item in row:
                training_data_row.append(item)
            training_data.append(training_data_row)

    #PASSES TEST SET INTO 2D ARRAY "test_data"
    with open(arguments[1]) as test_file:
        test_reader = csv.reader(test_file, delimiter = ",")
        ncol = len(next(test_reader))               #Reads the first line and counts number of cols
        test_file.seek(0)                           #Goes back to the beginning of the file

        for row in test_reader:
            test_data_row = []
            for item in row:
                test_data_row.append(item)
            test_data.append(training_data_row)

    if arguments[2] == "NB":
        NB(training_data , test_data)
        return

    


if __name__ == "__main__":
    main(sys.argv[1:])