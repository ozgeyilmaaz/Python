import pandas as pd
import numpy as np
import time as tm
import matplotlib.pyplot as plt

def first_plot(data, route):
    plt.figure(figsize=(15,8))
    plt.scatter(data["X"],data["Y"],color="g",label="$Cities$")
    for i in range(0,len(data["X"])):
        plt.annotate("C"+str(i+1),(data.iloc[i,0],data.iloc[i,1]))
    plt.xlabel("$X$ $Axis$")
    plt.ylabel("$Y$ $Axis$")
    plt.legend()
    return  plt.show()

def final_plot(data, route,total_cost,total_time):
    plt.figure(figsize=(15,8))
    plt.scatter(data["X"],data["Y"],color="g",label="$Cities$")
    for i in range(0,len(data["X"])):
        plt.annotate("C"+str(i+1),(data.iloc[i,0],data.iloc[i,1]))
    new_df = data.loc[route]    
    plt.plot(new_df["X"],new_df["Y"])
    plt.xlabel("$X$ $Axis$")
    plt.ylabel("$Y$ $Axis$")
    plt.legend()
    plt.ylim(0,70)
    plt.annotate("Total distance covered: "+str(total_cost)+ " unit",(24,7))
    plt.annotate("Total time passed: "+str(total_time)+" second",(24,3))  
    return plt.show()

def arc_cost(data, route):
    df = pd.DataFrame([["nan", "nan", "nan"]], columns = ["City 1", "City 2", "Cost"])
    for x in range(len(route)-1):
        cost = round(euclidean_distance(data, route[x], route[x+1]), 2)
        row_dict = {"City 1":route[x], "City 2":route[x+1],"Cost":cost}
        df = df.append(row_dict, ignore_index=True)
    df.drop([0], axis=0, inplace=True)
    return df

def totalcost(data, route):
    total_cost = 0
    for x in range(len(route)-1):
        total_cost += euclidean_distance(data, route[x], route[x+1])
    return total_cost

def insertion(data, k, route, cities):
    insertion_cost = np.inf
    for x in range(len(route)-1):
        insertion_calculation = euclidean_distance(data, route[x], k) + euclidean_distance(data, k, route[x+1]) - euclidean_distance(data, route[x], route[x+1])
        if insertion_calculation < insertion_cost:
            insertion_cost = insertion_calculation
            insertion_loc = x
    cities.insert(insertion_loc+1, k)
    route.insert(insertion_loc+1, k)

def finding_k(data, cities):
    k_distance = np.inf
    for a in cities:
        for b in range(1, len(data)+1):
            if b in cities:
                continue
            else:
                k_calculation = euclidean_distance(data, b, a)
                if k_calculation < k_distance:
                    k_distance = k_calculation
                    k = b
    return k

def euclidean_distance(data, city_1, city_2):
    return (sum((data.loc[city_1] - data.loc[city_2])**2))**0.5

def initializition(data):
    cities = []
    min_value = np.inf
    for idx, row in data.iterrows():
        for c in range(idx+1, len(data)+1):
            calculation = euclidean_distance(data, idx, c)
            if calculation < min_value:
                cities.clear()
                min_value = calculation
                cities.append(idx)
                cities.append(c)              
    route = cities.copy()
    route.append(route[0])
    return cities, route

def nearest_insertion(data):
    starting_time = tm.time()
    cities, route = initializition(data)
    for x in range(len(data)-2):
        k = finding_k(data, cities)
        insertion(data, k, route, cities)
    total_cost = totalcost(data, route)   
    total_time = tm.time() - starting_time
    arccosts = arc_cost(data, route)
    first_p = first_plot(data, route)
    final_p = final_plot(data, route, total_cost, total_time)
    return route, total_cost, total_time, first_p, final_p, arccosts

data = pd.read_csv("Nearest_Insertion_Heuristic_Data.csv", index_col=0)
route, total_cost, total_time, first_p, final_p, arccosts = nearest_insertion(data)

print("Route: ", route)
print("------------------------------")
print("Total Cost: ", total_cost)
print("------------------------------")
print("Total Time:", total_time)
print("------------------------------")
print(arccosts)