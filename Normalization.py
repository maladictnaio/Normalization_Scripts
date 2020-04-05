import pandas as pd
import glob

# global variables
merged = []  # epmty DataFrame to place normalized values into
i = 0  # iteration counter


def normalize(file):
    # import xye file
    df = pd.read_csv(file, sep='\s+', index_col=0, names=['2Theta', file, 'Error'])

    # remove Error column
    df = df.drop(columns=['Error'])

    # find min and max
    dfmin = df[file].min()
    dfmax = df[file].max()

    # normalize
    df[file] = (df[file] - dfmin) / (dfmax - dfmin)

    # export normalized data as CSV
    df.to_excel(file+" normalized.xlsx")

    return df


# Search for all xye files and pass them to normalize
xye_files = glob.glob('*.xye')

for var in xye_files:
    if xye_files.index(var) == 0:
        merged = normalize(var)
    else:
        # merges two DataFrames where they overlap in 2Theta. Outer puts NaN where the data does not overlap
        merged = pd.merge(merged, normalize(var), on=['2Theta'], how='outer')

# Sorts the 2theta into the correct order
merged = merged.sort_index()

# adds one to the normalized data to stack plots long the y axis
for column in merged:
    merged[column] = merged[column] + i
    i = i + 1

# exports the merged files to excel
merged.to_excel("normalized.xlsx")
