""" I think you have to do this instead of using the api search """

import numpy as np
import requests
from lxml import html
from astropy.table import Table


def set_payload(pagenum):
    """ Set the payload """
    payload = {'page': '%s' %pagenum, 
               'isTNS_AT': 'yes', 
               'classified_sne': '1', 
               'num_page': '1000', 
               'format': 'csv'}
    return payload


def run_query(pagenum):
    www = 'https://wis-tns.weizmann.ac.il/search'
    r = requests.get(www, params=set_payload(pagenum))
    print(r.url)
    out = r.text.split('\n')
    return out
    

def make_table():
    pagenum = 0
    out = run_query(pagenum)
    #headers = np.array([val.replace('"', '') for val in out[0].split(',')])
    headers = np.array(out[0].split(','))
    ncols = len(headers)
    datatype = np.array([headers.dtype]*ncols) # for use in table initiation
    nrows = len(out[1:])

    # Fill in the table
    t = Table(names=headers, dtype=datatype)
    while nrows > 0:
        for rownum in np.arange(1,nrows-1):
            row = np.array([val.replace('"', '') 
                            for val in out[rownum].split(',')])
            t.add_row(row)
        pagenum += 1
        out = run_query(pagenum)
        nrows = len(out[1:])

    t.write("tns_query_output.csv", format='csv', overwrite=True)


if __name__=="__main__":
    #make_table()
    dat = Table.read("tns_query_output.csv", dtype="ascii.fast_csv")
    #redshift = list(filter(None, dat['redshift']))

