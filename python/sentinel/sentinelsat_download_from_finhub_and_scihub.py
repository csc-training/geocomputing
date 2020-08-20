# -*- coding: utf-8 -*-
"""
An example script for downloading Sentinel data with sentinelsat Python library.
It first tries to download the data from Finhub,
checking also Scihub for products not available in Finhub.
https://scihub.copernicus.eu
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

scihub_user = 'a'
scihub_pwd = 'a'
scihub_url = 'https://scihub.copernicus.eu/dhus'

### Open API connection
finhub_api = sentinelsat.SentinelAPI(finhub_user, finhub_pwd, finhub_url)
scihub_api = sentinelsat.SentinelAPI(scihub_user, scihub_pwd, scihub_url)

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

def queryAndDownload_preferFinhubToScihub():
    ### See both repositories, which products they have
    scihub_products = scihub_api.query(footprint, date=(startDate, endDate), platformname=platformname,
                                       cloudcoverpercentage=cloudcoverage, producttype=producttype,
                                       area_relation=area_relation)
    finhub_products = finhub_api.query(footprint, date=(startDate, endDate), platformname=platformname,
                                       cloudcoverpercentage=cloudcoverage, producttype=producttype,
                                       area_relation=area_relation)

    ### Checking, if any results were found
    if (len(finhub_products) == 0):
        finhub_hasresults = False
        print('No products found from Finhub')
    else:
        finhub_hasresults = True

    if (len(scihub_products) == 0):
        scihub_hasresults = False
        print('No products found from Scihub')
    else:
        scihub_hasresults = True

    if (not finhub_hasresults and not scihub_hasresults):
        print('No images available from Finhub or Scihub. Terminating')
        return

    ### Change to pandas dataframe (also geopandas option available)
    scihub_df = scihub_api.to_dataframe(scihub_products)
    if utm_zone:
        scihub_df = scihub_df[scihub_df['title'].str.contains(utm_zone)]

    ### Remove from Scihub download list files, that are available in Finhub
    if finhub_hasresults:
        finhub_df = finhub_api.to_dataframe(finhub_products)
        if utm_zone:
            finhub_df = finhub_df[finhub_df['title'].str.contains(utm_zone)]
        scihub_df = scihub_df[~scihub_df.title.isin(finhub_df.title.values)]

        finhub_id_to_download = finhub_df.uuid.tolist()
        print(f'{len(finhub_id_to_download)} image(s) will be downloaded from Finhub repository')
        print(finhub_df.title.to_string(index=False))


    scihub_id_to_download = scihub_df.uuid.tolist()
    print(f'{len(scihub_id_to_download)} image(s) will be downloaded from Scihub repository')
    print(scihub_df.title.to_string(index=False))

    combined_df = scihub_df
    if finhub_hasresults:
        combined_df = pd.concat([scihub_df,finhub_df])

    print(f'All together {calculateTotalSize(combined_df["size"])} GB will be downloaded')

    ### Download files
    scihub_api.download_all(scihub_id_to_download, directory_path=directory_path)
    if (finhub_hasresults):
        finhub_api.download_all(finhub_id_to_download, directory_path=directory_path)


def main():
    queryAndDownload_preferFinhubToScihub()


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("The Download script finished in " + str((time.time() - start_time) / 60) + " minutes")

