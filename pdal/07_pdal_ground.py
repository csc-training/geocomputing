# -*- coding: utf-8 -*-

from mpl_toolkits.mplot3d import Axes3D
from multiprocessing import Pool 
from pathlib import Path
import json
import matplotlib.pyplot as plt
import pandas as pd
import pdal
import time

#Location of .laz files, relative to the script
input_dir="data"

## How many parallel processes do we want to use
parallel_processes = 4

# Filter laz with SMRF and create Pandas dataframe with points in it.
def pdal2df(input_file):

    pipe = [
        input_file,
        {
            "type":"filters.smrf",
            "window":33,
            "slope":1.0,
            "threshold":0.15,
            "cell":1.0
        }
    ]

    pipeline = pdal.Pipeline(json.dumps(pipe))
    pipeline.validate() # check if our JSON and options were good
    pipeline.loglevel = 8 #really noisy
    count = pipeline.execute()
    arrays = pipeline.arrays
    arr = pipeline.arrays[0]
    description = arr.dtype.descr
    cols = [col for col, __ in description]
    df = pd.DataFrame({col: arr[col] for col in cols})
    
    return df

# Plot as 3D plot, green if ground red if not.
def plot_df(df, input_file):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    df = df.sample(frac=0.05)
    colors=['green' if c==2 else 'red' for c in df.Classification.tolist()]
    ax.scatter(df.X.tolist(),df.Y.tolist(),df.Z.tolist(), c=colors)
    plt.savefig(input_file.replace('laz','png'))

# Procesing steps for one file 
def process_laz(input_file):
    input_file = str(input_file)
    print(input_file)
    df = pdal2df(input_file)
    print(df)
    plot_df(df, input_file)
   
# Start the script find laz files in data folder and parallelize its processing   
def main():
    # Find laz files on local disk    
    file_list = Path(input_dir).rglob('*.laz')

    ## Create a pool of workers and run the function process_laz for each filepath in the list
    pool = Pool(parallel_processes)
    pool.map(process_laz, file_list)

if __name__ == '__main__':
    ## This part is the first to execute when script is ran. It times the execution time and rans the main function
    start = time.time()
    main()
    end = time.time()
    print("Script completed in " + str(end - start) + " seconds")