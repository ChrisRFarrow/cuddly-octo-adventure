# File developed to calculate count of specific count of concentraiton percentages differences 
# for a given concentration. This script has a function that is called to cycle through each directory 
# in the same directory as this Python script and to read in and output certain files.

# REQUIRED FILES WITHIN A CONTMAINANT FOLDER NAME:
# "{contaminant_name, such as C14}_2020_check090622.csv"
# "{contaminant_name, such as C14}_zonal_statistics.csv"
# IF THESE FILES NEED CHANGING SEE THE 'Variables Declaration Section' below.
# REQUIRED DIRECTORY INSIDE A CONTAMINANT FOLDER NAME:
# "Python_data_processing_output"

import pandas as pd
import numpy as np
import os

# Get the list of all directories in the directory where this python file is stored.
path = os.getcwd()
dir_list = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

# Create an empty CSV file to be used for information appending with each contaminant
with open('Contaminants_Calc_Output.csv', 'a') as creating_new_csv_file:
    pass

def contaminant_checking_calcs(directory_list):
    # Define the output Data Frame here, including the contaminant rows and column headings.
    # Set the headers to be used for the percent values calculated below.
    headers = ['Contaminant', 'Total Row Count', 'Count Over 1 Percent', 'Count Over 2.5 Percent', 'Count Over 5 Percent', 'Count Over 10 Percent','Count Over 25 Percent', 'Count Over 50 Percent']
    df_calcs = pd.DataFrame(data = None, columns = headers)
    df_calcs.to_csv('Contaminants_Calc_Output.csv', mode='w')

    for j in directory_list:
        # Variables Declaration Section 
        contaminant = f'{j}'
        input_file_1 = f'{contaminant}/{contaminant}_2020_check090622.csv'
        input_file_2 = f'{contaminant}/{contaminant}_zonal_statistics.csv'
        base_output_file = f'{path}/{contaminant}/Python_data_processing_output/{contaminant}_Conc_Comparison.csv'
        calc1_output_file = f'{path}/{contaminant}/Python_data_processing_output/calc1_{contaminant}_Conc_Comparison.csv'
        calc2_output_file = f'{path}/{contaminant}/Python_data_processing_output/{contaminant}_Final_Calc_Output.csv'
        conc_thres = 0.01
        GT_OnePercent = 1
        GT_TwoFivePercent = 2.5
        GT_FivePercent = 5
        GT_TenPercent = 10
        GT_TwentyFivePercent = 25
        GT_FiftyPercent = 50
        colName = 'Percent_Diff'

        # Get only the file names within a the current contaminant directory
        #print("\nOnly files:")
        #print([ name for name in os.listdir(contaminant) if not os.path.isdir(os.path.join(contaminant, name)) ])
        ([ name for name in os.listdir(contaminant) if not os.path.isdir(os.path.join(contaminant, name)) ])

        # Two Data Frame declarations from two input files. These two will be merged into a single Data Frame.
        # First Data Frame (Cell centroid values)
        df1 = pd.read_csv(input_file_1)
        # Second Data Frame (Zonal Statistics calculated from qGIS)
        df2 = pd.read_csv(input_file_2)

        # Merge the two dataframes.
        df_merge = pd.merge(df1, df2, how='left', on=['I','J'])
        # Remove rows without data in the listed columns, such as _count, _sum, etc.
        df_merge = df_merge.dropna(subset=["_count","_sum","_mean","_median","_min","_max","_range"])
        df_merge.to_csv(base_output_file)

        #Calculate the percent difference between 'Conc' (concentration) and the calculated '_mean' value.
        df_merge['Percent_Diff'] = 100*(abs(df_merge['Conc']-df_merge['_mean']))/((df_merge['Conc'] + df_merge['_mean'])/2)
        df_merge=df_merge[df_merge['Conc']>conc_thres]
        # Output the Data Frame for general use, as needed.
        df_merge.to_csv(calc1_output_file)

        # Calculate from the "Percent_Diff" column the number of cells over a specific percentage value.
        column = df_merge[colName] # 
        percents = [] # List to store each percent value calculated.
        percents.append(" ")
        percents.append(contaminant)
        percents.append(len(df_merge.Percent_Diff)) # Total Row Count for Cell 0 in df_output_headers.
        percents.append(column[column > GT_OnePercent].count()) # Over 1 % for Cell 1 in df_output_headers.
        percents.append(column[column > GT_TwoFivePercent].count()) # Over 2.5 % for Cell 1 in df_output_headers.
        percents.append(column[column > GT_FivePercent].count()) # Over 5 % for Cell 1 in df_output_headers.
        percents.append(column[column > GT_TenPercent].count()) # Over 10 % for Cell 1 in df_output_headers.
        percents.append(column[column > GT_TwentyFivePercent].count()) # Over 25 % for Cell 1 in df_output_headers.
        percents.append(column[column > GT_FiftyPercent].count()) # Over 50 % for Cell 1 in df_output_headers.
        # Create the Pandas Data Frame with the output data and the correct headers.
        df_percents = pd.DataFrame(percents).transpose() # Transpose the multiple row list into a single row, multiple column Data Frame.
        #df_percents.columns = headers
        df_percents.to_csv('Contaminants_Calc_Output.csv', mode='a', index=False, header=False)

        

# Initialize the for loop to run through each contaminant directory and perform the calcs.
contaminant_checking_calcs(dir_list)


