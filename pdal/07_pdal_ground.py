# -*- coding: utf-8 -*-
import pdal
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def pdal2df(pipelineJson):
    """
    Feed me a JSON pipeline, get back a Pandas dataframe with points in it.
    """
    pipeline = pdal.Pipeline(pipelineJson)
    pipeline.validate() # check if our JSON and options were good
    pipeline.loglevel = 8 #really noisy
    count = pipeline.execute()
    arrays = pipeline.arrays
    arr = pipeline.arrays[0]
    description = arr.dtype.descr
    cols = [col for col, __ in description]
    df = pd.DataFrame({col: arr[col] for col in cols})
    
    return df
	

input_file="data/part_00.laz"

pipe_json="""
[
    "data/part_00.laz",
    {
        "type":"filters.smrf",
        "window":33,
        "slope":1.0,
        "threshold":0.15,
        "cell":1.0
    }
]
"""

df = pdal2df(pipe_json)
print(df)

#Plot as 3d plot, green if ground red if not.
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
df = df.sample(frac=0.05)
colors=['green' if c==2 else 'red' for c in df.Classification.tolist()]
ax.scatter(df.X.tolist(),df.Y.tolist(),df.Z.tolist(), c=colors)
plt.savefig(input_file.replace('laz','png'))


