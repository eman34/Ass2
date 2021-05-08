import sys
import csv
import math

#will be around 3% lower accuracy than weka as implementation is different. 
#Accuracy maybe for comp3368 was about 70 for most ppl instead of 95
#Needs to be stratified, as well as 10-fold

def K_fold_strat(data: list, length: int) -> None:

    sorted_data = data
    sorted_data.sort(key = lambda x: x[-1] , reverse=True)
    NB_accuracy_sum = 0
    KNN_accuracy_sum = [0]*5

    with open("pima-folds.csv", "w+") as o:
        for i in range(10):
            o.write("fold{}\n".format(i+1))

            training = []
            test = []
            for index in range(length):
                if index % 10 == i:
                    test.append(sorted_data[index])
                    strings = (str(item) for item in sorted_data[index])
                    s = ",".join(strings)
                    o.write(s + "\n")
                else:
                    training.append(sorted_data[index])
            o.write("\n")
            NB_accuracy_sum += NB(training , test, True)
            KNN_accuracy_sum[0] += KNN(1,training, test, True)
            KNN_accuracy_sum[1] += KNN(2,training, test, True)
            KNN_accuracy_sum[2] += KNN(3,training, test, True)
            KNN_accuracy_sum[3] += KNN(4,training, test, True)
            KNN_accuracy_sum[4] += KNN(5,training, test, True)

    with open("eval.txt", "w+") as f:
        f.write("Accuracies of our classifiers using 10-fold stratified CV on the \"pima.csv\" dataset is as follows:\n")
        f.write("Naive Bayes: {}\n".format(NB_accuracy_sum/10))
        f.write("1-Nearest-Neighbour: {}\n".format(KNN_accuracy_sum[0]/10))
        f.write("2-Nearest-Neighbour: {}\n".format(KNN_accuracy_sum[1]/10))
        f.write("3-Nearest-Neighbour: {}\n".format(KNN_accuracy_sum[2]/10))
        f.write("4-Nearest-Neighbour: {}\n".format(KNN_accuracy_sum[3]/10))
        f.write("5-Nearest-Neighbour: {}".format(KNN_accuracy_sum[4]/10))

def calc_pdf(x , mu, sig) -> float:
    result = 1.0/(sig*math.sqrt(2*math.pi)) * math.exp((-(x - mu)**2) / (2*sig**2)) 
    return result  
    
def NB(training_data: list, test: list, test_has_class: bool) -> float:
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

    num_correct = 0
    num_wrong = 0
    for t in test:
        resultYes = 1
        resultNo = 1
        for index in range(ncol - 1):
            resultYes *= calc_pdf(t[index], yes_means[index], yes_stddev[index])
            resultNo *= calc_pdf(t[index], no_means[index], no_stddev[index])
        resultYes *= pYes
        resultNo *= pNo

        #ONLY NEED TO COMPARE NUMERATOR
        if not (test_has_class):
            if resultYes >= resultNo:
                print("yes")
            else:
                print("no")
        else:
            if resultYes >= resultNo and t[-1] == "yes":
                num_correct += 1
            elif resultYes < resultNo and t[-1] == "no":
                num_correct += 1
            else:
                num_wrong += 1
    if not (test_has_class):
        return 0
    else:
        return (float) (num_correct / (num_wrong + num_correct))
     
def KNN(k: int, training_data: list, test_data: list, test_has_class: bool) -> float:
    #initialization
    ncol = len(training_data[0]) 


    num_correct = 0
    num_wrong = 0
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
        if not test_has_class:
            if num_yes >= num_no:
                print("yes")
            else:
                print("no")
        else:
            if num_yes >= num_no and test[-1] == "yes":
                num_correct += 1
            elif num_yes < num_no and test[-1] == "no":
                num_correct += 1
            else:
                num_wrong += 1
    if not test_has_class:
        return 0
    else:
        return (float) (num_correct / (num_wrong + num_correct))
        
def main(args: list) -> None:       

    if len(args) != 3 and len(args) != 1:
        print("Usage: MyClassifier.py <Path_to_training> <Path_to_test> <Algorithm Type>")
        sys.exit()


    if len(args) == 1:
        data = []

        with open(args[0]) as data_file:
            data_reader = csv.reader(data_file, delimiter = ",")
            ncol = len(next(data_reader))
            data_file.seek(0)

            counter = 0
            for row in data_reader:
                data_row = []
                for i in range(ncol-1):
                    data_row.append(float(row[i]))
                data_row.append(row[ncol-1])
                data.append(data_row)
                counter += 1
        K_fold_strat(data, counter)


    if len(args) == 3:
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
            NB(training_data , test_data, False)
            return


        #RUN KNN
        if "NN" in args[2]:
            k = int(args[2].replace("NN",""))
            KNN(k, training_data , test_data, False)
            return

if __name__ == "__main__":
    main(sys.argv[1:])