# -*- coding: utf-8 -*-
"""
An example script for downloading Sentinel data from FinHub with sentinelsat Python library.

https://finhub.nsdc.fmi.fi
"""

import sentinelsat
from datetime import date
import pandas as pd
import time

### Set your credentials
finhub_user = 'a'
finhub_pwd = 'a'
finhub_url = 'https://finhub.nsdc.fmi.fi'

### Open API connection
finhub_api = sentinelsat.SentinelAPI(finhub_user, finhub_pwd, finhub_url)

### Search by polygon (WGS84), time, and  query keywords
footprint = sentinelsat.geojson_to_wkt(sentinelsat.read_geojson(r'helsinki.geojson'))
startDate = date(2020,1,1)
endDate = date(2020,7,30)
cloudcoverage = (0, 20)
platformname = 'Sentinel-2'
producttype = 'S2MSI1C'
# producttype='S2MSI2A' #for L2 images
area_relation = "Contains"  # footprint has to be fully inside the image. Other options "Intersects", "IsWithin"

### If your area is between two UTM zones, this script often downloads two versions of the same image
### Uncomment and add e.g "T35" to only focus on one UTM zone
utm_zone = ""

### Image output directory
directory_path = r'sentinel_temp'

### Help setting to see product names in full lenghth
pd.set_option('display.max_colwidth', None)
pd.set_option('display.expand_frame_repr', False)

def calculateTotalSize(size_column):
    total_size = 0
    for i in size_column:
        if "MB" in i:
            total_size += float(i.replace(" MB",""))/1000
        if "GB" in i:
           total_size += float(i.replace(" GB",""))
    return round(total_size,2)

def queryAndDownload():

    finhub_products = finhub_api.query(footprint, date=(startDate, endDate), platformname=platformname,
                                       cloudcoverpercentage=cloudcoverage, producttype=producttype,
                                       area_relation=area_relation)

    ### Checking, if any results were found
    if (len(finhub_products) == 0):
        finhub_hasresults = False
        print('No products found from Finhub. Terminating')
    else:
        finhub_hasresults = True

    if finhub_hasresults:
        finhub_df = finhub_api.to_dataframe(finhub_products)
        if utm_zone:
            finhub_df = finhub_df[finhub_df['title'].str.contains(utm_zone)]

        finhub_id_to_download = finhub_df.uuid.tolist()
        print(f'{len(finhub_id_to_download)} image(s) will be downloaded from Finhub repository')
        print(finhub_df.title.to_string(index=False))

    print(f'All together {calculateTotalSize(finhub_df["size"])} GB will be downloaded')

    ### Download files
    if (finhub_hasresults):
        finhub_api.download_all(finhub_id_to_download, directory_path=directory_path)


def main():
    queryAndDownload()


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("The Download script finished in " + str((time.time() - start_time) / 60) + " minutes")

