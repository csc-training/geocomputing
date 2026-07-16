## Allas Sentinel bucket content without AWS credentials

This is an example script of how to get contents from public buckets in Allas containing Sentinel-2 data (without credentials).

### Running 

On CSC's supercomputer Roihu, you can use the [python-geo module](https://docs.csc.fi/apps/python-geo/) which includes the boto3 library:
```
module load python-geo
python get_open_sentinel_buckets.py
```

On local machine install the required library: boto3

```
pip install boto3
```


### Results

The script prints out the first bucket's name, and the contents of the first 5 SAFEs in that bucket. The bucket's contents are accessible in the get_contents function.
The image URLs could also be used directly with e.g. `rasterio` package.
