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

lambdas = [0, 0, 0, 0, 0, 0, 0]
#lambdass = [0]*7
epsilon = 0.13
alpha = 0.5

def updating_lambdas(LB , UB , alpha, lambdas , full_x_values):
    new_lambdas = [0]*7 # 
    full_x_values_copy = full_x_values.copy() # xij values from knapsack problem
    s_j = (full_x_values_copy.sum(axis=0) - 1) # sub gradient for every demand points
    
    beta = alpha * (UB - LB) / (s_j**2).sum() # scalar value beta that will used while updating lambdas
    
    new_lambdas = lambdas + beta * s_j # lambdas updated
    
    return new_lambdas # new lambdas returned

def simplex_algorithm(open_facilities):
    # Data frame that has number of opened facility rows and number of demand points columns
    x_ij_ = pd.DataFrame(np.zeros((len(open_facilities) , len(demands))) , index = open_facilities , columns= demands.index) 
    
    obj_func_coeff = cost.loc[open_facilities].values.flatten() # 
    
    capacity_cons_full = [] # empty list of capacity constraint, constarints will be added in for loop
    for i in open_facilities:
        capacity_cons_left = x_ij_.copy() # all x's are taken
        capacity_cons_left.loc[i,:] = demands # capacity coefficients put into necessary locations
        capacity_cons_left = capacity_cons_left.values.flatten() # flattend to get 1D array
        capacity_cons_full.append(capacity_cons_left) # appended to full capacity constraint
        
    capacity_cons_right_side = capacity[open_facilities].values # capacities of opened facilities
    
    demand_cons_full = [] # empty list of demand constraint, constarints will be added in for loop
    for i in demands.index: # it will iterate 7 times = number of demand point because there are 7 demand constraints for each of demand points 
        demand_cons_left = x_ij_.copy() # all x's are taken
        demand_cons_left[i] = 1 # all demand coefficients put into necessary locations (they all taken as a 1)
        demand_cons_left = demand_cons_left.values.flatten() # flattend to get 1D array
        demand_cons_full.append(demand_cons_left) # appended to full demand constraint
                        
    demand_cons_right = np.ones(len(demands)) # weights of demand points which must be equal to 1 
    
    bounds = (0, None) # Xij bounds -> [0 , infinity]
                               
    result = linprog(obj_func_coeff, # objective function coefficients 
                  A_ub=capacity_cons_full, b_ub=capacity_cons_right_side,  # inequalty constraints
                  A_eq=demand_cons_full , b_eq=demand_cons_right, # equalty constraints
                  method='revised simplex',bounds=bounds) 
    
    return result # result of simplex algorithm returned

def UB_CPL(lambdas, LB_cpl_order):
    q = 0 # q as a current capacity, set to 0 at first. As facilities open, the capacity of facilities will be added to q
    total_demand = demands.sum() # total demand of the demand points
    open_facilities = [] # empty list that will kepp the record of opened facilities. It will be uptaded
    
    for x in LB_cpl_order: # we will decide which facility to open in the order of "LB_cpl_order"
        if q < total_demand: # check if total supply with opened facilities meets total demand 
            open_facilities.append(x) # index of opened facility will be appended to "open_facilities" list
            q += capacity[x] # add opened facilitiy's capacity to total supply   
        else: 
            break # if supply meets demand break the for loop
    
    open_facilities.sort() # sort the opened faciites
    
    result = simplex_algorithm(open_facilities) # Result of simplex algorthm 
    objective_value = result.fun + fixed_cost[open_facilities].sum() # Objective value (Z value) of simplex algorithm plus fixed cost of opened facilities are set as a objective value
    
    xijs = result.x # Xij values of opened facilities
    xij_from_simplex = pd.DataFrame(np.zeros((len(capacity) , len(demands))) , index = capacity.index , columns= range(1,8)) # dataframe of all Xij's
    xij_from_simplex.loc[open_facilities] = xijs.reshape((len(open_facilities) , len(demands))) # dataframe Xij values for opened facilities will be replaced with the values found in simplex
    xij_from_simplex = xij_from_simplex.round(3) # xij values will be rounded to 3 decimals to be able to read easily
    return objective_value , xij_from_simplex ,open_facilities # as a return; objective value (Z value), Xij values from simplex, and opened facilities list taken

