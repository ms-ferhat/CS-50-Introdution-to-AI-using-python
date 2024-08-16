import csv
import sys
import pandas

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    # print(evidence[0],labels[0])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    # print('model is \n')
    # print(model)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as f:
        data = csv.reader(f)
        next(data)
        evidence=[]
        label=[]
        mon=['Jan','Feb','Mar','Apr','May','June','Jul','Aug','Sep','Oct','Nov','Dec']
        for row in data:
            evidence.append(
                [
                    int(row[0]),float(row[1]),int(row[2]),float(row[3]),
                    int(row[4]),float(row[5]),float(row[6]),float(row[7]),
                    float(row[8]),float(row[9]),mon.index(row[10]),
                    int(row[11]),int(row[12]),int(row[13]),int(row[14]),
                    1 if row[15] == 'Returning_Visitor' else 0,
                    1 if row[16]=='TRUE' else 0
                ]
            )
            label.append(1 if row[17]=='TRUE' else 0)
            # t_list=[]
            # for cell in range(17):
            #     if cell < 10:
            #        t_list.append(float(row[cell]))
            #     elif cell == 10:
            #         t_list.append(float(mon.index(row[cell])))
            #     elif cell > 10 and cell < 15 :
            #         t_list.append(float(row[cell]))
            #     elif cell == 15:
            #         t_list.append(1 if row[cell] == 'Returning_Visitor' else 0)
            #     elif cell == 16:
            #         t_list.append(1 if row[cell]=='TRUE' else 0)
            #     else:
            #         label.append(1 if row[cell]=='TRUE' else 0)
            # evidence.append(t_list)
        print(evidence[0])
        print(label[0])
    return (evidence,label)
    
            




def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model=KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence,labels)
    return model



def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    TN,FP,FN,TP=confusion_matrix(labels,predictions).ravel()
    
    TPR=(TP)/(TP+FN)
    TNR=(TN)/(TN+FP)
    return (TPR,TNR)

    


if __name__ == "__main__":
    main()
