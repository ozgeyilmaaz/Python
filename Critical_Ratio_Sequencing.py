import numpy as np 
import pandas as pd

def critical_ratio(df_jobs):
    
    df_jobs["Critical Ratio"] = np.nan
    sequence = np.full_like(df_jobs.index, np.nan)
    days_passed = 0
    
    for i in range(len(df_jobs)):
    
        for idx, row in df_jobs.iterrows():
            df_jobs.loc[idx, "Critical Ratio"] = (df_jobs.loc[idx, "Due Date"] - days_passed) / df_jobs.loc[idx, "Processing Time"]
        
        sequence[i] = df_jobs["Critical Ratio"].idxmin()
        days_passed += df_jobs.loc[sequence[i], "Processing Time"]
        df_jobs = df_jobs.drop(sequence[i])
        
    return sequence.tolist()

jobs = pd.read_excel("./Critical_Ratio_Sequencing_Data.xlsx", index_col=0)

print(critical_ratio(jobs))