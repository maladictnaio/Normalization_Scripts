# need pandas, pathlib, openpyxl, mathplotlib modules
import pandas as pd
import glob
import matplotlib.pyplot as plt

# global variables
merged = []  # epmty DataFrame to place normalized values into
i = 0  # iteration counter

# custom variables
extension = '.csv'           
export_individual = True     
export_combined = False                        
normalize_data = False 
stack = True         

# graphing variables 
x_axis_label = '2Theta'
y_axis_label = 'y'
custom_x_axis = True
x_axis_start = 5
x_axis_end = 40

# import data function 
def read(file):
    
    # remove old file type from name
    filename = file
    filename = filename.rstrip(extension)

    
    if extension == ".xye":
        
        #specific step for .xye set and error column labeled
        df = pd.read_csv(file, sep='\s+', index_col=0, names=[x_axis_label, filename, 'Error'])
        
        # remove Error column
        df = df.drop(columns=['Error'])
    # normal import    
    else: df = pd.read_csv(file, index_col=0,names=[x_axis_label, filename])
    
    # removes y values of zero 
    df = df[(df != 0).all(1)]
    
    if normalize_data == True:
        df = normalize(df, filename)

    # export normalized data as xlsx (Excel)
    if export_individual == True:
        if normalize_data == True:
            df.to_excel(filename + ' normalized.xlsx')
        else: 
            df.to_excel(filename + '.xlsx') 

    return df

# normalization function
def normalize(data, filename): 
    # find min and max
    datamin = data[filename].min()
    datamax = data[filename].max()

    # normalize
    data[filename] = (data[filename] - datamin) / (datamax - datamin)
        
    return data 

# graphing function
def graph(graph):
    graph.plot()
    plt.xlabel(x_axis_label)
    plt.ylabel(y_axis_label)
    plt.legend( loc='center', ncol=4, bbox_to_anchor=(0.5, 1.05), shadow=False, frameon=False)
    if custom_x_axis == True:
        plt.xlim(x_axis_start,x_axis_end)


# Search for all .csv files and pass them to normalize
search_files = glob.glob('*' + extension)


for var in search_files: #itterates through all the file found in the search
    if search_files.index(var) == 0:
        merged = read(var) #inputs the first file into the merged DataFrame
    else:
        # merges two DataFrames where they overlap in x. Outer puts NaN where the data does not overlap
        merged = pd.merge(merged, read(var), on=[x_axis_label], how='outer')

# Sorts the x values into the correct order
merged = merged.sort_index()

#graphs the normalized data overlaping
graph(merged)

# adds one to the normalized data to stack plots along the y axis
if stack == True:
    for column in merged:
        merged[column] = merged[column] + i
        i = i + 1
    graph(merged)

# exports the merged files to excel
if export_combined == True:
    if normalize_data == True:
        merged.to_excel("combined normalized data.xlsx")
    else: 
        merged.to_excel("combined data set.xlsx")

#shows the two plots
plt.show()