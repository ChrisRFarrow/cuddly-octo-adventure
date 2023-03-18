import pandas as pd
import numpy as np

input_file_1 = 'C14_2020_check090622.csv'
input_file_2 = 'c14_zonal_statistics.csv'
output_file = 'Python_data_processing_output/c14_Conc_Comparison.csv'
output_false_file = 'Python_data_processing_output/c14_FALSE_Conc_Values.csv'

# First dataframe (cell centroid values)
df1 = pd.read_csv(input_file_1)
#df1 = df1[df1['Conc']>10]
# #df1.plot(y='Conc')

# First dataframe (cell centroid values)
df2 = pd.read_csv(input_file_2)

# Merge two dataframes
df_merge = pd.merge(df1, df2, how='left', on=['I','J'])
# Remove rows without data in the listed columns, such as _count, _sum, etc.
df_merge = df_merge.dropna(subset=["_count","_sum","_mean","_median","_min","_max","_range"])

# Compare the 'Conc' column against the 'CELLACTIVE_y' column (both represent the concentration at I & J)
# while writing to a new column titled 'Comparison_Output'
#df_merge['Comparison_Output'] = np.where((df_merge['Conc'] > df_merge['CELLACTIVE_y']) or (df_merge['Conc'] < df_merge['CELLACTIVE_y']), df_merge['Conc'], '0')
# Check if all values are the same:
# print(df_merge['Conc'].equals(df_merge['CELLACTIVE_y']))
# Check which values are not the same, write to the 'df_merge' data frame
df_merge['Conc-_mean_Comparison_Output'] = np.where((df_merge['Conc']==df_merge['_mean']), "True", "False")
df_merge['Conc-_median_Comparison_Output'] = np.where((df_merge['Conc']==df_merge['_median']), "True", "False")
df_merge['Conc-_min_Comparison_Output'] = np.where((df_merge['Conc']==df_merge['_min']), "True", "False")
df_merge['Conc-_max_Comparison_Output'] = np.where((df_merge['Conc']==df_merge['_max']), "True", "False")
df_merge['Conc-_sum_Comparison_Output'] = np.where((df_merge['Conc']==df_merge['_sum']), "True", "False")
# Export the merged dataframe to a CSV file format.
df_merge.to_csv(output_file, sep=',')

# Create a new data frame for the rows that generated a "FALSE" in the 'Comparison_Output' column
df_FALSE = df_merge[df_merge.Comparison_Output == "False"]
df_FALSE.to_csv(output_false_file, sep=',')


# merged_df = pd.concat([df1, df2], ignore_index=True, sort=False)
# merged_df.to_csv('data_cleaning/cleaned_c14_data.csv', sep=',')
