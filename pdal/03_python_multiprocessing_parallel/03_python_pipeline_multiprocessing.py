import json
import multiprocessing as mp
from pathlib import Path
import pdal
import os
import copy

def processFile(args):
    laz_file, pipeline_template = args

    laz_file = Path(laz_file)
    tif_file = Path(f"{laz_file.stem}.tif")

    # Copy pipeline and replace filenames
    pipeline = copy.deepcopy(pipeline_template)

    for stage in pipeline["pipeline"]:
        if stage["type"] == "readers.las":
            stage["filename"] = str(laz_file)

        elif stage["type"] == "writers.gdal":
            stage["filename"] = str(tif_file)

    #print(json.dumps(pipeline))
    p = pdal.Pipeline(json.dumps(pipeline))
    p.execute()

    return f"{laz_file} -> {tif_file}"


if __name__ == "__main__":

     # Read pipeline JSON
    with open("../pipeline.json") as f:
        pipeline_template = json.load(f)
        print(type(pipeline_template))
        print(pipeline_template)

    # Number of parallel PDAL processes
    workers = len(os.sched_getaffinity(0))

    # Read file list
    with open("../filelist.txt") as f:
        files = [
            line.strip()
            for line in f
            if line.strip()
        ]

    tasks = [
        (filename, pipeline_template)
        for filename in files
    ]

    with mp.Pool(processes=workers) as pool:
        for result in pool.map(processFile, tasks):
            print("Done:", result)