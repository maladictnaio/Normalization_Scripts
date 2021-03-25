#preset script for the processing of .csv files
import pandas as pd
import glob
import matplotlib.pyplot as plt

# global variables
merged = []  # epmty DataFrame to place normalized values into
i = 0  # iteration counter

# custom variables
extension = '.xlsx'                 

# import data function 
def read(file):
    
    # remove old file type from name
    filename = file
    filename = filename.rstrip(extension)

    # import .csv file
    df = pd.read_excel(file)

    return df

# Search for all .csv files and pass them to normalize
files = glob.glob('*' + extension)

for var in files: #itterates through all the file found in the search
    if files.index(var) == 0:
        merged = read(var) #inputs the first file into the merged DataFrame
    else:
        # merges two DataFrames where they overlap in x. Outer puts NaN where the data does not overlap
        merged = pd.merge(merged, read(var), on=[x_axis_label], how='outer')

merged.to_excel("combined data set.xlsx")