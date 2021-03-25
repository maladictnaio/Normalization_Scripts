#creates a new excel file from the data in the specified file type 
import pandas as pd
import glob


extension = '.xye'     # extension of the file type to be converted to Excel
ind_var = 'x'          # label for independent variable

def excel_convert(file):

    # remove file extension from name
    filename = file
    filename = filename.rstrip(extension)
    
    # specific import procedures based on specified file type
    
    if extension == '.xye': 
        # import .xye file type and label
        df = pd.read_csv(file, sep='\s+', index_col=0, names=[ind_var, file, 'Error'])
        
        # remove Error column
        df = df.drop(columns=['Error'])
    else:  
        # import other file types and label
        df = pd.read_csv(file, index_col=0, names=[ind_var, file])
    
    # removes y values of zero 
    df = df[(df != 0).all(1)]

    # export excel file
    df.to_excel(filename+".xlsx")

# search for all files of specified file type
xye_files = glob.glob('*' + extension)

# convert all files found to .xlxs (Excel)
for var in xye_files:
    excel_convert(var)




