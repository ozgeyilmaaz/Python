import numpy as np
import pandas as pd
import time as tm

def two_opt(solution):
    soll = solution.copy()
    i = np.random.randint(0, len(soll)-3)
    j = np.random.randint(i+2, len(soll)-1)
    reversed_part = soll[i+1:j+1] # piece of solution will be reversed
    reverse = reversed_part[::-1] # reversed the piece of solution
    soll[i+1:j+1] = reverse # the space will be reversed filled with reversed solution piece
    return soll # solution returned

def city_swap(solution):
    soll = solution.copy() # main solution copied
    i,j = np.random.choice(len(soll), 2, replace=False) # 2 random different indixes selected
    soll[i], soll[j] = soll[j], soll[i] # cities swapped
    return soll

def evaluation(solution, distance_matrix):
    solution = np.append(solution, solution[0]) # first city number appended to last to end the tour
    distance = 0 
    for i, j in zip(solution[0:-1], solution[1:]): 
        distance += distance_matrix.loc[i, j] # distance will be cumulatively increase
    return distance

def initial_solution(indexes):
    num_of_cities = len(indexes) # number of cities
    sol = np.random.permutation(range(1, num_of_cities+1)) # random permutatiton with all city numbers 
    return sol # randomized slution returned

def calculate_distance(c1, c2): # This function will calculate distances with given city coordinates
    distance = (sum((c1 - c2)**2))**(1/2) # Ecledian distance
    return distance # function returned distance as a scalar number

def distance_matrix_function(df): # This function is creates a distance matrix with city indexes
    distance_matrix = pd.DataFrame(index=df.index, columns=df.index, dtype="float") # Data frame that n numbers of columns n number of rows, n is number of city in TSP
    for i in df.index:
        for j in df.index:
            if i == j:
                distance_matrix.loc[i, j] = np.inf # if i equals j, distance taken as an infinity to prevent picking this node
            else:
                coordinate_i = df.loc[i] # coordinate of city i
                coordinate_j = df.loc[j] # coordinate of city j
                distance = calculate_distance(coordinate_i, coordinate_j) # distance calculated with "calculate_distance" function
                distance_matrix.loc[i, j] = distance # distance of city i to city j set as a distance calculated in previous step 
    return distance_matrix

def simulated_annealing(coords_df, cooling_ratio, T, T_limit = 0.1, threshold=1, k=1, is_two_opt=True): 
    # City swap will always used however, optionally two opt improvment heuristic can be used too(it is closed as default)
    start = tm.time() # starting time recorded
    distance_matrix = distance_matrix_function(coords_df) # distance matrix of all cities gathered from "distance_matrix_function"
    sol = initial_solution(coords_df.index) # random initial solution gathered
    cost = evaluation(sol, distance_matrix) # cost of initial solution calculated in "evaluation" function  
    
    total_inner_it = 0
    total_outer_it = 0
    
    while T > T_limit: # As long as T greater than T_limit that specified at the start of the algorithm, it will iterate 
        # OUTER TERMINATION CONDITION 
        print("---------------------------------------------")
        print("TEMPERATURE: ",T,"\n")
        iteration = 0
        
        while True: # As long as it's not broken it will iterate INNER TERMINATION CONDITION
            iteration += 1 # to have the record of inner iteration number
            total_inner_it += 1
            
            new_sol_1 = city_swap(sol) # altered solution of city_swap
            new_sol_2 = two_opt(sol) # altered solution of two_opt
            
            new_cost_1 = evaluation(new_sol_1, distance_matrix) # cost of city_swap
            new_cost_2 = evaluation(new_sol_2, distance_matrix) # cost of two_opt   
            
            if is_two_opt == False:
                new_cost_2 = np.inf # if "is_two_opt" set as a False at the start of the algortihm cost of two_opt will be infinity
                
            both = pd.DataFrame([[new_sol_1, new_cost_1], [new_sol_2, new_cost_2]], index=["city_swap", "two_opt"], columns=["solution", "cost"])
            min_index = both["cost"].idxmin() # index of solution that has smallest cost 
            new_sol = both.loc[min_index, "solution"] # new solution set as a solution that has smallest cost
            new_cost = both.loc[min_index, "cost"] # smallest cost set as a new_cost
            
            print("Iteration: ", iteration, "|| Cost: ", cost)
            print("Iteration: ", iteration, "|| New cost: ", new_cost, "\n")
            
            difference = abs(cost - new_cost) # difference between new and old solution
            
            if difference <= threshold: # INNER TERMINATION CONDITION 
                break # if difference lower than threshold that we specified at the start of the algorithm, inner termination granted
                
            if new_cost < cost: # if cost of new solution is lower, it is accepeted
                sol = new_sol
                cost = new_cost
            else: # if cost of new solution is greater, it is accepeted if probability specified as "P" is greater than random number between (0,1)
                expo = ((cost - new_cost) / (k * T))
                P = np.exp(expo)
                if P >= np.random.random():
                    sol = new_sol
                    cost = new_cost
        
        total_outer_it += 1
        T *= (1 - cooling_ratio) # After each inner loop temperature cools down
    
    sol = np.append(sol, sol[0]) # first city appended to last in final solution
    total_time = tm.time() - start # total time of the algorithm gathered
    
    print("******************************************************************")
    print("EXECUTIVE SUMMARY \n")
    print("Total time spent: ", round(total_time, 2), "seconds")
    print("Final cost: ", round(cost, 2))
    print("Total inner iteration number: ", total_inner_it)
    print("Total outer iteration number: ", total_outer_it)
    print("\nFinal solution: ", sol)
    
    return sol, cost, total_time

df = pd.read_csv("Simulated_Annealing_Metaheuristic_Data.csv", index_col=0)

sol, cost, total_time = simulated_annealing(df, cooling_ratio=0.1, T=100, T_limit = 0.1, threshold=1, k=1, is_two_opt=True)