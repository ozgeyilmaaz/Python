import numpy as np
import pandas as pd

def p_y(y):
    p_y = []
    for i in np.sort(y.unique()):   
        pyi = len(y[y==i])/len(y)
        p_y.append(pyi)
    return p_y

def mean_sd_for_each_class(x, y):
    means = []
    sds = []
    p = x['x1'].corr(x['x2'])
    for i in np.sort(y.unique()):
        means_i=x[y==i].mean()
        means.append(means_i)
    sd_i = x.std()
    sds.append(sd_i)
    return means, sds, p

def calculateGaussianProbability(x, means, stdev, p):
    x1 = x['x1']
    x2 = x['x2']
    u1k = means[0]
    u2k = means[1]
    s1 = stdev[0][0]
    s2 = stdev[0][1]
    expo = np.exp(-(np.power(s2,2) * np.power((x1-u1k),2) + np.power(s1,2) * np.power((x2-u2k),2) - 2*p*s1*s2*(x1-u1k)*(x2-u2k)))
    return (1/(2*np.pi*s1*s2*np.sqrt(1-np.power(p,2)))) * expo

def calculateClassProbabilities(x,means,sds,class_probs, p):
    probabilities= []
    for k in range(len(class_probs)):
        mean_k = means[k]
        fxk = calculateGaussianProbability(x, mean_k, sds, p)
        probabilities.append(fxk)
    return (probabilities/np.sum(probabilities,axis=0))    

def predict(x, means, sds, class_probs, p):
    probabilities=calculateClassProbabilities(x,means,sds,class_probs, p)
    Class=(probabilities[0]<=0.5).astype('int')
    return Class

def compute_accuracy(prediction, y_test):
    return (1-np.sum(np.abs(prediction-y_test))/len(prediction))*100

def not_so_naive_bayes(train, test):
    
    x_train = train.drop('y', axis = 1)
    y_train = train['y']
    class_probs = p_y(y_train)
    means, sds, p = mean_sd_for_each_class(x_train, y_train)
    
    x_test = test.drop('y',axis=1)
    y_test = test['y']
    
    prediction = predict(x_test, means, sds, class_probs, p)
    accuracy = compute_accuracy(prediction, y_test)
    
    return accuracy, prediction

train = pd.read_csv('not_so_Naive_Bayes_train.csv')
test = pd.read_csv('not_so_Naive_Bayes_test.csv')

a, p = not_so_naive_bayes(train, test)

print("Accuracy: ", a)
print("Predict: ", p)