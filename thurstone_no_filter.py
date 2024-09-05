# for pip, use py -m pip (command here)

# Created by Andrew Glen Scutt

import pandas as pd
import numpy as np
import scipy.stats as st
from transformers import pipeline
import math

# Steps:
# 1. Convert Qualtrics data into table
# 2. Perform operations on this table to get scale values
# 3. Use pandas
# 4. Get z-score library
# 5. Need to reject data that does not meet the attention check and whether or not data is allowed to be used in the study or (no prolific id ??? check with norman if this is true)

def get_column_name_from_index(df, index):
    if 0 <= index < len(df.columns):
        return df.columns[index]
    else:
        raise IndexError("Column index out of range")

def create_global_preference_list(y1, x1, x2, dataframe, num_rows):
    temp_list = []
    global_preference_list = []

    for j in range(y1,num_rows + y1):
        if j:
            for i in range(x1, x2 + 1):
                temp_list.append(dataframe.at[j,get_column_name_from_index(dataframe,i)])
            global_preference_list.append(temp_list)
            temp_list=[]
    return global_preference_list

def create_preference_matrix():
    items = int(input("Please input the number of items that the participants must rank: "))
    contents = []
    rows = []
    cols = []
    k = 0 

    for i in range(items):
        rows.append(str(i))
        cols.append(str(i))
        sub_contents = []
        for j in range(items):
            if j == k:
                sub_contents.append("imp")
            else:
                sub_contents.append(0)
        contents.append(sub_contents)
        k = k + 1
    matrix = pd.DataFrame(np.array(contents), index = rows, columns = cols)
    return matrix, items


# 1. Convert Qualtrics data into table

path = "ANDREW_RANKING3.csv"

data = pd.read_csv(path)

# End converting Qualtrics data into table


# 2. Organize choices

sets_of_ranks = int(input("Please input the number of rank sets: ")) 
y1 = int(input("Please input the number of the highest row minus two that contains a rank value of interest: "))
x1 = int(data.columns.get_loc(str(input("Please input the name of the column that contains the leftmost rank value of interest: "))))
x2 = int(data.columns.get_loc(str(input("Please input the name of the column that contains the rightmost rank value of interest: "))))
rows = int(input("Please input the number of rows: "))

for k in range(sets_of_ranks):
    global_preference_list = create_global_preference_list(y1, x1, x2, data, rows)

num_of_people = len(global_preference_list)

preference_matrix, items = create_preference_matrix()

# End organizing choices


# 3. Fit choices into matrix + compute z-scores

for i in range(num_of_people):
    individual_choices = global_preference_list[i]
    for r in range(items):
        for l in range(items):
            if r != l:
                if individual_choices[r] < individual_choices[l]:
                    preference_matrix.at[str(r), str(l)] = float(preference_matrix.at[str(r), str(l)]) + 1

print(preference_matrix)

for r in range(items):
    for l in range(items):
        if r != l:
            preference_matrix.at[str(r), str(l)] = st.norm.ppf(float(preference_matrix.at[str(r), str(l)]) / num_of_people)

print(preference_matrix)

z_score_list = []

for r in range(items):
    average = 0
    for l in range(items):
        if r != l:
            average = preference_matrix.at[str(l), str(r)] + average
    z_score_list.append(average / (items - 1))

# End fitting choices into dataframe + computing z-scores

print(z_score_list)


# 4. Compute scale

scale_list = []

smallest_value = min(z_score_list)

for p in range(items):
   scale_list.append(z_score_list[p] - smallest_value)

print(scale_list)

# End computing scale