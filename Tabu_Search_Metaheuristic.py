import numpy as np
import pandas as pd
from scipy.optimize import linprog
import time as tm

cost_list = [[83.16, 122.22, 82.62, 133.50, 81.81, 65.70, 52.89],
          [97.20, 98.28, 75.48, 147.00, 40.50, 70.20, 110.94],
          [123.84, 99.12, 76.16, 130.00, 79.92, 38.40, 101.48],
          [75.60, 123.48, 42.84, 195.00, 72.90, 88.20, 59.34],
          [139.32, 107.10, 78.54, 121.50, 36.45, 65.70, 99.33],
          [83.88, 92.82, 124.10, 134.50, 75.87, 69.90, 48.59]]

cost = pd.DataFrame(cost_list, index = range(1,7), columns = range(1,8)) # cost(i,j) - data frame

demands = pd.Series([36, 42, 34, 50, 27, 30, 43], index = range(1,8)) # demand(j) - series

capacity = pd.Series([80, 90, 110, 120, 100, 120], index = range(1,7)) # capacity(i) - series

fixed_cost = pd.Series([220, 240, 260, 275, 240, 230], index = range(1,7)) # cost(i) - series

def simplex_algorithm(open_facilities): # The function that simplex solution is performed
    # Data frame that has number of opened facility rows and number of demand points columns
    x_ij_ = pd.DataFrame(np.zeros((len(open_facilities) , len(demands))) , index = open_facilities , columns= demands.index) 
    
    obj_func_coeff = cost.loc[open_facilities].values.flatten() 
    
    capacity_cons_full = [] # Empty list of capacity constraint, constarints will be added in for loop
    for i in open_facilities:
        capacity_cons_left = x_ij_.copy() # All x's are taken
        capacity_cons_left.loc[i,:] = demands # Capacity coefficients put into necessary locations
        capacity_cons_left = capacity_cons_left.values.flatten() # Flattend to get 1D array
        capacity_cons_full.append(capacity_cons_left) # Appended to full capacity constraint
        
    capacity_cons_right_side = capacity[open_facilities].values # Capacities of opened facilities
    
    demand_cons_full = [] # Empty list of demand constraint, constarints will be added in for loop
    for i in demands.index: # It will iterate 7 times = number of demand point because there are 7 demand constraints for each of demand points 
        demand_cons_left = x_ij_.copy() # All x's are taken
        demand_cons_left[i] = 1 # All demand coefficients put into necessary locations (they all taken as a 1)
        demand_cons_left = demand_cons_left.values.flatten() # Flattend to get 1D array
        demand_cons_full.append(demand_cons_left) # Appended to full demand constraint
                        
    demand_cons_right = np.ones(len(demands)) # Weights of demand points which must be equal to 1 
    
    bounds = (0, None) # Xij bounds -> [0 , infinity]
                               
    result = linprog(obj_func_coeff, # Objective function coefficients 
                  A_ub=capacity_cons_full, b_ub=capacity_cons_right_side,  # Inequalty constraints
                  A_eq=demand_cons_full , b_eq=demand_cons_right, # Equalty constraints
                  method='revised simplex',bounds=bounds) 
    
    objective_value = result.fun + fixed_cost[open_facilities].sum() 
    
    xijs = result.x 
    xij_from_simplex = pd.DataFrame(np.zeros((len(capacity) , len(demands))) , index = capacity.index , columns= range(1,8)) 
    xij_from_simplex.loc[open_facilities] = xijs.reshape((len(open_facilities) , len(demands))) 
    xij_from_simplex = xij_from_simplex.round(3) 
    
    return objective_value, xij_from_simplex
    
