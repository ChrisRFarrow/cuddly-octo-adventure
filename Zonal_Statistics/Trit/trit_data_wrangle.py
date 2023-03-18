import pandas as pd
import numpy as np

# Variables Declaration Section 
input_file_1 = 'Trit_2020_check090622.csv'
input_file_2 = 'Trit_zonal_statistics.csv'
base_output_file = 'Python_data_processing_output/trit_Conc_Comparison.csv'
calc1_output_file = 'Python_data_processing_output/calc1_trit_Conc_Comparison.csv'
calc2_output_file = 'Python_data_processing_output/Trit_Final_Calc_Output.csv'
output_false_file = 'Python_data_processing_output/trit_FALSE_Conc_Values.csv'
conc_thres = 0.01
GT_OnePercent = 1
GT_TwoFivePercent = 2.5
GT_FivePercent = 5
GT_TenPercent = 10
GT_TwentyFivePercent = 25
GT_FiftyPercent = 50
colName = 'Percent_Diff'

# Two Data Frame declarations from two input files. These two will be merged into a single Data Frame.
# First Data Frame (Cell centroid values)
df1 = pd.read_csv(input_file_1)
# Second Data Frame (Zonal Statistics calculated from qGIS)
df2 = pd.read_csv(input_file_2)

# Merge the two dataframes.
df_merge = pd.merge(df1, df2, how='left', on=['I','J'])
# Remove rows without data in the listed columns, such as _count, _sum, etc.
df_merge = df_merge.dropna(subset=["_count","_sum","_mean","_median","_min","_max","_range"])
df_merge.to_csv(base_output_file, sep=',')

#Calculate the percent difference between 'Conc' (concentration) and the calculated '_mean' value.
df_merge['Percent_Diff'] = 100*(abs(df_merge['Conc']-df_merge['_mean']))/((df_merge['Conc'] + df_merge['_mean'])/2)
df_merge=df_merge[df_merge['Conc']>conc_thres]
# Output the Data Frame for general use, as needed.
df_merge.to_csv(calc1_output_file)

# Set the headers to be used for the percent values calculated below.
headers = ['Total Row Count', 'Count Over 1 Percent', 'Count Over 2.5 Percent', 'Count Over 5 Percent', 'Count Over 10 Percent','Count Over 25 Percent', 'Count Over 50 Percent']

# Calculate from the "Percent_Diff" column the number of cells over a specific percentage value.
column = df_merge[colName] # 
Percents = [] # List to store each percent value calculated.
Percents.append(len(df_merge.Percent_Diff)) # Total Row Count for Cell 0 in df_output_headers.
Percents.append(column[column > GT_OnePercent].count()) # Over 1 % for Cell 1 in df_output_headers.
Percents.append(column[column > GT_TwoFivePercent].count()) # Over 2.5 % for Cell 1 in df_output_headers.
Percents.append(column[column > GT_FivePercent].count()) # Over 5 % for Cell 1 in df_output_headers.
Percents.append(column[column > GT_TenPercent].count()) # Over 10 % for Cell 1 in df_output_headers.
Percents.append(column[column > GT_TwentyFivePercent].count()) # Over 25 % for Cell 1 in df_output_headers.
Percents.append(column[column > GT_FiftyPercent].count()) # Over 50 % for Cell 1 in df_output_headers.
# Create the Pandas Data Frame with the output data and the correct headers.
df_calcs = pd.DataFrame(Percents).transpose() # = output_headers)
df_calcs.columns = headers # Set the headers on the new Data Frame, df_calcs

# Output the new Data Frame to a CSV file.
df_calcs.to_csv(calc2_output_file)

# Output to the screen the final data frame
print(df_calcs)
