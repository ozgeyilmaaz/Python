import numpy as np
import pandas as pd

def standardize(X):
    return (X - X.mean())/X.std(), X.mean(), X.std()

def predict(X,beta0,beta1):
    y = 1/(1+np.exp(-(beta0+beta1*X)))
    return y 

def gradient(X,y,beta0,beta1):
    grad_beta0 = (-1/len(X))*np.sum((y*np.exp(-beta0-beta1*X)+y-1)/(1+np.exp(-beta0-beta1*X)))
    grad_beta1 = (-1/len(X))*np.sum(X*(y*np.exp(-beta0-beta1*X)+y-1)/(1+np.exp(-beta0-beta1*X))) 
    return grad_beta0, grad_beta1

def update_param(beta0,beta1,grad_beta0,grad_beta1,alpha):
    beta0_new=beta0-alpha*grad_beta0
    beta1_new=beta1-alpha*grad_beta1
    return beta0_new,beta1_new

def gradient_descent(data,num_iter,alpha,random_seed):
    X=np.array(data['X'])
    y=np.array(data['y'])
    X,muX,sdX=standardize(X)
    np.random.seed(random_seed)
    beta0=np.random.rand()
    beta1=np.random.rand()
    J_list=[]
    for i in range(num_iter):
        ypred=predict(X,beta0,beta1)
        J=(-1/len(X))*np.sum(y*np.log(ypred)+(1-y)*np.log(1-ypred))
        J_list.append(J)
        grad_beta0,grad_beta1=gradient(X,y,beta0,beta1)
        beta0,beta1=update_param(beta0,beta1,grad_beta0,grad_beta1,alpha)
    
    return J_list,beta0,beta1

data = pd.read_csv('Logistic_Regression_Data.csv')
J, beta0, beta1 = gradient_descent(data, num_iter = 50000, alpha = 0.01, random_seed = 42)

print("Beta0: ", beta0)
print("Beta1", beta1)