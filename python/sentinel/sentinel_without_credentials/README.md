## Sentinel bucket content without AWS credentials

This is an example script of how to get contents from an open bucket without AWS credentials.

### Running 

On local machine install the required library: boto3

On Puhti, you can use the [geoconda module](https://docs.csc.fi/apps/geoconda/) which includes the boto3 library:
```
module load geoconda
python get_open_sentinel_buckets.py
```
### Results

The script prints out the first bucket's name, and the contents of the first 5 SAFEs in that bucket. The bucket's contents are accessible in the get_contents function.