def LB_CPL(lambdas):
    coeff = cost + lambdas # lambdas added into cost function
    LB_cpl = 0 # LB_cpl set to 0 at start
    LB_cpl_series = pd.Series(dtype ='float64') # Series that will keep the record of in index of the facility's and their caltulated Lower Bounds (LBcpl)
    
    full_x_values = pd.DataFrame(np.zeros((len(capacity) , len(demands))) , index = capacity.index , columns= range(1,8)) # a dataframe that has 6 columns and 7 columns like Xij table, every value is equal 0 at first
    
    # -KNAPSACK ALGORITHM- 
    for i in capacity.index: # for every facility i it will iterate 
        current_coeff = coeff.loc[i] # facility i's cost coefficients
        sub_ratio = (current_coeff / demands).sort_values() # ratios ordered from small to large 
        knapsack_order = sub_ratio.index # indexes of ordered ratios are taken
        capacity_i = capacity[i] # capacity for i th facility 
        x_values = pd.Series([0] * 7, index = range(1, 8), dtype ='float64') # Series of facility (x(1,1),x(1,2), ... ) , all 0 at first
        
        for j in knapsack_order: # for every demand point j in the order of "knapsack_order" it will iterate 
            demand_j = demands[j] # demand of j th demand point 
    
            x = min(1, capacity_i/demand_j) # min of (1 , ratio) taken as x
            
            if capacity_i >= demand_j: # if capacity greater than demand, take it as a 1 and substract the demand
                capacity_i -= demand_j 
            else:
                capacity_i = 0 # if capacity smaller than demand, take it as a zero because it will finish after current supply
                
            x_values[j] = x # x for the ith facility to jth demand point equals current "x"       
            
        LB_cpl_i = (current_coeff * x_values).sum() + fixed_cost[i] # (facility i's cost coefficients X found x values) + fixed cost of facility i
        # it will equal to facility's lower bound
        
        if LB_cpl_i > 0: 
            x_values[:] = np.zeros(7) # facility i's lower bound greater than 0, take lower bound as a 0 and make every "x_values" 0
            LB_cpl_i = 0
        
        full_x_values.loc[i] = x_values # Founded X values of ith facility will go into the dataframe that we have created at the start of the function ("full_x_values")
                        
        LB_cpl += LB_cpl_i # lower bound of facility i (LB_cpl_i) will be added with it self (it was set 0 at start of the function)
        LB_cpl_series.loc[i] = LB_cpl_i
        
    LB_cpl = LB_cpl - sum(lambdas) # sum of lambdas substracted from total lower bound 
    return LB_cpl , LB_cpl_series.sort_values(axis=0).index , full_x_values # as a return; lower bound, indexes of sorted lower bound, and "full_x_values" taken

def lagrangian(epsilon, alpha, lambdas):
    first_lambdas = lambdas
    start = tm.time()
    LB = 0.000000000000001 # at first, lower bound set to negative infinity
    UB = 10000000000000000 # at first, upper bound set to positive infinity
    h = 0 # to record the iteration number
    while ((UB-LB)/LB > epsilon): # as long as the (UB-LB)/LB > epsilon , algortihm will keep iterate
        LB_cpl, LB_cpl_order, full_x_values = LB_CPL(lambdas)
        UB_cpl,xij_from_simplex,opened_facilities = UB_CPL(lambdas, LB_cpl_order)
        
        if LB_cpl > LB:
            LB = LB_cpl # old lower bound set to current lower bound if current lb is greater than old lb
        
        if UB_cpl < UB:
            UB = UB_cpl # old upper bound set to current upper bound if current ub is greater than old ub
        
        lambdas = updating_lambdas(LB , UB , alpha , lambdas , full_x_values) # alpha is tolerance value
        h += 1
        
        print("Iteration number: ",h)
        print("UP: ",UB)
        print("LB: ",LB)
        print("--------------------------------------------------------")
    
    total_time = tm.time() - start
    print("EXECUTIVE SUMMARY\n")
    print("Epsilon: ",epsilon)
    print("Alpha: ",alpha)
    print("First lambdas: ",first_lambdas)
    print("Last lambdas: ",lambdas.values.round(2))
    print("Total iteration number: ",h)
    print("Total time passed: ",round(total_time,2),"second")
    print("Final UB (Objective Value): ",UB)
    print("Final LB: ",LB)

    print("--------------------------------------------------------")
    print("           FINAL Xij TABLE")
    print(xij_from_simplex)
    return LB,UB,h,lambdas,xij_from_simplex
LB,UB,h,lambdas,final_xij_table = lagrangian(epsilon, alpha , lambdas)