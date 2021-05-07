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
                yes_sum[i] += rows[i]
            num_yes += 1
        if rows[ncol-1] == "no":
            for i in range(ncol-1):
                no_sum[i] += rows[i]
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
                yes_dev[i] += (rows[i] - yes_means[i])**2
        if rows[ncol-1] == "no":
            for i in range(ncol-1):
                no_dev[i] += (rows[i] - no_means[i])**2

    #ATTR STDDEV
    yes_stddev = [math.sqrt(x / (num_yes-1)) for x in yes_dev]
    no_stddev = [math.sqrt(x / (num_no-1)) for x in no_dev]

    for t in test:
        resultYes = 1
        resultNo = 1
        for index in range(len(t)):
            resultYes *= calc_pdf(t[index], yes_means[index], yes_stddev[index])
            resultNo *= calc_pdf(t[index], no_means[index], no_stddev[index])
        resultYes *= pYes
        resultNo *= pNo

        #ONLY NEED TO COMPARE NUMERATOR
        if resultYes >= resultNo:
            print("yes")
        else:
            print("no")
        
def KNN(k: int, training_data: list, test_data: list) -> None:
    #initialization
    ncol = len(training_data[0]) 
    
    for test in test_data:
        
        #create nested list(element = [edist,class])
        edist_class = []
        for train in training_data:
            edist = 0
            for i in range(ncol-1):
                edist += (test[i]-train[i])**2
            edist_class.append([math.sqrt(edist), train[-1]])
        
        #sort list according to edist
        edist_class.sort(key = lambda x: x[0]) 
        
        #retrieve class of kth closest training example
        kclass = [] 
        for i in range(k):
            kclass.append(edist_class[i][1])
            
        #count number of item in classes
        num_yes = 0
        num_no = 0
        for item in kclass:
            if item == "yes":
                num_yes += 1
            if item == "no":
                num_no += 1
        
        #result
        if num_yes >= num_no:
            print("yes")
        else:
            print("no")

def main(args: list) -> None:       

    if len(args) != 3:
        print("Usage: MyClassifier.py <Path_to_training> <Path_to_test> <Algorithm Type>")
        sys.exit()
    training_data = []
    test_data = []

    #PARSES TRAINING SET INTO 2D ARRAY "training_data"
    with open(args[0]) as training_file:
        training_reader = csv.reader(training_file, delimiter = ",")
        ncol = len(next(training_reader))               #Reads the first line and counts number of cols
        training_file.seek(0)                           #Goes back to the beginning of the file

        for row in training_reader:
            training_data_row = []
            for i in range(ncol-1):
                training_data_row.append(float(row[i]))
            training_data_row.append(row[ncol-1])
            training_data.append(training_data_row)

    #PARSES TEST SET INTO 2D ARRAY "test_data"
    with open(args[1]) as test_file:
        test_reader = csv.reader(test_file, delimiter = ",")

        for row in test_reader:
            test_data_row = []
            for item in row:
                test_data_row.append(float(item))
            test_data.append(test_data_row)

    #RUN NB
    if args[2] == "NB":
        NB(training_data , test_data)
        return


    #RUN KNN
    if "NN" in args[2]:
        k = int(args[2].replace("NN",""))
        KNN(k, training_data , test_data)
        return

if __name__ == "__main__":
    main(sys.argv[1:])