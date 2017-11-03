""" I think you have to do this instead of using the api search """

import requests
from lxml import html
from astropy.table import Table

#www = "https://wis-tns.weizmann.ac.il/search?&amp;page=0&amp;isTNS_AT=yes&amp;classified_sne=1&amp;num_page=1000&amp;format=csv"

payload = {'page': '0', 'isTNS_AT': 'yes', 'classified_sne': '1', 'num_page': '50', 'format': 'csv'}

www = 'https://wis-tns.weizmann.ac.il/search'

r = requests.get(www, params=payload)
print(r.url)

out = r.text.split('\n')
headers = np.array([val.replace('"', '') for val in out[0].split(',')])
ncols = len(headers)

nrows = len(out[1:])

t = Table(names=headers, dtype=[headers.dtype] * ncols)
for rownum in np.arange(1,nrows-1):
    row = np.array(
            [val.replace('"', '') for val in out[rownum].split(',')]).astype(str)
    t.add_row(row)

