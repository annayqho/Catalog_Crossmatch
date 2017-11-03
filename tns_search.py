""" I think you have to do this instead of using the api search """

import numpy as np
import requests
from lxml import html
from astropy.table import Table

#www = "https://wis-tns.weizmann.ac.il/search?&amp;page=0&amp;isTNS_AT=yes&amp;classified_sne=1&amp;num_page=1000&amp;format=csv"

payload = {'page': '0', 'isTNS_AT': 'yes', 'classified_sne': '1', 'num_page': '1000', 'format': 'csv'}

www = 'https://wis-tns.weizmann.ac.il/search'

r = requests.get(www, params=payload)
print(r.url)

pagenum = 0

out = r.text.split('\n')
headers = np.array([val.replace('"', '') for val in out[0].split(',')])
ncols = len(headers)
datatype = np.array([headers.dtype]*ncols) # for use in table initiation
datatype[headers=='redshift'] = 'float'
datatype[headers=='ID'] = 'int'
nrows = len(out[1:])


# Fill in the table
t = Table(names=headers, dtype=[headers.dtype] * ncols)
while nrows > 0:
    for rownum in np.arange(1,nrows-1):
        row = np.array([val.replace('"', '') 
                        for val in out[rownum].split(',')]).astype(str)
        t.add_row(row)
    pagenum += 1
    payload = {'page': '%s' %pagenum, 
               'isTNS_AT': 'yes', 
               'classified_sne': '1', 
               'num_page': '1000', 
               'format': 'csv'}
    r = requests.get(www, params=payload)
    print(r.url) 
    out = r.text.split('\n')
    nrows = len(out[1:])

