# fast, once click scripts that normalize, combine and plot a range of data files
# files must all have the same independent variable (x values) and be in the same folder

# imoprt modules
import pandas as pd
import glob
import matplotlib.pyplot as plt

# global variables
merged = []  # epmty DataFrame to place normalized values into
i = 0  # iteration counter

# custom variables
extension = '.csv'                           # file type to process
ind_var = '2Theta'                           # name of indipendent variable all data have in common

# custom settings                
normalize_data = False       # normalizes data (True or False)
graph_data = True            # graphs the processed data (True or False)

# graphing variables 
x_axis_label = ind_var       # sets the x-axis label to the independent variable defined
y_axis_label = 'y'           # label for y-axis  
custom_x_axis = True         # use custom range for x-axis (True or False)
x_axis_min = 5               # min custom x value
x_axis_max = 40              # max custom x value 
stack = True                 # stacks the plotted data (True or False)

# import function, returnes the processed individual file as df
def read(file):
    
    # remove file extension from name
    filename = file
    filename = filename.rstrip(extension)

    # specific import procedures based on specified file type
    # check for .xye file type
    if extension == '.xye':
        
        #specific step for .xye set and error column labeled
        df = pd.read_csv(file, sep='\s+', index_col=0, names=[ind_var, filename, 'Error'])
        
        # remove Error column
        df = df.drop(columns=['Error'])
    
    # check for .xlsx file type (Excel). File is expected not to have labels in first row
    elif extension == '.xlsx':
        df = pd.read_excel(file, index_col=0,names=[ind_var, filename])
    
    # normal import    
    else: df = pd.read_csv(file, index_col=0,names=[ind_var, filename])
    
    # removes y values of zero 
    df = df[(df != 0).all(1)]
    
    # call normalize function
    if normalize_data == True:
        df = normalize(df, filename)

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
        plt.xlim(x_axis_min,x_axis_max)


# search for all files of specified type
search_files = glob.glob('*' + extension)

# reads all the files found and merges them into a single DataFrame
for var in search_files: # itterates through all the file found in the search
    if search_files.index(var) == 0:
        # passes first file to read function and then sets merged to the resulting df
        merged = read(var) 
    else:
        # merges two DataFrames. Values are merged on the specified indipendant variable  
        # outer puts NaN where the data does not overlap
        merged = pd.merge(merged, read(var), on=[ind_var], how='outer')

# Sorts the independent variable values into the correct order
merged = merged.sort_index()

#graphs the overlaping normalized data 
graph(merged)

# adds one to the normalized data to stack plots along the y axis
if stack == True:
    for column in merged:
        merged[column] = merged[column] + i
        i = i + 1
    graph(merged)

# shows the plots
if graph_data == True:
    plt.show()