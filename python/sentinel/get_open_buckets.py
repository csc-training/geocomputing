"""
An example script for retrieving Sentinel data from an open bucket without AWS credentials.
The script prints out contents from one of the buckets. 
The preview image, XML metadatafiles and the first 5 jp2 files are printed out from the first 5 SAFEs.
All of the buckets, the preview images, metadatafiles, and jp2 files are stored in corresponding variables.

Buckets => buckets
All of the bucket contents => bucketcontents
SAFEs => listofsafes
Preview images => previewimage
Metadatafile => metadatafile
CRS Metadatafile => crsmetadatafile
jp2 files => jp2images
"""

import boto3

from botocore import UNSIGNED
from botocore.client import Config

def main() -> int:
        
    # Initialize a boto3 client
    s3 = init_client()
    
    # Use the initialized client to retrieve all the buckets from Sentinel-2 and store them in a variable (buckets)
    buckets = get_buckets(s3)
    
    # Get all of the contents from all of the buckets
    get_contents(s3, buckets)

    return 0

def init_client():

    # Create client using UNSIGNED config to enable getting information from open buckets
    s3 = boto3.client('s3', endpoint_url="https://a3s.fi", region_name="regionOne", config=Config(signature_version=UNSIGNED))

    return s3

def get_buckets(client):

    # Get the Sentinel-2 bucket names from the README-file which is located in bucket 'sentinel-readme'
    readme = client.get_object(Bucket='sentinel-readme', Key='uploadedByMariaYliHeikkila.txt')
    buckets_readme = readme['Body'].read().splitlines()
    
    # Separate the bucket names into a list
    buckets = list(set(list(map(lambda x: x.decode().split('//',1)[1].split('/',1)[0], buckets_readme))))

    # The function returns a list of all the buckets
    return buckets

def get_contents(client, buckets):

    """
    The function to retrieve all of the infromation inside the buckets. For this example only the content of the first bucket is retrieved.  
    If you would like to retrieve more, modify the numbers below:
        line 62: buckets[:->1<-] Only the first bucket
        line 83: listofsafes[:->5<-] Only the first 5 SAFEs
    """

    for bucket in buckets[:1]:

        print('Bucket:', bucket)
        bucketcontents = []

        # Usual list_objects function only lists up to 1000 objects so pagination is needed when using a client
        paginator = client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket)
        # Gets all of the Keys from objects in the bucket
        bucketcontents = [x['Key'] for page in pages for x in page['Contents']]
        
        # These are used to get the relevant filenames from the bucket contents
        # MTD_MSIL2A.xml is the metadatafile, MTD_TL.xml contains CRS Metadata and jp2's are the individual items
        bucketcontent_mtd = [x for x in bucketcontents if x.endswith('MTD_MSIL2A.xml')]
        bucketcontent_crs = [x for x in bucketcontents if x.endswith('MTD_TL.xml')]
        bucketcontent_jp2 = [x for x in bucketcontents if x.endswith('.jp2')]

        # Takes the SAFE-names from the bucket contents and then lists them so that a single SAFE is listed only once
        listofsafes = list(set(list(map(lambda x: x.split('/')[0], bucketcontents))))

        # As there are a bunch of SAFEs in the buckets, only the first five are printed in this example
        for safe in listofsafes[:5]:
            
            print('SAFE:', safe)

            # Using these generators, the right Metadata and CRSMetadata files corresponding to the relevant SAFE are selected from the list
            metadatafile = ''.join((x for x in bucketcontent_mtd if safe in x))
            crsmetadatafile = ''.join((x for x in bucketcontent_crs if safe in x))

            print(' * Metadatafile: https://a3s.fi/' + bucket + '/' +  metadatafile)
            print(' * CRS Metadatafile: https://a3s.fi/' + bucket + '/' +  crsmetadatafile)

            jp2images = []
            # Selects only jp2 that are image bands
            [jp2images.append(x) for x in bucketcontent_jp2 if safe in x and 'IMG_DATA' in x]
            # Selects the jp2s that are preview images
            previewimage = [x for x in bucketcontent_jp2 if safe in x and 'PVI' in x]

            print(' * Preview image: https://a3s.fi/' + bucket + '/' + previewimage[0])

            print(' * First 5 images:')
            # As there are a bunch of images per SAFE, only the first five are printed in this example
            for jp2image in jp2images[:5]:

                uri = 'https://a3s.fi/' + bucket + '/' + jp2image
                print('  - Image URL:', uri)
            

if __name__ == "__main__":
    main()