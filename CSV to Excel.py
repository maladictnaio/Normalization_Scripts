import pandas as pd
import glob

# extension of the file type to be converted to Excel
extension = '.csv' 

def excel_convert(file):
    # import .csv file
    df = pd.read_csv(file, index_col=0, names=['x', file,])

    # remove old file type from name
    filename = file
    filename = filename.rstrip(extension)
    
    # export excel file
    df.to_excel(filename+".xlsx")

# search for all csv files
xye_files = glob.glob('*' + extension)

# convert all files found 
for var in xye_files:
    excel_convert(var)




