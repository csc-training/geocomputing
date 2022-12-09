### Sentinel bucket content without AWS credentials

This is an example script of how to get bucket contents from an open bucket without AWS credentials.

### Running 

On local machine install the required library: boto3

On Puhti, you can use the [geoconda module](https://docs.csc.fi/apps/geoconda/) which includes the boto3 library:
```
module load geoconda
python get_open_sentinel_buckets.py
```