def tabu_search(open_facilities, feasible_set, tabu_list): # With add/drop, neighbors will created and for each of them, cost will be calculated
    tabu_df = pd.DataFrame(columns = ["Closed Facility", "Opened Facility", "Cost", "x_ij"])
    for x in open_facilities: # With this for loop, we try to close each facility that in open_facilities and
        for y in feasible_set: # instead of the facility that is closed from the open_facility list, every facility in the feasible set is tried to be opened 
            copy = open_facilities.copy()
            copy.remove(x) # The closed facility is removed from the list
            copy.append(y) # The opened facility is added to the list
            copy.sort() 
            if capacity.loc[copy].sum() >= demands.sum(): # If the total capacity of the open facilities meets the total demand
                cost, x_ij = simplex_algorithm(copy) # simplex calculation is made
                row_dict = {} # A dictionary is created to hold closed and opened facility information, cost and table values
                row_dict["Closed Facility"] = x
                row_dict["Opened Facility"] = y
                row_dict["Cost"] = cost
                row_dict["x_ij"] = x_ij
                tabu_df = tabu_df.append(row_dict, ignore_index=True) # This dictionary line is saved in the dataframe
            
    row_index = tabu_df["Cost"].idxmin() # The index number with the minimum cost is taken
    # Then, the closed and opened facilities, cost and table values with that index are taken from the locations
    closed = tabu_df.loc[row_index, "Closed Facility"]
    opened = tabu_df.loc[row_index, "Opened Facility"]
    cost = tabu_df.loc[row_index, "Cost"]
    x_ij = tabu_df.loc[row_index, "x_ij"]
    
    tabu_list.append(closed) # The number of the closed facility is appended to the tabu list
    open_facilities.remove(closed) # The closed facility is removed from the opened_facility list
    open_facilities.append(opened) # The newly opened facility is added to the opened_facility list 
    
    return cost, open_facilities, x_ij

def initialization(): # The function that we created randomly order at the beginning
    order = np.random.permutation(range(1, len(capacity)+1)) # Order is randomly generated
    q = 0 # The variable that holds our capacities as the facilities opens
    total_demand = demands.sum() # The variable that holds the total demand
    open_facilities = [] # The list that holds the opened facilities
    
    for x in order: 
        if q < total_demand: # The facility continues to be opened until the capacity meets the demand
            open_facilities.append(x) 
            q += capacity[x]   
        else: 
            break 
    
    open_facilities.sort() # Since the simplex algorithm works as sorted, the list is sorted
     
    return open_facilities 
    
def main(list_size): # The main function that the tabu search algorithm starts
    start = tm.time()
    open_facilities = initialization() # Initial random open facilities creation
    s, x_ij = simplex_algorithm(open_facilities) # Calculation of the initial cost (s) and table of the opened facilities
    tabu_list = []
    current_best = s
    iteration = 0
    
    print("---------------------------------------")
    print("Initial")
    print("Open facilities: ", open_facilities)
    print("s: ", s)
    print()
    print("x_ij Table")
    print(x_ij)
    
    while True:
        iteration += 1
        
        closed_facilities = []
        for i in capacity.index: # capacity.index: (1, 2, 3, 4, 5, 6) which it is also facility numbers
            if i not in open_facilities: # if facility with number i not in open_facilities list,
                closed_facilities.append(i) # it is the closed facility. So we append it to the closed_facilites list
        
        feasible_set=[] # List of closed facilities not included in the taboo list
        
        for x in closed_facilities:
            if x not in tabu_list: # If x is not in the tabu list,
                feasible_set.append(x) # we append it to the feasible_set list
              
        print("---------------------------------------")
        print("Iteration ", iteration)   
        print("Open facilities: ", open_facilities)
        print("Closed Facilities: ", closed_facilities)
        print("Tabu List: ", tabu_list)
        print("Feasible Set: ", feasible_set)
        print("Current Best: ", current_best)
              
        s_new, open_facilities, x_ij = tabu_search(open_facilities, feasible_set, tabu_list)
        
        print("s_new: ", s_new)
        print()
        print("x_ij Table")
        print(x_ij)
        
        s = s_new
        
        if len(tabu_list) > list_size: # If length of tabu_list is greater than list_size given as parameter,
            tabu_list.pop(0) # the value of the tabu_list at index 0 (i.e. the oldest tabu) is deleted
        # So the lifetime of a tabu here is the length of the tabu list.
        
        if s == current_best: # Stopping criterion: As long as s is different from current_best, the loop continues
            break
        
        if s < current_best: # If s is less than current_best (ie, if cost is better)
            current_best = s # current_best will be s.
            
    total_time = tm.time() - start
    
    return open_facilities, current_best, x_ij, total_time

open_facilities, current_best, x_ij, total_time = main(list_size = 2)
print("---------------------------------------")
print("Total Time: ", total_time)
print("Open facilities: ", open_facilities)